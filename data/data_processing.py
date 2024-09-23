# import pandas, if you dont have this you should "pip install pandas"
import pandas as pd

# Load CSV file you found from kaggle and skip corrupted lines (i.e. bad data)
df = pd.read_csv("ratings.csv.gz", compression="gzip", on_bad_lines="skip")

## If the data you have isnt zipped you could do this
# df = pd.read_csv('ratings.csv', on_bad_lines='skip')

## Display the loaded DataFrame with some sample methods
# The empty print() statement are for empty line spacing
print(df.head(5))
print()
print(df.tail(5))
print()
print(df.info)
print()
print(df.shape)
