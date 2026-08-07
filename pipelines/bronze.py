from pyspark.sql import functions as F
from lib.spark_session import get_spark

spark = get_spark("bronze_ingest", iceberg=True)
spark.sql("CREATE NAMESPACE IF NOT EXISTS lake.bronze")

SOURCES = {
    "customers": None,
    "products": None,
    "orders": None,
    "clickstream": "event_ts",
    "payments": None
}

spark.sparkContext.setLogLevel("ERROR")

for name, ts_col in SOURCES.items():
    df = (spark.read.parquet(f"file:///home/sbaker/databricks-lab/data/raw/{name}")
          .withColumn("_ingest_ts",
                      F.current_timestamp())
          .withColumn("_source_file",
                      F.input_file_name())
          .withColumn("_ingest_batch",
                      F.lit("batch-0001"))
          )
    writer = (df.writeTo(f"lake.bronze.{name}")
              .using("iceberg"))
    if ts_col:
        #iceberg hidden partitioning: 1 part per calendar day
        writer  = writer.partitionedBy(F.days(F.col(ts_col)))
    writer.createOrReplace()
    print(f"bronze.{name}: {spark.table(
        f'lake.bronze.{name}')
        .count():,} rows")
spark.stop()