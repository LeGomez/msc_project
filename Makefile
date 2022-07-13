include .env
export

sentiment_analysis:
	python sentiment_analysis.py

data:
	python generate_data/generate_data.py