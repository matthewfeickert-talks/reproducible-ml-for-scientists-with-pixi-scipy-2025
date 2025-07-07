import pandas as pd
import cudf

data_url = "https://raw.githubusercontent.com/NVIDIA/accelerated-computing-hub/2186298825b85ef38f08e779af7992b8d762289f/gpu-python-tutorial/data/pageviews_small.csv"

# The semantics we know from Pandas
df = pd.read_csv(data_url, sep=" ")
print(f"Pandas DataFrame\n: {df.head()}")

# also exist with CuDF
pageviews = cudf.read_csv(data_url, sep=" ")
print(f"\nCuDF DataFrame\n: {pageviews.head()}")
