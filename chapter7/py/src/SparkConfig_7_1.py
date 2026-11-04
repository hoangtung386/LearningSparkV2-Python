from pyspark.sql import SparkSession


def print_configs(session):
    # PySpark exposes JVM configuration through SparkContext.getConf().
    for key, value in session.sparkContext.getConf().getAll():
        print(f"{key} -> {value}\n")


def main():
    spark = (
        SparkSession.builder
        .config("spark.sql.shuffle.partitions", 5)
        .config("spark.executor.memory", "2g")
        .master("local[*]")
        .appName("SparkConfig")
        .getOrCreate()
    )

    print_configs(spark)
    print(" ****** Setting Shuffle Partitions to Default Parallelism")
    spark.conf.set("spark.sql.shuffle.partitions", spark.sparkContext.defaultParallelism)
    print_configs(spark)


if __name__ == "__main__":
    main()
