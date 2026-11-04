# Learning Spark, 2nd Edition — Python Edition

> **Repository:** [hoangtung386/LearningSparkV2-Python](https://github.com/hoangtung386/LearningSparkV2-Python)  
> **Forked from:** [databricks/LearningSparkV2](https://github.com/databricks/LearningSparkV2)

This fork converts the book's stand-alone examples to **Python / PySpark** so readers who
primarily use Python can read, understand, and run every example without switching to
Scala or Java. Legacy Scala and Java sources are kept for reference.

---

## Table of Contents

- [Overview](#overview)
- [Learning Path](#learning-path)
- [Repository Structure](#repository-structure)
- [Prerequisites](#prerequisites)
- [How to Run](#how-to-run)
- [Legacy Examples](#legacy-examples)

---

## Overview

| Chapter | Topic | Python examples |
|---|---|---|
| 2 | First Spark application, DataFrame aggregations | ✅ |
| 3 | Schemas, Rows, columns, expressions | ✅ |
| 6 | Dataset/DataFrame transformations | ✅ |
| 7 | Configuration, partitions, caching, joins | ✅ |
| MLflow project | Random forest pipeline with MLflow | ✅ (already Python) |
| Other chapters | Notebooks (Databricks) | ✅ in `notebooks/` |

---

## Learning Path

Follow the files below in order. Each step builds on the previous one.

### 1. Chapter 2 — Your first Spark application

Start here to learn how to create a `SparkSession`, read CSV data, and aggregate.

- `chapter2/py/src/gen_mnm_dataset.py` — generate sample M&M data
- `chapter2/py/src/mnmcount.py` — read CSV, group, aggregate, filter
- `chapter2/py/src/test_agg.py` — simpler aggregation variant

### 2. Chapter 3 — Schemas and DataFrames

Learn how to define schemas, create DataFrames from Python data, and use expressions.

- `chapter3/py/src/rows.py` — `Row` and explicit `StructType`
- `chapter3/py/src/Example-3_6.py` — columns, expressions, `withColumn`

### 3. Chapter 6 — Transformations and typed data

Understand how DataFrame transformations replace Scala/Java typed `Dataset` APIs.

- `chapter6/py/src/PersonExample.py` — explicit schema instead of Java beans
- `chapter6/py/src/Example6_3.py` — filter, map, and derived columns

### 4. Chapter 7 — Performance and execution

Explore Spark configuration, partitions, caching, and join strategies.

- `chapter7/py/src/SparkConfig_7_1.py` — inspect and change Spark config
- `chapter7/py/src/Partitions_7_2.py` — repartitioning
- `chapter7/py/src/MapAndMapPartitions_7_3.py` — `map` vs `mapPartitions`
- `chapter7/py/src/CachingData_7_5.py` — cache, persist, temp views
- `chapter7/py/src/SortMergeJoin_7_6.py` — sort-merge join
- `chapter7/py/src/SortMergeJoinBucketed_7_6.py` — bucketed join

### 5. MLflow project

Train and track a random forest model with MLflow and Spark ML.

- `mlflow-project-example/train.py`
- `mlflow-project-example/MLproject`
- `mlflow-project-example/conda.yaml`

### 6. Notebooks (advanced topics)

Open `notebooks/LearningSparkv2.dbc` in Databricks for the remaining chapters,
including ML and streaming examples.

---

## Repository Structure

```text
.
├── chapter2/
│   ├── py/src/          # Python examples
│   └── scala/           # Legacy Scala examples
├── chapter3/
│   ├── py/src/
│   └── scala/
├── chapter6/
│   ├── py/src/          # Python examples (converted from Java)
│   └── java/            # Legacy Java examples
├── chapter7/
│   ├── py/src/          # Python examples (converted from Scala)
│   └── scala/
├── mlflow-project-example/
├── notebooks/
├── databricks-datasets/
├── run_python_examples.py
└── build_jars.py        # Legacy JAR build script
```

---

## Environment Setup (uv)

This project uses `pyproject.toml` and `uv` for dependency management.

Create and activate the virtual environment:

```bash
uv sync
source .venv/bin/activate
```

Run commands through `uv` without activating:

```bash
uv run python run_python_examples.py
uv run spark-submit chapter2/py/src/mnmcount.py
```

## Prerequisites

- Python 3.9–3.11
- Apache Spark 3.x with `spark-submit` on `PATH`
- PySpark matching your Spark version

> Note: this environment was validated only for Python syntax; runtime execution
> requires a working Spark installation.

---

## How to Run

List all Python examples:

```bash
python run_python_examples.py
```

Run a specific chapter:

```bash
python run_python_examples.py --chapter chapter6
```

Run one example directly:

```bash
cd chapter2/py/src
spark-submit mnmcount.py ../../data/mnm_dataset.csv
```

---

## Legacy Examples

The original Scala and Java examples remain under:

- `chapter2/scala/`
- `chapter3/scala/`
- `chapter6/java/`
- `chapter7/scala/`

They are retained for reference. `build_jars.py` is also kept for those legacy
examples, but the Python examples are the recommended implementation for this
repository.
