# Custom Lambda

This repo aimed to build an alternative version for AWS Lambda Hosting. It is a simple and lightweight serverless framework that allows you to run your code without provisioning or managing servers. It is a great way to build serverless applications and microservices.

## Description

This project replicates the Hosting of AWS Lambda with Python and FastAPI. For more information about AWS Lambda, you can visit [here](https://aws.amazon.com/lambda/).

## Features:

- Supports serverless functions in Python
- Run all functions locally
- Allows user to deploy new function while not interrupting the existing ones
- Allows install new dependencies without rebuilding the image

## Installation

Before starting, you need to copy the `.env.example` file to `.env` and fill in the required environment variables.

```bash
cp .env.example .env
```

1. Docker
   
   To run the application, you need to have Docker and installed on your machine. You can install Docker from [here](https://docs.docker.com/get-docker/).

```bash
docker build -t custom-lambda .
docker run -d -p 9999:9999 custom-lambda
```

2. Docker Compose
   
   You can install Docker Compose from [here](https://docs.docker.com/compose/install/).
   Then, you can run the following command to build and run the application:

```bash
docker-compose up --build -d
```

2. Pure Python
   
   You can also run the application without Docker. You need to have Python 3.8 or later installed on your machine. Then, you can run the following command to install the dependencies and run the application:

```bash
pip install -r requirements.txt
uvicorn app:app --reload --host 127.0.0.1 --port 9999
```

## Usage

You can call bash script from test directory to test the application.

Visit http://localhost:9999/docs to see the API documentation.

## Roadmap

v1.0.0:

- Allow user to CREATE invokee function in Python
- Uers can EXECUTE the function
- Users can GET all functions, GET a function by its name
- Users can MODIFY existing functions and DELETE a function
- Functions is stored distributedly in the file system
- Added logging for each function

v1.0.1 (Upcoming):

- Allow in-app package installation (through pip)
- Add Timeout and Memory Limit for each function
- Limit file size for each function
- Add simple UI for the application

v1.0.2 (Upcoming):

- Separate function uploading and function executing channels
- Separate dependency for each function
- Add support for other languages
