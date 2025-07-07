#!/usr/bin/env python3

import pandas as pd
import cudf

# 1M Wikipedia pageview counts
data_url = "https://raw.githubusercontent.com/NVIDIA/accelerated-computing-hub/2186298825b85ef38f08e779af7992b8d762289f/gpu-python-tutorial/data/pageviews_small.csv"

# The semantics we know from Pandas
df_cpu = pd.read_csv(data_url, sep=" ")
print(f"Pandas DataFrame:\n {df_cpu.head()}")

# also exist with CuDF
df_gpu = cudf.read_csv(data_url, sep=" ")
print(f"\nCuDF DataFrame:\n {df_gpu.head()}")

# Label columns & drop unused column
df_gpu.columns = ["project", "page", "requests", "x"]
df_gpu = df_gpu.drop("x", axis=1)

# Count number of English pages
print(f"\n# of English:\n {df_gpu[df_gpu.project == 'en'].count()}")
