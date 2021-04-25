build:
	docker build -f Dockerfile -t streamlit .
	docker tag streamlit:latest midhunharikumar/plant-water:latest
push:
	docker push midhunharikumar/plant-water:latest
process:
	docker-compose up -d
stop:
	docker-compose down