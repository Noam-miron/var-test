import azure.functions as func
import logging
import json
import datetime
from azure.cosmos import CosmosClient
from os import environ

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="api_function")
def api_function(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request... YAY!')
  
    req_body = req.get_json()
    name = req_body.get('name', '')
    style = req_body.get('style', '')
    address = req_body.get('address', '')
    is_veg = req_body.get('isVeg', False)
    is_open = req_body.get('isOpen', False)
    
    logging.info(f"parsed request, {req_body}")
    response_body = json.dumps(req_body)

    
    return func.HttpResponse(response_body, status_code=200, mimetype="application/json")
#     cosmos_db_connection_string = environ.get("COSMOSDB_CONNECTION_STRING")[0]

#     client = CosmosClient.from_connection_string(cosmos_db_connection_string)
#     database_name = environ.get("COSMOSDB_DATABASE_NAME")
#     container_name = environ.get("COSMOSDB_CONTAINER_NAME")

#     database = client.get_database_client(database_name)
#     container = database.get_container_client(container_name)

#     log_entry = {
#         'name': name,
#         'style': style,
#         'address': address,
#         'isVeg': is_veg,
#         'isOpen': is_open,
#         'timestamp': str(datetime.datetime.utcnow())
#     }

#     container.upsert_item(log_entry)

#     result = query_cosmos_db(req_body,client,database,container)
    
#     if result:
#         current_hour = datetime.datetime.utcnow().hour
#         json_result = {
#             'restaurantRecommendations': [
#                 {
#                     'name': item['name'],
#                     'style': item['style'],
#                     'address': item['address'],
#                     'openHour': item['openHour'],
#                     'closeHour': item['closeHour'],
#                     'vegetarian': 'yes' if item['vegetarian'] else 'no',
#                     'isOpen': 'yes' if item['openHour'] <= current_hour < item['closeHour'] else 'no'

#                 }
#                 for item in result
#             ]
#         }
#         return func.HttpResponse(json.dumps(json_result), mimetype="application/json")
#     else:
#         return func.HttpResponse("No restaurants found")


# def query_cosmos_db(query_parameters, client, database, container):

#     query = "SELECT * FROM c WHERE "
#     for key, value in query_parameters.items():
#         if isinstance(value, str):
#             query += f'CONTAINS(c.{key}, "{value}") AND '
#         else:
#             query += f'c.{key} = {value} AND '

#     query = query.rstrip("AND ")

#     query_result = container.query_items(query=query, enable_cross_partition_query=True)

#     return list(query_result)
  