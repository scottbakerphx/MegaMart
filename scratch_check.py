# save as scratch_check.py, run:  env -u SPARK_HOME python scratch_check.py
from lib.spark_session import get_spark

spark = get_spark("e2e", iceberg=True)
spark.sql("CREATE NAMESPACE IF NOT EXISTS lake.smoke")
spark.sql("DROP TABLE IF EXISTS lake.smoke.hello")
(
    spark.createDataFrame([(1, "bronze"), (2, "silver"), (3, "gold")], ["id", "layer"])
    .writeTo("lake.smoke.hello")
    .using("iceberg")
    .create()
)
spark.table("lake.smoke.hello").orderBy("id").show()
spark.stop()
