from lib.spark_session import get_spark


# Initialize the session (turn iceberg=True to read the catalog)
spark = get_spark(app_name="bronze_checks", iceberg=True)

# 1. Show all tables in the bronze namespace
print("--- BRONZE TABLES ---")
spark.sql("SHOW TABLES IN lake.bronze").show(truncate=False)

# 2. Check row count (Should be 2,020,188 based on your ingest)
print("--- ORDERS COUNT ---")
spark.sql("SELECT count(*) AS total_orders FROM lake.bronze.orders").show()

# 3. View Iceberg snapshot history
print("--- ICEBERG SNAPSHOTS ---")
spark.sql("SELECT committed_at, snapshot_id, operation FROM lake.bronze.orders.snapshots").show(truncate=False)

# 4. View Iceberg partitions (Event day)
print("--- ORDERS PARTITIONS ---")
spark.sql("SELECT record_count, file_count, total_data_file_size_in_bytes FROM lake.bronze.orders.partitions").show(truncate=False)
spark.sparkContext.setLogLevel("ERROR")

spark.stop()