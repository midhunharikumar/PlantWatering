build:
	docker build -f Dockerfile -t streamlit .
	docker tag streamlit:latest midhunharikumar/plant-watering:latest
push:
	docker push midhunharikumar/plant-watering:latest
process:
	docker-compose pull
	docker-compose up -d
stop:
	docker-compose down
