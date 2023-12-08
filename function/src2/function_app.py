import azure.functions as func
import logging
import json
import datetime

#azure-functions in requirements

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

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
