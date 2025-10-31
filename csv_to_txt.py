import pandas as pd
""" 
Using the export chrome history addon. All history is saved to a csv file with the 
6th element being the link. This program parses such a csv file to a txt file. Each link on a new row. 
It then cleans the txt file from all empty lines and "" lines.
"""

df = pd.read_csv("history.csv", header=1)

links = df.iloc[:, 5] # Selects all rows from column index 5
links.to_csv("History.txt", index=False, header=False) # Writes our pandas series "links", containing all urls, to History.txt

with open("History.txt", "r") as f: # 
    lines = f.readlines() 

filtered = [line for line in lines if line.strip() not in ('""', '')] # Removes all of the empty/meaningless lines

with open("History.txt", "w") as f:
    f.writelines(filtered) # Updates the txt file without unessecary junk