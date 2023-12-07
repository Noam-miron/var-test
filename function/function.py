import azure.functions as func
from flask import Flask, request, jsonify
from azure.cosmos import CosmosClient
import datetime

app = Flask(__name__)

# Replace these values with your Cosmos DB connection details
endpoint = 'your_cosmos_db_endpoint'
key = 'your_cosmos_db_key'
database_name = 'your_database_name'
log_collection_name = 'log_collection'
query_collection_name = 'query_collection'

# Initialize Cosmos DB client
client = CosmosClient(endpoint, key)
database = client.get_database_client(database_name)
log_container = database.get_container_client(log_collection_name)
query_container = database.get_container_client(query_collection_name)

@app.route('/search', methods=['POST'])
def search(req: func.HttpRequest):
    try:
        data = request.get_json()

        # Log the query and query time to Cosmos DB
        log_entry = {
            'query': data,
            'query_time': str(datetime.datetime.utcnow())
        }
        log_container.upsert_item(log_entry)

        # Perform the query on another collection
        # Replace this query logic with your actual query
        query_result = query_container.query_items(
            query='SELECT * FROM c WHERE c.name = @name',
            parameters=[
                dict(name='@name', value=data['name'])
            ]
        )

        # Extract and format the result
        result = [item for item in query_result]

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)})

func_app = func.FlaskFunction(app)

# Azure Functions HTTP trigger
def main(req: func.HttpRequest) -> func.HttpResponse:
    return func_app(req)
