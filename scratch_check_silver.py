from lib.spark_session import get_spark

spark = get_spark(app_name="silver_check", iceberg=True)

spark.sql("SELECT customer_id, name, email, is_current, valid_from FROM lake.silver.dim_customer LIMIT 10").show(truncate=False)

spark.stop()