from pyspark.sql import SparkSession


def print_configs(session):
    for key, value in session.sparkContext.getConf().getAll():
        print(f"{key} -> {value}\n")


def main():
    spark = (
        SparkSession.builder
        .master("local[*]")
        .appName("Partitions")
        .getOrCreate()
    )

    print_configs(spark)

    num_df = spark.range(1000 * 1000 * 1000).repartition(16)
    print(f"****** Number of Partitions in DataFrame: {num_df.rdd.getNumPartitions()}")

    spark.conf.set("spark.sql.shuffle.partitions", spark.sparkContext.defaultParallelism)
    print("****** Setting Shuffle Partitions to Default Parallelism")
    print_configs(spark)


if __name__ == "__main__":
    main()
