# Created by Sean L. on May. 18.
# Last Updated by Sean L. on May. 18.
#
# ZKE-DICT Client
# client.py
#
# Makabak1880, 2025. All rights reserved.

import os
import requests
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