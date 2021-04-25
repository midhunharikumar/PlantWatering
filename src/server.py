from fastapi import FastAPI, File, UploadFile, Form
import pendulum
import logging
from pydantic import BaseModel
import time
import json
from datetime import datetime
import uuid
import os
import pymongo
import datetime

MONGO_CONTAINER = os.environ['MONGO_CONTAINER']

class MongoConnector:
    #(TODO) refactor all the customer code here

    def __init__(self, clientURL='localhost', base_db_key=None, sub_db_key=None):
        self.client = pymongo.MongoClient(clientURL)
        if base_db_key==None or sub_db_key== None:
            print('Bad db name')
        self.base_database_key = base_db_key  # 'saheli-prime'
        self.sub_database_key = sub_db_key  # 'customer_info'

    def add_item(self, customer):
        print(customer)
        return self.client[self.base_database_key][self.sub_database_key].insert_one(customer)

    def find_item(self, customer):
        db = self.client[self.base_database_key][self.sub_database_key]
        mydoc = db.find(customer)
        for x in mydoc:
            print(x)
        return []

    def delete_item(self, customer):
        db = self.client[self.base_database_key][self.sub_database_key]
        db.delete_many(customer)

    def get_all(self, filter={}):
        db = self.client[self.base_database_key][self.sub_database_key]
        return list(db.find(filter,{"_id":0}))

    def update_item(self, filter_mongo, query):
        db = self.client[self.base_database_key][self.sub_database_key]
        db.update(filter_mongo, {"$set": query})



connector  = MongoConnector(MONGO_CONTAINER, 'jarvis', 'plant_status')


class Item(BaseModel):
    sensor_name:str
    value: float

LOG = logging.getLogger('simple_example')
LOG.setLevel(logging.DEBUG)


app = FastAPI()

@app.get("/showdata/")
async def show_data():
    data = connector.get_all()
    return data


@app.post("/submit_value/")
async def schedulejob(item: Item):
    LOG.info('scheduling a Job')
    time.sleep(0.1)
    connector.add_item({"sensor_name":item.sensor_name,
			"value":item.value,
                        "date":pendulum.now("UTC")})
    return "submitted"
