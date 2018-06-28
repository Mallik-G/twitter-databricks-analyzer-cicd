# Databricks notebook source
# Databricks notebook source
from pyspark.sql.functions import *
from pyspark.sql.types import *

eventhub_namespace = dbutils.preview.secret.get(scope = "storage_scope", key = "eventhub_namespace")
eventhub_enriched = dbutils.preview.secret.get(scope = "storage_scope", key = "eventhub_enriched")
eventhub_alerts = dbutils.preview.secret.get(scope = "storage_scope", key = "eventhub_alerts")
eventhub_key = dbutils.preview.secret.get(scope = "storage_scope", key = "eventhub_key")
readConnectionString = "Endpoint=sb://{ns}.servicebus.windows.net/;" \
                       "EntityPath={name};SharedAccessKeyName=RootManageSharedAccessKey;" \
                       "SharedAccessKey={key}".format(ns=eventhub_namespace, name=eventhub_enriched, key=eventhub_key)
writeConnectionString = "Endpoint=sb://{ns}.servicebus.windows.net/;" \
                       "EntityPath={name};SharedAccessKeyName=RootManageSharedAccessKey;" \
                       "SharedAccessKey={key}".format(ns=eventhub_namespace, name=eventhub_alerts, key=eventhub_key)
ehReadConf = {
  'eventhubs.connectionString': readConnectionString
}
ehWriteConf = {
  'eventhubs.connectionString': writeConnectionString
}

# COMMAND ----------

inputStream = spark.readStream \
  .format("eventhubs") \
  .options(**ehReadConf) \
  .load()
  
# Cast the data as string (it comes in as binary by default)
bodyNoSchema = inputStream.selectExpr("CAST(body as STRING)", "CAST (enqueuedTime as timestamp) AS Time")

display(bodyNoSchema)

# COMMAND ----------

# Write body data from a DataFrame to EventHubs. Events are distributed across partitions using round-robin model.
ds = bodyNoSchema \
  .writeStream \
  .format("eventhubs") \
  .options(**ehWriteConf) \
  .option("checkpointLocation", "/mnt/tmp/checkpoint.tmp") \
  .start()

# COMMAND ----------


