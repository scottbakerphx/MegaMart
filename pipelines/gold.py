from pyspark.sql import functions as F
from lib.spark_session import get_spark

spark = get_spark("gold", iceberg=True)
spark.sql("CREATE NAMESPACE IF NOT EXISTS lake.gold")

orders = spark.table("lake.silver.fact_orders")
product = spark.table("lake.silver.dim_product").select("product_id", "category")

daily = (
    orders.join(F.broadcast(product), "product_id")
    .groupby("event_date", "category")
    .agg(
        F.sum("total").alias("revenue"),
        F.count("*").alias("orders"),
        F.countDistinct("customer_id").alias("buyers"),
    )
)

(
    daily.writeTo("lake.gold.daily_sales")
    .using("iceberg")
    .partitionedBy(F.months("event_date"))
    .createOrReplace()
)

print("gold.daily_sales rows:", spark.table("lake.gold.daily_sales").count())

#  recency frequency monetary stats per customer -> segmentation + churn features
rFm = orders.groupby("customer_id").agg(
    F.datediff(F.current_date(), F.max("event_date")).alias("recency_days"),
    F.count("*").alias("frequency"),
    F.sum("total").alias("monetary"),
)

customer = (
    spark.table("lake.silver.dim_customer")
    .where("is_current = true")
    .select("customer_id", "name", "country")
)

spark.sparkContext.setLogLevel("ERROR")

customer_360 = rFm.join(customer, "customer_id", "left")
customer_360.writeTo("lake.gold.customer_360").using("iceberg").createOrReplace()
