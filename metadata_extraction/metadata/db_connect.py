from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["USER"]
collection = db["metadata"]

# Insert a document
document = {"name": "John Doe", "email": "john.doe@example.com", "age": 30}
collection.insert_one(document)

# Query the inserted document
result = collection.find_one({"name": "John Doe"})
print(result)

# Close the connection
client.close()
