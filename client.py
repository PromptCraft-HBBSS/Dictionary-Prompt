# Created by Sean L. on May. 18.
# Last Updated by Sean L. on May. 18.
#
# ZKE-DICT Client
# client.py
#
# Makabak1880, 2025. All rights reserved.

import os
import requests
from pymongo import MongoClient
import openai

class DeepSeekClient:
	def __init__(self):
		self.api_key = os.getenv("MODEL_APIKEY")
		self.api_secret = os.getenv("MODEL_APISECRET")
		self.endpoint = os.getenv("MODEL_ENDPOINT")

	def generate_query(self, system_prompt, user_prompt):
		openai.api_key = self.api_secret
		openai.base_url = self.endpoint
  
		response = openai.chat.completions.create(
			model=os.getenv("MODEL_NAME"),
			messages=[
				{"role": "system", "content": system_prompt},
				{"role": "user", "content": user_prompt}
			],
			max_tokens=4096
		)

		return response

class MongoDBClient:
	def __init__(self):
		# Retrieve environment variables
		protocol = os.getenv("MONGODB_PROTOCOL")
		user = os.getenv("MONGODB_USER")
		password = os.getenv("MONGODB_PASSWORD")
		uri = os.getenv("MONGODB_URI")
		queries = os.getenv("MONGODB_QUERIES")
		db_name = os.getenv("MONGODB_DB")

		# Construct the connection string
		connection_string = f"{protocol}://{user}:{password}@{uri}/{queries}"

		# Initialize the MongoDB client and select the database
		self.client = MongoClient(connection_string)
		self.db = self.client[db_name]

	def insert_query(self, collection_name, query):
		# Insert the query into the specified collection
		collection = self.db[collection_name]
		collection.insert_one(query)
