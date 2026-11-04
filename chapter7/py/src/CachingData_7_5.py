import time

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.storagelevel import StorageLevel


def print_config(session, key):
    value = session.conf.get(key, None)
    print(f"{key} -> {value}\n")


def timer(block):
    # Python has no by-name parameters, so callers pass a callable.
    start_time = time.perf_counter_ns()
    result = block()
    end_time = time.perf_counter_ns()
    delta_ms = (end_time - start_time) / 1_000_000.0
    return result, delta_ms


def main():
    spark = (
        SparkSession.builder
        .master("local[*]")
        .appName("CachingData")
        .getOrCreate()
    )

    # The Scala example passes a quoted config key; keep that behavior explicit.
    print_config(spark, '"spark.sql.join.preferSortMergeJoin"')

    df = spark.range(1 * 10000000).toDF("id").withColumn("square", F.col("id") * F.col("id"))

    # Cache DataFrame.
    df.cache()
    result, elapsed = timer(lambda: df.count())
    print(f"***** Count={result} and time={elapsed}")

    print("***** Get the second time around")
    result2, elapsed2 = timer(lambda: df.count())
    print(f"***** Count={result2} and time={elapsed2}")

    # Persist on disk.
    df.persist(StorageLevel.DISK_ONLY)
    result3, elapsed3 = timer(lambda: df.count())
    print(f"***** Count={result3} and time={elapsed3}")

    # Create a temporary SQL view.
    df.createOrReplaceTempView("dfTable")
    spark.sql("cache table dfTable")
    result4, elapsed4 = timer(lambda: spark.sql("select count(*) from dfTable").show())
    print(f"***** Count={result4} and time={elapsed4}")

    # Unpersist.
    df.unpersist()


if __name__ == "__main__":
    main()
