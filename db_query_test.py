import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import dotenv
from bson.objectid import ObjectId

# Load the .env file
dotenv.load_dotenv()

uri = os.environ.get("MONGO_URI")

# Create a new client and connect to the server
client = MongoClient(uri)

db = client.ghost_db

chat_history = db.chat_history

#query by id
query = {"_id": ObjectId("650a02b4d99a4c2de04c0da0")}

results = chat_history.find_one(query)
pprint.pprint(results)

client.close()
