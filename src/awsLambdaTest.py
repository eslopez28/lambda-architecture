#Import all the unit test and mock dependencies, also we will need boto3 and json to create the resource and request
import unittest
from moto import mock_dynamodb2
from unittest.mock import patch
from boto3 import resource
import json

# Import from awsLambda file the method that save the data and the Class to create the DynamoDB
from awsLambda import save_data, LambdaDynamoDB

#We need that our test mock the dynamodb by using this annotation
@mock_dynamodb2
class TestLambdaFunction(unittest.TestCase):

    #DynamoDB setUp
    def setUp(self):
        # Configure the DynamoDB mock
        dynamodb = resource('dynamodb', region_name='us-east-1')
        table_name = 'SLAErrors'
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {'AttributeName': 'folder', 'KeyType': 'HASH'},
                {'AttributeName': 'filename', 'KeyType': 'RANGE'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'folder', 'AttributeType': 'S'},
                {'AttributeName': 'filename', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        #We will wait until table exist in the mock dynamodb
        table.wait_until_exists()
        
        mocked_dynamo_resource = {"resource" : dynamodb,
                                  "table_name" : table_name}
        
        self.mocked_dynamodb_class = LambdaDynamoDB(mocked_dynamo_resource)

    #This will be the test execution
    def test_lambda_handler(self):
        #We are going to create the event with an example of files and folders with SLA
        event = {
            'body': json.dumps(
                {
                "sla_error": [
                    {
                        "folder": "/usr/document/folderwithSLA2",
                        "sla": 60,
                        "files": [
                            {
                                "filename": "exampleFile6.txt",
                                "creationDate": "2024-06-15T19:25:25"
                            },
                            {
                                "filename": "exampleFile7.txt",
                                "creationDate": "2024-06-15T18:05:25"
                            }
                        ]
                    },
                    {
                        "folder": "/usr/document/folderwithSLA1",
                        "sla": 20,
                        "files": [
                            {
                                "filename": "exampleFile1.txt",
                                "creationDate": "2024-06-15T20:05:25"
                            },
                            {
                                "filename": "exampleFile3.txt",
                                "creationDate": "2024-06-15T19:55:25"
                            }
                        ]
                    },
                    {
                        "folder": "/usr/document/folderwithSLA3",
                        "sla": 90,
                        "files": [
                            {
                                "filename": "exampleFile8.txt",
                                "creationDate": "2024-06-15T18:55:25"
                            },
                            {
                                "filename": "exampleFile11.txt",
                                "creationDate": "2024-06-15T19:00:25"
                            }
                        ]
                    }
                ]
            })
        }
        #We are going to call the method that will save the data from SLA and sending as parameter the Mocked DynamoDB class
        response = save_data(event, self.mocked_dynamodb_class)
        #Check for response code
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('Data processed successfully', response['body'])

        # Verify if the data was successfully save it in the mocked database
        result = self.mocked_dynamodb_class.table.get_item(Key={'folder': '/usr/document/folderwithSLA2', 'filename': 'exampleFile7.txt'})
        self.assertIn('Item', result)
        self.assertEqual(result['Item']['folder'], '/usr/document/folderwithSLA2')
        self.assertEqual(result['Item']['filename'], 'exampleFile7.txt')

if __name__ == '__main__':
    unittest.main()
