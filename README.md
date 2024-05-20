# Awesome Project: ETL Process for Currency Quotes Data

![Project Status](https://img.shields.io/badge/status-in%20development-yellow) ![License](https://img.shields.io/badge/license-MIT-blue) ![GitHub release (latest by date)](https://img.shields.io/github/v/release/IvanildoBarauna/ETL-awesome-api) ![Python Version](https://img.shields.io/badge/python-3.9-blue) ![GitHub Workflow Status](https://github.com/IvanildoBarauna/ETL-awesome-api/actions/workflows/CI-CD.yaml/badge.svg)

## Project Stack

<img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original.svg" Alt="Python" width="50" height="50"> <img src="https://github.com/devicons/devicon/blob/master/icons/docker/docker-original.svg" Alt="Docker" width="50" height="50"> <img src="https://github.com/devicons/devicon/blob/master/icons/poetry/poetry-original.svg" Alt="Poetry" width="50" height="50"> <img src="https://github.com/devicons/devicon/blob/master/icons/pandas/pandas-original.svg" Alt="Pandas" width="50" height="50"> <img src="https://github.com/devicons/devicon/blob/master/icons/jupyter/jupyter-original.svg" Alt="Jupyter" width="50" height="50"> <img src="https://github.com/devicons/devicon/blob/master/icons/matplotlib/matplotlib-original.svg" Alt="Matplotlib" width="50" height="50"> <img src="https://github.com/devicons/devicon/blob/master/icons/githubactions/githubactions-original.svg" Alt="GitHub Actions" width="50" height="50">

## Project Description

This project, called "Awesome Project: ETL Process for Currency Quotes Data", is a solution dedicated to extracting, transforming, and loading (ETL) currency quote data. It makes a single request to a specific endpoint to obtain quotes for multiple currencies.

The request response is then processed, where each currency quote is separated and stored in individual files in Parquet format. This makes it easier to organize data and efficiently retrieve it for future analysis.

Additionally, the project includes a Jupyter Notebook for data exploration. This notebook is responsible for consolidating all individual Parquet files into a single dataset. From there, the data can be explored and analyzed to gain valuable insights into currency quotes.

In summary, this project provides a complete solution for collecting, processing, and analyzing currency quote data.

## Project Structure

- [`data/`](https://github.com/IvanildoBarauna/ETL-awesome-api/tree/main/data): Stores raw data in Parquet format.
  - ETH-EUR-1713658884.parquet: Example: Raw data for ETH-EUR quotes. file-name = symbol + unix timestamp of extraction
- [`notebooks/`](https://github.com/IvanildoBarauna/ETL-awesome-api/tree/main/notebooks): Contains the `data_explorer.ipynb` notebook for data exploration.
- [`etl/`](https://github.com/IvanildoBarauna/ETL-awesome-api/tree/main/etl): Holds the project source code.
  - [`main.py`](https://github.com/IvanildoBarauna/ETL-awesome-api/blob/main/etl/main.py): The entry point for the ETL Module.
  - [`common/`](https://github.com/IvanildoBarauna/ETL-awesome-api/tree/main/etl/common)
    - [`utils/`](https://github.com/IvanildoBarauna/ETL-awesome-api/tree/main/etl/utils)
      - [`logs.py`](https://github.com/IvanildoBarauna/ETL-awesome-api/blob/main/etl/utils/logs.py): Package for managing logs.
      - [`common.py`](https://github.com/IvanildoBarauna/ETL-awesome-api/blob/main/etl/utils/common.py): Package for common tasks in the code.
      - [`constants.py`](https://github.com/IvanildoBarauna/ETL-awesome-api/blob/main/etl/utils/constants.py): Constants used in the code.
    - [`logs/`](https://github.com/IvanildoBarauna/ETL-awesome-api/tree/main/etl/common/logs): For storage debug logs
  - [`controller/`](https://github.com/IvanildoBarauna/ETL-awesome-api/tree/main/etl/controller): For receive and validate params
    - [`pipeline.py`](https://github.com/IvanildoBarauna/ETL-awesome-api/blob/main/etl/controller/pipeline.py):
  - [`models/`](https://github.com/IvanildoBarauna/ETL-awesome-api/tree/main/etl/models): Receive and transform response
    - [`extract/`](https://github.com/IvanildoBarauna/ETL-awesome-api/tree/main/etl/models/extract): Module for data extraction from API.
      - [`ApiToParquetFile.py`](https://github.com/IvanildoBarauna/ETL-awesome-api/blob/main/etl/models/extract/ApiToParquetFile.py): Extract API data to Parquet File and store in /data.
  - [`views/`](https://github.com/IvanildoBarauna/ETL-awesome-api/tree/main/etl/views): For storage Data Analysis and Visualization

## How to run this project and verify execution time:

<details>
  <summary>Click here:</summary>
  
  ## Step by Step
  1. Clone the repository:
     ```sh
     $ git clone https://github.com/IvanildoBarauna/ETL-awesome-api.git
     ```

2. Create a virtual environment and install dependencies:
   Ensure you have Python 3.9 installed on your system.

   ```sh
   $ cd ETL-awesome-api
   $ python -m venv .venv
   $ source .venv/bin/activate  # On Windows use `venv\Scripts\activate`
   $ .venv/bin/python -m pip install --upgrade pip
   $ echo "SERVER_URL=https://economia.awesomeapi.com.br" > .env # Create enviroment variable for server URL`
   $ pip install -e .
   $ python etl/main.py
   ```

   Learn more about [venv module in python](https://docs.python.org/pt-br/3/library/venv.html)

3. Alternatively, you can run the project using [`Dockerfile`](https://github.com/IvanildoBarauna/ETL-awesome-api/tree/main/Dockerfile) or [`docker-compose`](https://github.com/IvanildoBarauna/ETL-awesome-api/tree/main/docker-compose.yml). To build and run the Docker image, use the following command:

   ```sh
   $ docker build -t etl-awesome-api . && docker run etl-awesome-api
   ```

   To run the project with Docker Compose, use the following command:

   ```sh
   $ docker-compose up --build
   ```

   Learn more about [docker](https://docs.docker.com/)

4. Or you can install and run the project using the dependency manager [`poetry`](https://python-poetry.org/):
`sh
     $ poetry install && poetry run python etl/main.py
     `
</details>

## ETL and Data Analysis Results:

You can see the complete data analysis, the Jupyter Notebook is deployed in [GitHub Pages](https://ivanildobarauna.github.io/ETL-awesome-api/)
