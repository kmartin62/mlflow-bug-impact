from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from config import MONGO_USER, MONGO_PASSWORD, MONGO_CLUSTER

uri = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@cluster0.thiuk.mongodb.net/?retryWrites=true&w=majority&appName={MONGO_CLUSTER}"

client = MongoClient(uri, server_api=ServerApi('1'))

mongo_db = client["mlflow_db"] # add this to .env or not? TODO: think about this
mongo_collection = mongo_db["model_params"]