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

# Example of iterating over a dataframe using the .iterrows() method.
# This method returns the index of the row and the value of the row.
# The value of the row (in this case) containts 3 values, those are
# 'user_name', 'film_id', and 'rating'. For whatever your CSV holds,
# That will the the values of your row.
for index, row in df.iterrows():
    print(f"index={index} | username = {row['user_name']}")
    print(f"index={index} | film_id = {row['film_id']}")
    print(f"index={index} | rating = {row['rating']}")
    # Break after one interation because I dont want to print forever
    # Normally would not break
    break
