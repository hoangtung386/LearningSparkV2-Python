import random

from pyspark.sql import SparkSession
from pyspark.sql import functions as F


def main():
    spark = (
        SparkSession.builder
        .appName("SortMergeJoin")
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

    # Scala's nextInt(5) returns values in [0, 4].
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

    users_df.show(10)
    orders_df.show(10)

    users_orders_df = orders_df.join(users_df, F.col("users_id") == F.col("uid"))
    users_orders_df.show(10, truncate=False)
    users_orders_df.cache()
    users_orders_df.explain()


if __name__ == "__main__":
    main()
