# Databricks notebook source
import dlt
from pyspark.sql.functions import col, expr

@dlt.view
def users():
  return spark.readStream.format("delta").table("cdc_data.users_nk")

dlt.create_streaming_table("target_users_nk")

dlt.apply_changes(
  target = "target_users_nk",
  source = "users",
  keys = ["userId"],
  sequence_by = col("sequenceNum"),
  apply_as_deletes = expr("operation = 'DELETE'"),
  except_column_list = ["operation", "sequenceNum"],
  stored_as_scd_type = "2",
  track_history_except_column_list = ["city"]
)

# COMMAND ----------


