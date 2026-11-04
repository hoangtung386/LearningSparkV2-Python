import random
import string

from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StructType,
    StructField,
    IntegerType,
    StringType,
)
from pyspark.sql.functions import col, desc, when


def main():
    spark = SparkSession.builder.appName("Example6_8").getOrCreate()

    # Replace Java's RandomStringUtils with Python's standard library.
    random.seed(42)
    data = []
    for uid in range(1000):
        uname = "user-" + "".join(
            random.choices(string.ascii_letters + string.digits, k=5)
        )
        usage = random.randrange(1000)
        data.append((uid, uname, usage))

    usage_schema = StructType([
        StructField("uid", IntegerType(), False),
        StructField("uname", StringType(), False),
        StructField("usage", IntegerType(), False),
    ])

    # PySpark has no typed Dataset/Encoder API. Use a DataFrame with an explicit schema.
    ds_usage = spark.createDataFrame(data, usage_schema)
    ds_usage.show(10)

    # Filter and order by usage.
    ds_usage.filter(col("usage") > 900).orderBy(col("usage").desc()).show(5)

    # Equivalent of mapping Usage -> Double.
    ds_usage.select(
        when(col("usage") > 750, col("usage") * 0.15)
        .otherwise(col("usage") * 0.50)
        .alias("cost")
    ).show(5)

    # Equivalent of mapping Usage -> UsageCost.
    usage_cost_df = ds_usage.withColumn(
        "cost",
        when(col("usage") > 750, col("usage") * 0.15).otherwise(col("usage") * 0.50),
    )
    usage_cost_df.select("uid", "uname", "usage", "cost").show(5)

    # The same transformation can also be expressed with an RDD map when a
    # function-style transformation is preferred.
    cost_rdd = ds_usage.rdd.map(
        lambda row: (
            row.uid,
            row.uname,
            row.usage,
            row.usage * 0.15 if row.usage > 750 else row.usage * 0.50,
        )
    )
    spark.createDataFrame(cost_rdd, ["uid", "uname", "usage", "cost"]).show(5)


if __name__ == "__main__":
    main()
