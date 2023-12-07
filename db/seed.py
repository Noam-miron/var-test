from azure.cosmos import CosmosClient
import json

# Replace these values with your Cosmos DB connection details
cosmosdb_connection_string = "your_cosmosdb_connection_string"
database_name = "your_database_name"
container_name = "your_container_name"

def seed_data(client, data):
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)

    for item in data:
        container.upsert_item(item)

if __name__ == "__main__":
    with open("your_seeding_data.json", "r") as file:
        seeding_data = json.load(file)

    client = CosmosClient.from_connection_string(cosmosdb_connection_string)

    seed_data(client, seeding_data)

    print("Data seeding completed.")
