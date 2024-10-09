#!/usr/bin/env bash

export CONDA_PATH=/opt/conda/bin/conda
eval "$($CONDA_PATH shell.bash hook)"

echo "[II] activate mhai-web"
conda activate mhai-web
