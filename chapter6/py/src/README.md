### How to run the Python code for this chapter

To run the Python code for this chapter:

 * `spark-submit PersonExample.py`
 * `spark-submit Example6_3.py`

These examples intentionally use explicit `StructType` schemas instead of Java
beans/Encoders, because PySpark does not provide a typed `Dataset` API for
arbitrary Python classes.

The legacy Java examples remain under `../java` for reference.
