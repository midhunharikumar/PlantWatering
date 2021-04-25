build:
	docker build -f Dockerfile -t streamlit .
process:
	docker-compose up -d
stop:
	docker-compose down