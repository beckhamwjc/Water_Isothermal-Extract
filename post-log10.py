import os
import glob
import pandas as pd
import numpy as np

# Get all files matching the pattern
files = glob.glob("*-output.dat")

for file in files:
    # Read the file, assuming it's a CSV with headers in the first four rows
    df = pd.read_csv(file, header=None)

    # Extract the headers (first 4 rows)
    headers = df.iloc[:4]

    # Extract the data (from row 5 onward) and apply log10 transformation
    # data = df.iloc[4:].applymap(lambda x: np.log10(float(x)) if pd.notna(x) else x)
    data = df.iloc[4:].map(lambda x: np.log10(float(x)) if pd.notna(x) else x)

    # Combine headers and transformed data
    transformed_df = pd.concat([headers, data], ignore_index=True)

    # Construct new filename
    new_filename = file.replace("-output.dat", "-output-log10.dat")

    # Save to a new file
    transformed_df.to_csv(new_filename, index=False, header=False)

    print(f"Processed and saved: {new_filename}")
