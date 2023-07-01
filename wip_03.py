from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Connect to MongoDB
load_dotenv()
DB_URL = os.getenv("DB_URL")
client = MongoClient(DB_URL)
db = client["test_db"]
collection = db["test_col"]

# Specify the field to check for duplicates
field_to_check = 'link'  # Replace 'your_field' with the actual field name

# Count duplicates
pipeline = [
    {'$group': {'_id': '$' + field_to_check, 'count': {'$sum': 1}}},
    {'$match': {'count': {'$gt': 1}}}
]
result = collection.aggregate(pipeline)

# Output the number of duplicates
num_duplicates = sum(1 for _ in result)
print(f"Number of duplicates in '{field_to_check}': {num_duplicates}")

# Disconnect from MongoDB
client.close()
