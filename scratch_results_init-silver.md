 [sbaker@archlinux MegaMart]$ python scratch_check_silver.py
OpenJDK 64-Bit Server VM warning: Max heap size too large for Compressed Oops
:: loading settings :: url = jar:file:/home/sbaker/MegaMart/.venv/lib/python3.12/site-packages/pyspark/jars/ivy-2.5.1.jar!/org/apache/ivy/core/settings/ivysettings.xml
Ivy Default Cache set to: /home/sbaker/.ivy2/cache
The jars for the packages stored in: /home/sbaker/.ivy2/jars
org.apache.iceberg#iceberg-spark-runtime-3.5_2.12 added as a dependency
org.apache.hadoop#hadoop-aws added as a dependency
com.amazonaws#aws-java-sdk-bundle added as a dependency
:: resolving dependencies :: org.apache.spark#spark-submit-parent-cf3087e9-439f-4ed0-8821-2888d0059422;1.0
        confs: [default]
        found org.apache.iceberg#iceberg-spark-runtime-3.5_2.12;1.6.1 in central
        found org.apache.hadoop#hadoop-aws;3.3.4 in central
        found com.amazonaws#aws-java-sdk-bundle;1.12.262 in central
        found org.wildfly.openssl#wildfly-openssl;1.0.7.Final in central
:: resolution report :: resolve 73ms :: artifacts dl 2ms
        :: modules in use:
        com.amazonaws#aws-java-sdk-bundle;1.12.262 from central in [default]
        org.apache.hadoop#hadoop-aws;3.3.4 from central in [default]
        org.apache.iceberg#iceberg-spark-runtime-3.5_2.12;1.6.1 from central in [default]
        org.wildfly.openssl#wildfly-openssl;1.0.7.Final from central in [default]
        ---------------------------------------------------------------------
        |                  |            modules            ||   artifacts   |
        |       conf       | number| search|dwnlded|evicted|| number|dwnlded|
        ---------------------------------------------------------------------
        |      default     |   4   |   0   |   0   |   0   ||   4   |   0   |
        ---------------------------------------------------------------------
:: retrieving :: org.apache.spark#spark-submit-parent-cf3087e9-439f-4ed0-8821-2888d0059422
        confs: [default]
        0 artifacts copied, 4 already retrieved (0kB/2ms)
26/08/07 14:28:11 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
26/08/07 14:28:12 WARN MetricsConfig: Cannot locate configuration: tried hadoop-metrics2-s3a-file-system.properties,hadoop-metrics2.properties
+-----------+------------+----------------+----------+--------------------------+
|customer_id|name        |email           |is_current|valid_from                |
+-----------+------------+----------------+----------+--------------------------+
|6          |Customer_6  |user6@mail.com  |true      |2026-08-07 14:16:26.471469|
|9          |Customer_9  |NULL            |true      |2026-08-07 14:16:26.471469|
|35         |Customer_35 |user35@mail.com |true      |2026-08-07 14:16:26.471469|
|45         |Customer_45 |user45@mail.com |true      |2026-08-07 14:16:26.471469|
|49         |Customer_49 |user49@mail.com |true      |2026-08-07 14:16:26.471469|
|61         |Customer_61 |user61@mail.com |true      |2026-08-07 14:16:26.471469|
|93         |Customer_93 |NULL            |true      |2026-08-07 14:16:26.471469|
|110        |Customer_110|NULL            |true      |2026-08-07 14:16:26.471469|
|114        |Customer_114|user114@mail.com|true      |2026-08-07 14:16:26.471469|
|120        |Customer_120|user120@mail.com|true      |2026-08-07 14:16:26.471469|
+-----------+------------+----------------+----------+--------------------------+

(.venv) [sbaker@archlinux MegaMart]$ python scratch_check_bronze.py
OpenJDK 64-Bit Server VM warning: Max heap size too large for Compressed Oops
:: loading settings :: url = jar:file:/home/sbaker/MegaMart/.venv/lib/python3.12/site-packages/pyspark/jars/ivy-2.5.1.jar!/org/apache/ivy/core/settings/ivysettings.xml
Ivy Default Cache set to: /home/sbaker/.ivy2/cache
The jars for the packages stored in: /home/sbaker/.ivy2/jars
org.apache.iceberg#iceberg-spark-runtime-3.5_2.12 added as a dependency
org.apache.hadoop#hadoop-aws added as a dependency
com.amazonaws#aws-java-sdk-bundle added as a dependency
:: resolving dependencies :: org.apache.spark#spark-submit-parent-d32e675d-1a2c-405f-9aef-345f54a6c7bf;1.0
        confs: [default]
        found org.apache.iceberg#iceberg-spark-runtime-3.5_2.12;1.6.1 in central
        found org.apache.hadoop#hadoop-aws;3.3.4 in central
        found com.amazonaws#aws-java-sdk-bundle;1.12.262 in central
        found org.wildfly.openssl#wildfly-openssl;1.0.7.Final in central
