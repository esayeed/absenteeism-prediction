#!/bin/bash
set -e

function help () {
    echo
    echo "Usage: $0 <command>"
    echo
    echo "Available commands:"
    echo "  predict_outputs - Predict outputs for a given input file using a trained model"
    echo "  run_notebook - Run Jupyter notebook server"
    echo "  train_model - Train a model using a given input file and save it for later use"
}

if [ $# -lt 1 ]; then
    help
    exit 1
fi

case $1 in
    predict_outputs)
        python3 -m absenteeism.scripts.predict_outputs $2
        ;;
    train_model)
        python3 -m absenteeism.scripts.train_model $2
        ;;
    run_notebook)
        jupyter lab notebooks/absenteeism_analysis.ipynb \
          --port=8888 \
          --no-browser \
          --ip=0.0.0.0 \
          --allow-root \
          --NotebookApp.token='' \
          --NotebookApp.password=''
        ;;
    *)
        echo "Invalid command: $1"
        help
        exit 1
        ;;
esac