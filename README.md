# Software Architecture Project with AWS Lambda and DynamoDB

## Table of Contents

1. [Project Description](#project-description)
2. [Project Structure](#project-structure)
3. [Requirements](#requirements)
4. [Installation](#installation)
5. [Running the Lambda Function Locally](#running-the-lambda-function-locally)
6. [Running the Unit Tests](#running-the-unit-tests)
7. [Additional Notes](#additional-notes)
8. [Contribution](#contribution)
9. [License](#license)

## Project Description

This project consists of a solution that checks if the SLA of a set of folders and files has been triggered, and then sends this information to a REST endpoint. This information will be ingested into a DynamoDB table using an architecture based on AWS Lambda and DynamoDB.

## Project Structure

- `architecture` : Contains the architecture diagram for the lambda process
- `slaFiles.ps1` : Contains the powershell process to get the SLA Files that will be trigger to the Lambda.
- `src/awsLambda.py`: Contains the Lambda function that processes the events and writes to DynamoDB.
- `src/awsLambdaTest.py`: Contains the unit tests for the Lambda function using the `moto` library to mock DynamoDB.
- `requirements.txt`: List of dependencies needed for the project.
- `README.md`: This file, containing instructions on how to set up and run the project.

## Requirements

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Clone this repository to your local machine:
    ```sh
    git clone https://link_to_repository.git
    cd architecture
    ```

2. Create a virtual environment and install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Running the Lambda Function Locally

To test the Lambda function locally, you can execute the `lambda_process.py` script with a test event:

    ```python
        python awsLambda.py event.json
    ```

## Running the Unit Tests
To run the unit tests, make sure you are in the root directory of the project and execute:

    ```python
        python -m unittest awsLambdaTest.py 
    ```
This will run the tests in test_lambda_process.py, using moto to mock DynamoDB.

### Additional Notes

AWS Credentials: You do not need AWS credentials to run the tests, as moto mocks AWS services.
Moto: Moto is a library that allows mocking AWS services for unit testing. This is useful for developing and testing without needing access to the real cloud.

### Contribution
If you wish to contribute to this project, please follow these steps:

Fork the project
Create a new branch (git checkout -b feature/new-feature)
Make your changes and commit them (git commit -am 'Add new feature')
Push your branch (git push origin feature/new-feature)
Create a new Pull Request

## License
This project is licensed.