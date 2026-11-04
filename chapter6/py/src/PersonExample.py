from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType


def main():
    spark = SparkSession.builder.appName("Person").getOrCreate()

    # Python does not have Java beans/Encoders. Use an explicit schema instead.
    person_schema = StructType([
        StructField("uname", StringType(), True),
        StructField("age", IntegerType(), True),
    ])

    person_list = [("Jules Damji", 60)]
    person_df = spark.createDataFrame(person_list, person_schema)

    print("*** here is the schema inferred from the bean")
    person_df.printSchema()
    person_df.show()

    # Equivalent of Dataset<String> created from a list of strings.
    string_data = ["hello", "world"]
    string_df = spark.createDataFrame([(value,) for value in string_data], ["value"])
    string_df.show()


if __name__ == "__main__":
    main()
