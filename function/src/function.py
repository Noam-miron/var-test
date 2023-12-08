import azure.functions as func
import json
import datetime
from azure.cosmos import CosmosClient
from os import environ

def main(req: func.HttpRequest) -> func.HttpResponse:

    req_body = req.get_json()
    name = req_body.get('name', '')
    style = req_body.get('style', '')
    address = req_body.get('address', '')
    is_veg = req_body.get('isVeg', False)
    is_open = req_body.get('isOpen', False)

    cosmos_db_connection_string = environ.get("COSMOSDB_CONNECTION_STRING")[0]

    client = CosmosClient.from_connection_string(cosmos_db_connection_string)
    database_name = environ.get("COSMOSDB_DATABASE_NAME")
    container_name = environ.get("COSMOSDB_CONTAINER_NAME")

    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)

    log_entry = {
        'name': name,
        'style': style,
        'address': address,
        'is_veg': is_veg,
        'is_open': is_open,
        'timestamp': str(datetime.datetime.utcnow())
    }

    container.upsert_item(log_entry)

    recommendation = {
        'restaurantRecommendation': {
            'name': 'Pizza hut',
            'style': 'Italian',
            'address': 'wherever street 99, somewhere',
            'openHour': 9,
            'closeHour': 23,
            'vegetarian': 'yes'
        }
    }

    current_hour = datetime.datetime.utcnow().hour
    recommendation['restaurantRecommendation']['isOpen'] = recommendation['restaurantRecommendation']['openHour'] <= current_hour < recommendation['restaurantRecommendation']['closeHour']

    return func.HttpResponse(json.dumps(recommendation), mimetype="application/json")
