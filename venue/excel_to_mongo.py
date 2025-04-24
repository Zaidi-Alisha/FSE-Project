import pandas as pd
from pymongo import MongoClient

# Step 1: Load the Excel file
file_path = 'updated_banquet_list.xlsx'  # Make sure this file is in the same directory or provide full path
df = pd.read_excel(file_path)

# Step 2: Drop unwanted columns
columns_to_drop = ['Contact Number', 'Image URL']
df = df.drop(columns=[col for col in columns_to_drop if col in df.columns])

# Step 3: Convert DataFrame to list of dictionaries
banquet_records = df.to_dict(orient='records')

# Step 4: Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')  # Adjust the URI if needed
db = client['venue_booking']
banquets_collection = db['banquets']

# Optional: Clear existing data if you want a fresh start
banquets_collection.delete_many({})

# Step 5: Insert records
banquets_collection.insert_many(banquet_records)

print(f"Inserted {len(banquet_records)} banquet records into MongoDB.")
