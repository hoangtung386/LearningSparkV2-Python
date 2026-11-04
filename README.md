# Learning Spark 2nd Edition

Repository: https://github.com/hoangtung386/LearningSparkV2-Python

This repository is a fork of the original project
[https://github.com/databricks/LearningSparkV2](https://github.com/databricks/LearningSparkV2).
Its purpose is to convert the entire codebase to Python, so readers of the book
who primarily use Python can understand and run all of the examples in the book.

Welcome to the GitHub repo for Learning Spark 2nd Edition.

Chapters [2](chapter2/README.md), [3](chapter3/README.md), [6](chapter6/README.md), and [7](chapter7/README.md) contain stand-alone Spark applications. The preferred implementations are now Python/PySpark and can be run with `spark-submit` as described in each chapter's README.

Legacy Scala and Java examples are retained for reference under their respective `scala/` and `java/` directories. The old JAR build script, `build_jars.py`, is also retained for those legacy examples.

For all the other chapters, we have provided notebooks in the [notebooks](notebooks) folder. We have also included notebook equivalents for a few of the stand-alone Spark applications in the aforementioned chapters.

Have Fun, Cheers!
