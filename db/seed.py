from azure.cosmos import CosmosClient
import json
from os import environ

# Replace these values with your Cosmos DB connection details
cosmosdb_connection_string = environ.get("COSMOSDB_CONNECTION_STRING")
database_name = environ.get("COSMOSDB_DB_NAME")
container_name = environ.get("COSMOSDB_DB_CONTAINER_NAME")

def seed_data(client, data):
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)

    for item in data:
        container.upsert_item(item)

if __name__ == "__main__":
    with open("seed_data.json", "r") as file:
        seeding_data = json.load(file)

    client = CosmosClient.from_connection_string(cosmosdb_connection_string)

    seed_data(client, seeding_data)

    print("Data seeding completed.")
