include .env
export

PIP_VERSION=22.0.4

venv:
	python3 -m venv .venv

reqs:
	. ./.venv/bin/activate && \
	pip install pip==${PIP_VERSION} && \
	pip install -r ./app/requirements.txt

sentiment_analysis:
	python sentiment_analysis.py

twitter_data:
	python generate_data/twitter_extract.py

data:
	python generate_data/generate_data.py

load_data:
	python rds_load/lambda_function.py