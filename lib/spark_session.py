"""
Optimized local Spark session for the MegaMart build rig
    - 20 cores / ~6=2GB ddr5 ram, using 16 cores.
Usage (Pycharm or cli), from repo root with the ~db-lab env active:
    from lib.spark_session import get_spark
    spark = get_spark("broze-ingest") 16 cores, tuned driver memory
    Iceberg ready

    spark.driver.memory is a JVM launch time arg - setting in builder is ignored
        in local mode because the JVM is already up. Set via PYSPARK_SUNBMIT_ARGS
        before pyspark launches the gateway
    System SPARK_HOME=/opt/apache-spark (separate spark) collides w/ venv's Sprak
        and causes JavaPackqage object is nt callable. We uset it to the venv's
        Sparks is used
    Spark 3.5.3 breaks with Java 21 so we pin Java 17
    PySpark 3.5.3 + Java 17 + Iceberg 1.6.1 writng to native MinIO

    local mode note: local[16] runs irt al inn one driver JVM
        no separate executors -- so DRIVER memory + pat=rallelsism matter most
        in this case and hence, we tune below:
"""

from __future__ import annotations
import os

# rig tuning
CORES = int(os.environ.get("SPARK_CORES", "16"))
DRIVER_MEM = os.environ.get("SPARK_DRIVER_MEM", "48G")
SHUFFLE_PARTS = str(CORES * 4)
MAX_RESULT = os.environ.get("SPARK_MAX_RESULT","4G")

# Set driver memory + GC before JV launches -> PYSPARK_SUBMIT_ARGS
os.environ.setdefault(
    "PYSPARK_SUBMIT_ARGS",
    f"--driver-memory {DRIVER_MEM} "
    f"--driver-java-options '-XX:+UseG1GC -XX:+UseCompressedOops' "
    f"pyspark-shell",
)

# avoid system Spark 3.5 at /opt/apache-spark collision
os.environ.pop("SPARK_HOME", None)

# python workers need to use this venv's interpreter
os.environ.setdefault("PYSPARK_PYTHON",
                      os.path.join(os.environ.get("VIRTUAL_ENV", ""),
                      "bin",
                      "python"))

# Spark 3.5. needs Java 18/11/17 my default is Java 17
_JDK17 = "/usr/lib/jvm/java-17-openjdk"
if os.path.isdir(_JDK17):
    os.environ["JAVA_HOME"] = _JDK17

from pyspark.sql import SparkSession # noqa: E402 (import after env is set)


def get_spark(
        app_name: str = "megamart",
        *,
        iceberg: bool = False,
        warehouse: str = "s3a://lakehouse/warehouse",
        minio_endpoint: str | None = None
) -> SparkSession:
    """Build the tuned local SparkSession. set iceberg = True to enable
       Iceberg + Hadoop catalog on MinIO"""

    builder = (
        SparkSession.builder.appName(app_name)
        .master(f"local[{CORES}]")
        # parallelism
        .config("spark.sql.shuffle.partitions", SHUFFLE_PARTS)
        .config("spark.default.parallelism", str(CORES * 2))
        # adaptive exec - smal partitions skew handles) default but make explicit
        .config("spark.sql.adaptive.enabled", "true")
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true")
        .config("spark.sql.adaptive.skewJoin.enabled", "true")
        # big-box scan sizing + result safety
        .config("spark.sql.files.maxPartitionBytes", "256M")
        .config("spark.driver.maxResultSize", MAX_RESULT)
        # faster serialization
        .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
    )

    if iceberg:
        """ Iceberg Spark runtime (pulled via packages) + Hadoop catalog named 'lake'
            on MinIO """
        builder = (
            builder.config(
                "spark.jars.packages",
                "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.6.1,"
                "org.apache.hadoop:hadoop-aws:3.3.4,"
                "com.amazonaws:aws-java-sdk-bundle:1.12.262"
            )
            .config(
                "spark.sql.extensions",
                "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions"
            )
            .config(
                "spark.sql.catalog.lake",
                "org.apache.iceberg.spark.SparkCatalog"\
                )
            .config(
                "spark.sql.catalog.lake.type",
                "hadoop"
            )
            .config(
                "spark.sql.catalog.lake.warehouse",
                warehouse
            )
            # S3A / MinIO
            .config(
                "spark.hadoop.fs.s3a.endpoint",
                minio_endpoint
                or os.environ.get("MINIO_ENDPOINT", "http://localhost:9000")
            )
            .config(
                "spark.hadoop.fs.s3a.access.key",
                os.environ.get("MINIO_ACCESS_KEY", "minioadmin")
            )
            .config(
                "spark.hadoop.fs.s3a.secret.key",
                os.environ.get("MINIO_SECRET_KEY", "gggggggg")
            )
            .config(
                "spark.hadoop.fs.s3a.path.style.access", "true"
            )
            .config(
                "spark.hadoop.fs.s3a.impl",
                "org.apache.hadoop.fs.s3a.S3AFileSystem"
            )
        )

    spark = builder.getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    return spark


if __name__ == "__main__":
    s = get_spark("rig-check")
    jvm_max_gb = s.sparkContext._jvm.java.lang.Runtime.getRuntime().maxMemory() / (1024 ** 3)
    print(f"master           = {s.sparkContext.master}")
    print(f"driver.memory    = {s.conf.get('spark.driver.memory', '(default)')}")
    print(f"JVM max heap     = {jvm_max_gb:.1f} GB   (proves --driver-memory took)")
    print(f"shuffle.parts    = {s.conf.get('spark.sql.shuffle.partitions')}")
    print(f"defaultParallel  = {s.sparkContext.defaultParallelism}")
    s.stop()