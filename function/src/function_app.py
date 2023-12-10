import azure.functions as func
import logging
import json
import datetime
from azure.cosmos import CosmosClient
from os import environ

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="api_function")
@app.cosmos_db_output(arg_name="outputDocument", database_name=environ.get("COSMOSDB_DATABASE_NAME"), collection_name=environ.get("COSMOSDB_CONTAINER_NAME"), connection_string_setting=environ.get("COSMOSDB_CONNECTION_STRING"))
def api_function(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
  
    req_body = req.get_json()
    name = req_body.get('name', '')
    style = req_body.get('style', '')
    address = req_body.get('address', '')
    is_veg = req_body.get('isVeg', False)
    is_open = req_body.get('isOpen', False)
    
    
    restaurantRecommendation = {
        'name': name,
        'style': style,
        'address': address,
        'openHour': datetime().hour(9),
        'closeHour': datetime().hour(22),
        'vegetarian': 'yes' if is_veg else 'no',
        'isOpen': 'yes' if 'openHour' <= datetime.datetime.utcnow().hour < 'closeHour' else 'no'
        }
    
    outputDocument.set(func.Document.from_json(restaurantRecommendation))
    return func.HttpResponse(restaurantRecommendation, status_code=200, mimetype="application/json")
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
  