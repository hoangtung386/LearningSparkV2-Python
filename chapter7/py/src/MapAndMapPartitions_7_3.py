import math
import time

from pyspark.sql import SparkSession
from pyspark.sql import functions as F


def get_connection(filename):
    # Python equivalent of appending to a file.
    return open(filename, "a")


def func(value):
    # Equivalent of the Scala func(v), but with safe resource handling.
    connection = get_connection("/tmp/sqrt.txt")
    try:
        square_root = math.sqrt(value)
        connection.write(str(square_root))
        connection.write("\n")
    finally:
        connection.close()
    return square_root


def func_map_partitions(connection, value):
    square_root = math.sqrt(value)
    connection.write(str(square_root))
    connection.write("\n")
    return square_root


def benchmark(name, block):
    # Python has no by-name parameters, so callers pass a callable.
    start_time = time.perf_counter()
    block()
    end_time = time.perf_counter()
    print(f"Time taken in {name}: {end_time - start_time} seconds")


def main():
    spark = SparkSession.builder.appName("MapAndMapPartitions").getOrCreate()

    df = (
        spark.range(1 * 10000000)
        .toDF("id")
        .withColumn("square", F.col("id") * F.col("id"))
        .repartition(16)
    )
    df.show(5)

    # Equivalent of df.map(r => func(r.getLong(1))).
    benchmark(
        "map function",
        lambda: df.rdd.map(lambda row: func(row[1])).toDF().show(10),
    )

    # Equivalent of df.mapPartitions(...).
    def map_partition(iterator):
        connection = get_connection("/tmp/sqrt.txt")
        try:
            result = [func_map_partitions(connection, row[1]) for row in iterator]
        finally:
            connection.close()
        return iter(result)

    benchmark(
        "mapPartitions function",
        lambda: df.rdd.mapPartitions(map_partition).toDF().show(10),
    )


if __name__ == "__main__":
    main()
