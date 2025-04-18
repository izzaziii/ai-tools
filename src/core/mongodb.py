from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pymongo.collection import Collection
from pymongo.database import Database
import pandas as pd
import warnings
import json

warnings.filterwarnings("ignore", category=DeprecationWarning)


class Mongo:
    def __init__(self, database_name: str, collection_name: str) -> None:
        """
        Initialize the MongoDB client.
        """
        self.client: MongoClient = MongoClient()
        self.database: Database = self.client[database_name]
        self.collection: Collection = self.database[collection_name]

    def _delete_records(self, filter: dict = {}) -> None:
        """
        Delete records from the collection based on the filter.
        """
        try:
            result = self.collection.delete_many(filter)
            print(f"Deleted {result.deleted_count} records.")
        except ConnectionFailure as e:
            print(f"Could not connect to MongoDB: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def _insert_records(self, data: dict) -> None:
        """
        Insert records into the collection.
        """
        try:
            result = self.collection.insert_many(data)
            print(f"Inserted {len(result.inserted_ids)} records.")
        except ConnectionFailure as e:
            print(f"Could not connect to MongoDB: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    @staticmethod
    def transform_dataframe(dataframe: pd.DataFrame):
        """
        Transform the dataframe to a list of dictionaries for insertion to MongoDB.
        """
        json_dict = json.loads(dataframe.to_json(orient="records"))
        return json_dict

    def replace_data(self, data: pd.DataFrame) -> None:
        """
        Replace data in the collection.
        """
        try:
            self._delete_records()
            self._insert_records(Mongo.transform_dataframe(data))
        except ConnectionFailure as e:
            print(f"Could not connect to MongoDB: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def get_data(self, pipeline: list = []) -> pd.DataFrame:
        """
        Get data from the collection based on the filter.
        """
        try:
            cursor = self.collection.aggregate(pipeline)
            data = pd.DataFrame(cursor)
            return data
        except ConnectionFailure as e:
            print(f"Could not connect to MongoDB: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def get_data_json(self, pipeline: list = []) -> str:
        """
        Get data from the collection based on the filter and return it as a JSON string
        suitable for OpenAI API consumption.

        Args:
            pipeline: MongoDB aggregation pipeline

        Returns:
            JSON string representation of the data
        """
        try:
            cursor = self.collection.aggregate(pipeline)
            data = list(cursor)

            # Remove MongoDB ObjectId fields which aren't JSON serializable
            for doc in data:
                if "_id" in doc and not isinstance(doc["_id"], (str, int, float, bool)):
                    doc["_id"] = str(doc["_id"])

            # Convert to JSON string
            json_data = json.dumps(data, ensure_ascii=False, default=str)
            return json_data
        except ConnectionFailure as e:
            print(f"Could not connect to MongoDB: {e}")
            return json.dumps({"error": f"Connection failure: {str(e)}"})
        except Exception as e:
            print(f"An error occurred: {e}")
            return json.dumps({"error": str(e)})
