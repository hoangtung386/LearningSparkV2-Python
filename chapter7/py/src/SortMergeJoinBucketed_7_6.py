import random

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.storagelevel import StorageLevel


def main():
    spark = (
        SparkSession.builder
        .appName("SortMergeJoinBucketed")
        .config("spark.sql.codegen.wholeStage", True)
        .config("spark.sql.join.preferSortMergeJoin", True)
        .config("spark.sql.autoBroadcastJoinThreshold", -1)
        .config("spark.sql.defaultSizeInBytes", 100000)
        .config("spark.sql.shuffle.partitions", 16)
        .getOrCreate()
    )

    states = {0: "AZ", 1: "CO", 2: "CA", 3: "TX", 4: "NY", 5: "MI"}
    items = {i: f"SKU-{i}" for i in range(6)}
    rnd = random.Random(42)

    users_data = [
        (uid, f"user_{uid}", f"user_{uid}@databricks.com", states[rnd.randrange(5)])
        for uid in range(100001)
    ]
    orders_data = [
        (
            transaction_id,
            transaction_id,
            rnd.randrange(100000),
            10 * transaction_id * 0.2,
            states[rnd.randrange(5)],
            items[rnd.randrange(5)],
        )
        for transaction_id in range(100001)
    ]

    users_df = spark.createDataFrame(
        users_data, ["uid", "login", "email", "user_state"]
    )
    orders_df = spark.createDataFrame(
        orders_data,
        ["transaction_id", "quantity", "users_id", "amount", "state", "items"],
    )

    # Cache them on disk only so the storage UI can show the difference in size.
    users_df.persist(StorageLevel.DISK_ONLY)
    orders_df.persist(StorageLevel.DISK_ONLY)

    # Create bucketed tables.
    spark.sql("DROP TABLE IF EXISTS UsersTbl")
    (
        users_df.orderBy(F.asc("uid"))
        .write.format("parquet")
        .mode("overwrite")
        .bucketBy(8, "uid")
        .saveAsTable("UsersTbl")
    )

    spark.sql("DROP TABLE IF EXISTS OrdersTbl")
    (
        orders_df.orderBy(F.asc("users_id"))
        .write.format("parquet")
        .mode("overwrite")
        .bucketBy(8, "users_id")
        .saveAsTable("OrdersTbl")
    )

    spark.sql("CACHE TABLE UsersTbl")
    spark.sql("CACHE TABLE OrdersTbl")
    spark.sql("SELECT * from OrdersTbl LIMIT 20")

    # Read data back in.
    users_bucket_df = spark.table("UsersTbl")
    orders_bucket_df = spark.table("OrdersTbl")

    # Join on the bucketed DataFrames.
    join_users_orders_bucket_df = orders_bucket_df.join(
        users_bucket_df, F.col("users_id") == F.col("uid")
    )
    join_users_orders_bucket_df.show(truncate=False)
    join_users_orders_bucket_df.explain()


if __name__ == "__main__":
    main()
