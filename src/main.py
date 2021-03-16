import pandas as pd

if __name__ == "__main__":
    print("Test main entry point.")
    df = pd.read_csv("../data/mfi/mortality/mortality_long.tsv", sep="\t")
    print(df)
