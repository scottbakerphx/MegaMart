from lib.spark_session import get_spark

spark = get_spark(app_name="silver_verification", iceberg=True)

print("--- 1. VERIFY SILVER TABLES ---")
# Verify dim_customer, dim_product, fact_orders, fact_clickstream_sessions, orders_quarantine, dq_report exist
spark.sql("SHOW TABLES IN lake.silver").show(truncate=False)

print("--- 2. VERIFY DIM_CUSTOMER COLUMNS ---")
# The query you provided: explicitly shows the SCD2 columns (is_current, valid_from, valid_to) are present
spark.sql("""
    SELECT customer_id, name, email, is_current, valid_from, valid_to 
    FROM lake.silver.dim_customer 
    LIMIT 10
""").show(truncate=False)

print("--- 3. RECONCILIATION: BRONZE = GOOD + QUARANTINE ---")
# Proves no data was lost during the silver transformation (good + quarantined = bronze orders)
spark.sql("""
    SELECT 
        (SELECT count(*) FROM lake.bronze.orders) AS bronze_raw_total,
        (SELECT count(*) FROM lake.silver.fact_orders) AS silver_good_orders,
        (SELECT count(*) FROM lake.silver.orders_quarantine) AS silver_quarantined,
        ((SELECT count(*) FROM lake.silver.fact_orders) + 
         (SELECT count(*) FROM lake.silver.orders_quarantine)) AS silver_total_reconciled
""").show()

print("--- 4. SCD2 VERIFICATION: CLOSED + CURRENT ROW ---")
# Dynamically acts as WHERE customer_id = <one that changed> by finding rows that have history
spark.sql("""
    SELECT customer_id, name, email, is_current, valid_from, valid_to
    FROM lake.silver.dim_customer
    WHERE customer_id IN (
        SELECT customer_id 
        FROM lake.silver.dim_customer 
        GROUP BY customer_id 
        HAVING count(*) > 1
    )
    ORDER BY customer_id, valid_from DESC
    LIMIT 10
""").show(truncate=False)
spark.sparkContext.setLogLevel("ERROR")

spark.stop()