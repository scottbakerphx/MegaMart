from lib.spark_session import get_spark

spark = get_spark(app_name="bronze_checks", iceberg=True)

print("--- SHOW TABLES IN lake.bronze ---")
spark.sql("SHOW TABLES IN lake.bronze").show(truncate=False)

print("--- SELECT count(*) FROM lake.bronze.orders ---")
spark.sql("SELECT count(*) FROM lake.bronze.orders").show()

print("--- SELECT * FROM lake.bronze.orders.snapshots ---")
spark.sql("SELECT * FROM lake.bronze.orders.snapshots").show(truncate=False)

print("--- SELECT * FROM lake.bronze.orders.partitions ---")
spark.sql("SELECT * FROM lake.bronze.orders.partitions").show(truncate=False)

spark.stop()