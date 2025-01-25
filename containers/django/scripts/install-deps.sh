#!/usr/bin/env bash
set -ex

pushd /opt/services/mhai-web
poetry config virtualenvs.create false

pip install "poetry>=2"

if [[ "$ENV" == "prod" ]]; then
  poetry install --no-root --only main
else
  poetry install --no-root
fi
set +ex
popd
