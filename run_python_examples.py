"""Helper for running the Python/PySpark examples in this repository.

By default this script only prints the ``spark-submit`` commands. Pass
``--run`` to execute them; Spark must be installed and available on ``PATH``.
"""

import argparse
import os
import subprocess
import sys

EXAMPLES = {
    "chapter2": ["mnmcount.py", "test_agg.py"],
    "chapter3": ["rows.py", "Example-3_6.py"],
    "chapter6": ["PersonExample.py", "Example6_3.py"],
    "chapter7": [
        "SparkConfig_7_1.py",
        "Partitions_7_2.py",
        "MapAndMapPartitions_7_3.py",
        "CachingData_7_5.py",
        "SortMergeJoin_7_6.py",
        "SortMergeJoinBucketed_7_6.py",
    ],
}


def build_commands(root):
    commands = []
    for chapter, files in EXAMPLES.items():
        src_dir = os.path.join(root, chapter, "py", "src")
        for filename in files:
            commands.append((chapter, filename, ["spark-submit", os.path.join(src_dir, filename)]))
    return commands


def main():
    parser = argparse.ArgumentParser(description="Run or list Python Spark examples.")
    parser.add_argument("--run", action="store_true", help="execute the examples")
    parser.add_argument("--chapter", choices=sorted(EXAMPLES), help="limit to one chapter")
    args = parser.parse_args()

    root = os.path.dirname(os.path.abspath(__file__))
    commands = build_commands(root)
    if args.chapter:
        commands = [item for item in commands if item[0] == args.chapter]

    for chapter, filename, command in commands:
        printable = " ".join(command)
        print(f"[{chapter}] {printable}")
        if args.run:
            try:
                subprocess.run(command, check=True)
            except FileNotFoundError:
                print("spark-submit was not found on PATH", file=sys.stderr)
                sys.exit(127)
            except subprocess.CalledProcessError as exc:
                print(f"failed: {filename} ({exc.returncode})", file=sys.stderr)
                sys.exit(exc.returncode)


if __name__ == "__main__":
    main()
