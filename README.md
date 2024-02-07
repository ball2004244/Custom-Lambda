# Custom Lambda

This repo aimed to build an alternative version for AWS Lambda Hosting. It is a simple and lightweight serverless framework that allows you to run your code without provisioning or managing servers. It is a great way to build serverless applications and microservices.

## Description

This project replicates the Hosting of AWS Lambda with Python and FastAPI, using Docker compose to run the application.

## Features:

- Supports serverless functions in Python
- Run all functions locally
- Allows user to deploy new function while not interrupting the existing ones
- Allows install new dependencies without rebuilding the image

## Installation

1. Docker
   To run the application, you need to have Docker and Docker Compose installed on your machine. You can install Docker from [here](https://docs.docker.com/get-docker/).

Then, you can run the following command to build and run the application:

```bash
docker-compose up --build -d
```

2. Pure Python
   You can also run the application without Docker. You need to have Python 3.8 or later installed on your machine. Then, you can run the following command to install the dependencies and run the application:

```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

## Usage

You can call bash script from test directory to test the application.
