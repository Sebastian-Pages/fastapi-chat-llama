# FastAPI Llama Chat

API using Vicuna LLM to generate text in a game.

## Table of Contents

-   [Introduction](#introduction)
-   [Features](#features)
-   [Installation](#installation)
-   [Usage](#usage)
-   [API Documentation](#api-documentation)
-   [Contributing](#contributing)
-   [License](#license)

## Introduction

This project is a game that utilizes a local language model (LLM) to generate text-based content. It is designed to work in conjunction with a React app, providing an interactive and dynamic gaming experience. The game is built using FastAPI, a modern, fast (high-performance), web framework for building APIs with Python.

The React app serves as the frontend interface for the game, allowing players to interact with the game world, participate in campaigns, and engage in chat-based gameplay. The local language model (LLM) is responsible for generating text-based prompts and responses, providing dynamic storytelling and decision-making elements to the game.

## Features

-   User authentication and authorization
-   CRUD operations for campaigns and users
-   Chat functionality for interacting with campaigns

## Installation

To install and run the project locally, follow these steps:

1. Clone the repository:

```shell
git clone https://github.com/your-username/project-name.git
```

2. Install the dependencies:

```shell
cd project-name
pip install -r requirements.txt
```

3. Set up the environment variables:
   Create a .env file in the root directory of the project.
   Add the following variables to the .env file and provide appropriate values using `example_config`.

4. Run the FastAPI app:

```shell
uvicorn main:app --reload
```

The app will be available at http://localhost:8000.

## Usage

To use the project, follow these steps:

Start the FastAPI app as described in the installation steps.
Open the React app in your web browser.
The React app should be available at http://localhost:3000 by default.
Follow the instructions provided in the React app to create an account, join campaigns, and interact with the game world.
Enjoy the game!
API Documentation

When running the FastAPI app, the API documentation will be available at http://localhost:8000/docs. It provides detailed information about each API endpoint, including request and response formats, authentication requirements, and other relevant details.

## License

This project is licensed under the MIT License.
