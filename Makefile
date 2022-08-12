include .env
export

sentiment_analysis:
	python sentiment_analysis.py

twitter_data:
	python generate_data/twitter_extract.py

data:
	python generate_data/generate_data.py

load_data:
	python rds_load/lambda_function.py