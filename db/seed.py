from azure.cosmos import CosmosClient
import json
from os import environ

cosmosdb_connection_string = environ.get("COSMOSDB_CONNECTION_STRING")[0]
database_name = environ.get("COSMOSDB_DATABASE_NAME")
container_name = environ.get("COSMOSDB_CONTAINER_NAME")

def seed_data(client, data):
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)

    for item in data:
        container.upsert_item(item)

if __name__ == "__main__":
    with open("seed_data.json", "r") as file:
        seeding_data = json.load(file)

    connection_settings = {k: v for k, v in (part.split('=', 1) for part in cosmosdb_connection_string.split(';'))}

    client = CosmosClient.from_connection_string(connection_settings)

    #client = CosmosClient.from_connection_string(conn_str=cosmosdb_connection_string)

    seed_data(client, seeding_data)

    print("Data seeding completed.")
