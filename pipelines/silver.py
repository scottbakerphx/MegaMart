from pyspark.sql import functions as F, Window
from lib.spark_session import get_spark

spark = get_spark("silver", iceberg=True)
spark.sql("CREATE NAMESPACE IF NOT EXISTS lake.silver")
spark.sparkContext.setLogLevel("ERROR")

c = spark.table("lake.bronze.customers")
clean = (
    c.withColumn("email", F.lower(F.trim("email")))
    .withColumn("name", F.initcap(F.trim("name")))
    .withColumn("country", F.upper(F.trim("country")))
    # keep onmly one row per customer_id: the most recent ingest
    .withColumn(
        "rn",
        F.row_number().over(
            Window.partitionBy("customer_id").orderBy(F.col("_ingest_ts").desc())
        ),
    )
    .filter("rn = 1")
    .drop("rn")
    # define the schema - dont forgetthis - I learned the hard way
    .withColumn("is_current", F.lit(True))
    .withColumn("valid_from", F.current_timestamp())
    .withColumn("valid_to", F.lit(None).cast("timestamp"))
)
# coment these out after run -- the MERGE SQL will lhandle it from now on
clean.writeTo("lake.silver.dim_customer").using(
    "iceberg"
).createOrReplace()  # example write */

orders = spark.table("lake.bronze.orders")
customer = spark.table("lake.silver.dim_customer").select("customer_id")

# riows w/ valid customer -> good - rows /wout -> quarantine (left-anti)
good = orders.join(customer, "customer_id", "left_semi")
quarantine = orders.join(customer, "customer_id", "left_anti").withColumn(
    "reason", F.lit("orphan_customer_id")
)

quarantine.writeTo("lake.silver.orders_quarantine").using("iceberg").createOrReplace()
print("quarantined orphan orders:", quarantine.count())

#  create clean dataframe for ability to query - i learned the hard way
clean.createOrReplaceTempView("staged_customer_changes")

# close changed rows - app inserts new current ros
# dim_cusotmer cols: customer_id, name, email, valid_from, valid_to, is_current
spark.sql("""
MERGE INTO lake.silver.dim_customer t
USING staged_customer_changes s
ON  t.customer_id = s.customer_id AND t.is_current = true
WHEN MATCHED AND (t.email <> s.email OR t.name <> s.name) THEN
  UPDATE SET t.is_current = false, t.valid_to = current_timestamp()
""")

clicks = spark.table("lake.bronze.clickstream").filter(
    "user_id IS NOT NULL AND is_bot = false"
)
w = Window.partitionBy("user_id").orderBy("event_ts")
sessions = (
    clicks.withColumn("prev_ts", F.lag("event_ts").over(w))
    .withColumn(
        "gap_min", (F.col("event_ts").cast("long") - F.col("prev_ts").cast("long")) / 60
    )
    # new session when >30 min since previous event
    .withColumn(
        "new_session", (F.col("gap_min").isNull() | (F.col("gap_min") > 30)).cast("int")
    )
    .withColumn("session_no", F.sum("new_session").over(w))
)
sessions.writeTo("lake.silver.fact_clickstream_sessions").using(
    "iceberg"
).createOrReplace()