:: resolution report :: resolve 71ms :: artifacts dl 2ms
        :: modules in use:
        com.amazonaws#aws-java-sdk-bundle;1.12.262 from central in [default]
        org.apache.hadoop#hadoop-aws;3.3.4 from central in [default]
        org.apache.iceberg#iceberg-spark-runtime-3.5_2.12;1.6.1 from central in [default]
        org.wildfly.openssl#wildfly-openssl;1.0.7.Final from central in [default]
        ---------------------------------------------------------------------
        |                  |            modules            ||   artifacts   |
        |       conf       | number| search|dwnlded|evicted|| number|dwnlded|
        ---------------------------------------------------------------------
        |      default     |   4   |   0   |   0   |   0   ||   4   |   0   |
        ---------------------------------------------------------------------
:: retrieving :: org.apache.spark#spark-submit-parent-d32e675d-1a2c-405f-9aef-345f54a6c7bf
        confs: [default]
        0 artifacts copied, 4 already retrieved (0kB/2ms)
26/08/07 14:28:32 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
--- BRONZE TABLES ---
26/08/07 14:28:34 WARN MetricsConfig: Cannot locate configuration: tried hadoop-metrics2-s3a-file-system.properties,hadoop-metrics2.properties
+---------+-----------+-----------+
|namespace|tableName  |isTemporary|
+---------+-----------+-----------+
|bronze   |payments   |false      |
|bronze   |customers  |false      |
|bronze   |orders     |false      |
|bronze   |products   |false      |
|bronze   |clickstream|false      |
+---------+-----------+-----------+

--- ORDERS COUNT ---
+------------+
|total_orders|
+------------+
|     2020188|
+------------+

--- ICEBERG SNAPSHOTS ---
+-----------------------+-------------------+---------+
|committed_at           |snapshot_id        |operation|
+-----------------------+-------------------+---------+
|2026-08-07 10:47:41.811|1917114047514439617|append   |
|2026-08-07 10:50:53.984|6516229298478476356|append   |
+-----------------------+-------------------+---------+

--- ORDERS PARTITIONS ---
+------------+----------+-----------------------------+
|record_count|file_count|total_data_file_size_in_bytes|
+------------+----------+-----------------------------+
|2020188     |181       |39900729                     |
+------------+----------+-----------------------------+

(.venv) [sbaker@archlinux MegaMart]$ python scratch_check_init.py
OpenJDK 64-Bit Server VM warning: Max heap size too large for Compressed Oops
:: loading settings :: url = jar:file:/home/sbaker/MegaMart/.venv/lib/python3.12/site-packages/pyspark/jars/ivy-2.5.1.jar!/org/apache/ivy/core/settings/ivysettings.xml
Ivy Default Cache set to: /home/sbaker/.ivy2/cache
The jars for the packages stored in: /home/sbaker/.ivy2/jars
org.apache.iceberg#iceberg-spark-runtime-3.5_2.12 added as a dependency
org.apache.hadoop#hadoop-aws added as a dependency
com.amazonaws#aws-java-sdk-bundle added as a dependency
:: resolving dependencies :: org.apache.spark#spark-submit-parent-5bf8d0ee-b616-4eb0-bbc8-0d19545c6930;1.0
        confs: [default]
        found org.apache.iceberg#iceberg-spark-runtime-3.5_2.12;1.6.1 in central
        found org.apache.hadoop#hadoop-aws;3.3.4 in central
        found com.amazonaws#aws-java-sdk-bundle;1.12.262 in central
        found org.wildfly.openssl#wildfly-openssl;1.0.7.Final in central
