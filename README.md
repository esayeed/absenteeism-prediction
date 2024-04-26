# Absenteeism Prediction Modeling

## Overview
This project is designed to predict absenteeism in a company based on various factors such as the reason for absence, the number of hours of absence, and the distance from the company. The project uses a machine learning model to predict absenteeism and provides a command line utility that can be run using a Docker container to train the model and predict absenteeism based on input data.

This project also includes the Jupyter Notebook that was used to analyze the data and build the initial machine learning model. The notebook can also be run interactively through a Docker container. The instructions on how to do that are detailed below.

## Prerequisites
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Python 3.9](https://www.python.org/downloads/)

## Project Structure
```
root/
├─ absenteeism/
│  ├─ dataprep/
│  │  ├─ <data preprocessing modules>
│  ├─ ml/
│  │  ├─ <machine learning modules>
│  ├─ scripts/
│  │  ├─ <command line utilities modules>
├─ data/
│  ├─ absenteeism_input_data.csv
│  ├─ absenteeism_training_data.csv
├─ notebooks/
│  ├─ absenteeism_analysis.ipynb
├─ output/
│  ├─ <generated output files>
```

## Running the Project

### Clone the repository
```bash
git clone https://github.com/esayeed/absenteeism-prediction.git
```
### Navigate to the project directory
```bash
cd absenteeism-prediction
```

### Build and Run the Docker Container
```bash
docker compose up --build -d
```

### View the Notebook
Open the following link in your browser to access the Jupyter Notebook:
http://localhost:8888/lab/tree/absenteeism_analysis.ipynb

### Train the Model
Run the following command to train the model using a CSV file containing the training data included with the project:
```bash
docker compose run app train_model data/absenteeism_training_data.csv
```

### Predict Absenteeism
Run the following command to predict absenteeism using a CSV file containing the test data included with the project:
```bash
docker compose run app predict_outputs data/absenteeism_input_data.csv
```
The output of the command will be saved in the `output/` directory in a file named `absenteeism_predictions.csv`.

### Shutting Down the Container
Run the following command to stop the container:
```bash
docker-compose down
```
