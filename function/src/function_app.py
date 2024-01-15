import azure.functions as func
import logging
import datetime
from os import environ

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="api_function")
# @app.cosmos_db_input(arg_name="documents", 
#                      database_name=environ.get("COSMOSDB_DATABASE_NAME"),
#                      collection_name=environ.get("COSMOSDB_CONTAINER_NAME"),
#                      partition_key="/id",
#                      connection_string_setting="MyAccount_COSMOSDB")
# @app.cosmos_db_output(arg_name="outputDocument",
#                       database_name=environ.get("COSMOSDB_DATABASE_NAME"),
#                       collection_name=environ.get("COSMOSDB_CONTAINER_NAME"),
#                       connection_string_setting=environ.get("COSMOSDB_CONNECTION_STRING"))
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
        'openHour': 9,
        'closeHour': 22,
        'vegetarian': 'yes' if is_veg else 'no',
        'isOpen': 'yes' if 'openHour' <= datetime.datetime.now().hour < 'closeHour' else 'no'
    }
    
    # outputDocument.set(func.Document.from_json(restaurantRecommendation))

    return func.HttpResponse(restaurantRecommendation, status_code=200, mimetype="application/json")
