#Import all the libraries need it to manage json, boto3 to get dynamodb resource and datime functions
import json
from boto3 import resource
from datetime import datetime, timezone

#Constant to create the DynamoDB resource and specify the table name/
#This can be change it to use environment variables
_LAMBDA_DYNAMO_RESOURCE = {"resource" : resource("dynamodb"),
                           "table_name" : "SLAErrors"}

#Class to init the creation of the Dynamodb tables by using getting as parameter the configuration as we have
#in the constant variable, for test purpose it helps to create it from moto
class LambdaDynamoDB:
    def __init__(self, lambda_dynamodb_resource):
        self.resource = lambda_dynamodb_resource["resource"]
        self.table_name = lambda_dynamodb_resource["table_name"]
        self.table = self.resource.Table(self.table_name)
        

#This is the lambda_handler that will get the event as HTTP Request where we can get from the body the json request
#This method will create the LambdaDynamoDB class and call the save_data method
def lambda_handler(event, context) :
    
    global _LAMBDA_DYNAMO_RESOURCE
    
    dynamo_resource_class = LambdaDynamoDB(_LAMBDA_DYNAMO_RESOURCE)
    
    return save_data(
        event, dynamo_resource_class
    )

#This method will get the DynamoDB with the table or the mock from moto and save the data with the SLA folders and files    
def save_data(event, dynamo_db_table : LambdaDynamoDB) :   
    try:
        print("Starting execution")
        dynamo_db = dynamo_db_table.table
        body = json.loads(event['body'])
        sla_errors = body['sla_error']

        for error in sla_errors:
            folder = error['folder']
            sla = error['sla']
            files = error['files']

            for file in files:
                dynamo_db.put_item(
                    Item={
                        'folder': folder,
                        'filename': file['filename'],
                        'creationDate': file['creationDate'],
                        'sla': sla,
                        'processedAt': datetime.now(timezone.utc).isoformat()
                    }
                )
        print("Execution succeeded")
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Data processed successfully"})
        }
    except KeyError as ke:
        print(ke)
        return {
            "statusCode" : 400,
            "body": json.dumps({"message": str(ke)})
        }
    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            "body": json.dumps({"message": str(e)})
        }
