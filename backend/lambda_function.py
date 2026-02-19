from mangum import Mangum
from backend.main import app

mangum_handler = Mangum(app)

def handler(event, context):
    if event.get("warm"):
        return {"statusCode": 200, "body": "warm"}
    return mangum_handler(event, context)