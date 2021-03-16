import os
import sys
import pandas as pd

if __name__ == "__main__":
    print(sys.executable)
    print(sys.version)
    print(sys.version_info)
    print(os.listdir())
    print("Test main entry point.")
    df = pd.read_csv("./data/country_codes.tsv", sep="\t")
    print(df)
