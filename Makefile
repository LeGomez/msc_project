include .env
export

PIP_VERSION=22.0.4

venv:
	python3 -m venv .venv

reqs:
	. ./venv/bin/activate && \
	pip install pip==${PIP_VERSION} && \
	pip install -r ./app/requirements.txt

sentiment_analysis:
	. ./venv/bin/activate && \
	python sentiment_analysis.py

twitter_data:
	. ./venv/bin/activate && \
	python twitter_extract/lambda_function.py

data:
	. ./venv/bin/activate && \
	python generate_data/generate_data.py

load_data:
	. ./venv/bin/activate && \
	python rds_load/lambda_function.py