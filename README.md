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

3. Pure Python

   You can also run the application without Docker. You need to have Python 3.8 or later installed on your machine. Then, you can run the following command to install the dependencies and run the application:

```bash
pip install -r requirements.txt
uvicorn app:app --host 127.0.0.1 --port 9999
```

## Usage

1. **Interact through Frontend**: Open your web browser and navigate to `http://localhost:9999/`. This will take you to the application's frontend where you can interact with its features.

2. **Testing the Application**: We have provided some bash scripts in `test` directory that you can use to test the application. Run the following command to test the application:

```bash
bash test/get_all.sh
```


3. **API Documentation**: To understand the application's API endpoints and their usage, visit `http://localhost:9999/docs`. This page provides comprehensive documentation for the API.

## Roadmap

v1.0.1 (Released)

- In-app package installation (through pip)
- Add Timeout and Memory Limit for each function
- Limit upload file size
- Add simple UI for the application

v1.0.2 (Upcoming)

- Separate function uploading and executing channels
- Separate dependencies for each function
- Separate functions between users, allow same function name for different users

v1.0.3 (Upcoming)

- Support other languages
- Restrict users' access to system level commands
- Add rate limit

Visit [CHANGELOG.md](CHANGELOG.md) to see full update history.

## Contributing

How to contribute to the project?

1. Fork the project
2. Create your feature branch: `git checkout -b feature/AmazingFeature`
3. Commit your changes: `git commit -m 'Add some AmazingFeature'`
4. Push to the branch: `git push origin feature/AmazingFeature`
5. Open a pull request

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more details.