:: resolution report :: resolve 74ms :: artifacts dl 2ms
        :: modules in use:
        com.amazonaws#aws-java-sdk-bundle;1.12.262 from central in [default]
        org.apache.hadoop#hadoop-aws;3.3.4 from central in [default]
        org.apache.iceberg#iceberg-spark-runtime-3.5_2.12;1.6.1 from central in [default]
        org.wildfly.openssl#wildfly-openssl;1.0.7.Final from central in [default]
        ---------------------------------------------------------------------
        |                  |            modules            ||   artifacts   |
        |       conf       | number| search|dwnlded|evicted|| number|dwnlded|
        ---------------------------------------------------------------------
        |      default     |   4   |   0   |   0   |   0   ||   4   |   0   |
        ---------------------------------------------------------------------
:: retrieving :: org.apache.spark#spark-submit-parent-5bf8d0ee-b616-4eb0-bbc8-0d19545c6930
        confs: [default]
        0 artifacts copied, 4 already retrieved (0kB/2ms)
26/08/07 14:28:44 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
--- SHOW TABLES IN lake.bronze ---
26/08/07 14:28:45 WARN MetricsConfig: Cannot locate configuration: tried hadoop-metrics2-s3a-file-system.properties,hadoop-metrics2.properties
+---------+-----------+-----------+
|namespace|tableName  |isTemporary|
+---------+-----------+-----------+
|bronze   |payments   |false      |
|bronze   |customers  |false      |
|bronze   |orders     |false      |
|bronze   |products   |false      |
|bronze   |clickstream|false      |
+---------+-----------+-----------+

--- SELECT count(*) FROM lake.bronze.orders ---
+--------+
|count(1)|
+--------+
| 2020188|
+--------+

--- SELECT * FROM lake.bronze.orders.snapshots ---
+-----------------------+-------------------+---------+---------+---------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|committed_at           |snapshot_id        |parent_id|operation|manifest_list                                                                                                        |summary                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
+-----------------------+-------------------+---------+---------+---------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|2026-08-07 10:47:41.811|1917114047514439617|NULL     |append   |s3a://lakehouse/warehouse/bronze/orders/metadata/snap-1917114047514439617-1-000f9ec7-b3ad-4095-8945-78413f13cb68.avro|{spark.app.id -> local-1786124855115, added-data-files -> 181, added-records -> 2020188, added-files-size -> 39900729, changed-partition-count -> 1, total-records -> 2020188, total-files-size -> 39900729, total-data-files -> 181, total-delete-files -> 0, total-position-deletes -> 0, total-equality-deletes -> 0, engine-version -> 3.5.3, app-id -> local-1786124855115, engine-name -> spark, iceberg-version -> Apache Iceberg 1.6.1 (commit 8e9d59d299be42b0bca9461457cd1e95dbaad086)}|
|2026-08-07 10:50:53.984|6516229298478476356|NULL     |append   |s3a://lakehouse/warehouse/bronze/orders/metadata/snap-6516229298478476356-1-e2739408-e34b-43d0-8f82-c26d1e812eb7.avro|{spark.app.id -> local-1786125047377, added-data-files -> 181, added-records -> 2020188, added-files-size -> 39900729, changed-partition-count -> 1, total-records -> 2020188, total-files-size -> 39900729, total-data-files -> 181, total-delete-files -> 0, total-position-deletes -> 0, total-equality-deletes -> 0, engine-version -> 3.5.3, app-id -> local-1786125047377, engine-name -> spark, iceberg-version -> Apache Iceberg 1.6.1 (commit 8e9d59d299be42b0bca9461457cd1e95dbaad086)}|
+-----------------------+-------------------+---------+---------+---------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

--- SELECT * FROM lake.bronze.orders.partitions ---
+------------+----------+-----------------------------+----------------------------+--------------------------+----------------------------+--------------------------+-----------------------+------------------------+
|record_count|file_count|total_data_file_size_in_bytes|position_delete_record_count|position_delete_file_count|equality_delete_record_count|equality_delete_file_count|last_updated_at        |last_updated_snapshot_id|
+------------+----------+-----------------------------+----------------------------+--------------------------+----------------------------+--------------------------+-----------------------+------------------------+
|2020188     |181       |39900729                     |0                           |0                         |0                           |0                         |2026-08-07 10:50:53.984|6516229298478476356     |
+------------+----------+-----------------------------+----------------------------+--------------------------+----------------------------+--------------------------+-----------------------+------------------------+

(.venv) [sbaker@archlinux MegaMart]$ 