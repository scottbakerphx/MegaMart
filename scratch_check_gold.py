from lib.spark_session import get_spark

spark = get_spark(app_name="gold_verification", iceberg=True)

print("--- 1. VERIFY GOLD TABLES ---")
# Check that daily_sales, customer_360, and customer_churn_scores exist
spark.sql("SHOW TABLES IN lake.gold").show(truncate=False)

print("--- 2. CHECK DAILY SALES METRICS ---")
# Verify the aggregations worked properly
spark.sql("""
    SELECT event_date, category, revenue, orders, buyers 
    FROM lake.gold.daily_sales 
    ORDER BY revenue DESC 
    LIMIT 10
""").show(truncate=False)

print("--- 3. CHECK CUSTOMER 360 & CHURN SCORES ---")
# Join the RFM stats with the ML predictions we just generated
spark.sql("""
    SELECT c.customer_id, c.recency_days, c.frequency, c.monetary, 
           round(s.churn_probability, 4) as churn_risk
    FROM lake.gold.customer_360 c
    LEFT JOIN lake.gold.customer_churn_scores s 
      ON c.customer_id = s.customer_id
    ORDER BY s.churn_probability DESC
    LIMIT 10
""").show(truncate=False)

print("--- 4. ICEBERG TABLE MAINTENANCE (COMPACTION) ---")
# Compact small files into optimized larger files for faster read performance
print("Compacting lake.gold.daily_sales...")
spark.sql("CALL lake.system.rewrite_data_files('lake.gold.daily_sales')").show()

print("Compacting lake.gold.customer_360...")
spark.sql("CALL lake.system.rewrite_data_files('lake.gold.customer_360')").show()

# (Optional: prune old snapshots to save disk space if they get too large)
# spark.sql("CALL lake.system.expire_snapshots('lake.gold.daily_sales', retain_last => 5)")
spark.sparkContext.setLogLevel("ERROR")

spark.stop()