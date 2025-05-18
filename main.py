# Created by Sean L. on May. 18.
# Last Updated by Sean L. on May. 18.
#
# ZKE-DICT - Client
# main.py
#
# Makabak1880, 2025. All rights reserved.

import os
import ast
from rich.console import Console
from rich.prompt import Prompt, Confirm
from dotenv import load_dotenv
from client import DeepSeekClient, MongoDBClient
import argparse
import json

load_dotenv();
console: Console = Console();
api_client: DeepSeekClient = DeepSeekClient();
db_client: MongoDBClient = MongoDBClient();

parser = argparse.ArgumentParser(description="ZKE Dictionary Entry Generator")
parser.add_argument('--start-id', type=int, default=1220, help='Starting ID for entries')
args = parser.parse_args()
index = args.start_id


with open('user.xml', 'r') as file:
	user_p = file.read()

system_p = os.getenv('SYSTEM_PROMPT');

while True:
	while True:
		word_input = Prompt.ask("Enter words to generate their MongoDB insertion queries (comma-separated)")
		words = [w.strip() for w in word_input.split(",") if w.strip()]
		
		if not words:
			console.print("[bold red][ERR!][/bold red] No valid words entered. Please try again.")
			continue
		break

	query = api_client.generate_query(system_p, user_p.replace('$words', ','.join(words)).replace('$idStarts', str(index))).choices[0].message.content
	index += len(words)
	console.print("[bold blue][INFO][/bold blue] ID Now: ", index)
 
	try:
		docs = ast.literal_eval(query)
	except (ValueError, SyntaxError) as e:
		console.print(f"[bold red][ERR!][/bold red] Error parsing query: {e}")
		continue
	if type(docs) != list:
		console.print(f"[bold red]ERR![/bold red] Error parsing query: {query}")
		continue
	for doc in docs:
		console.print(f"\n[bold green][INFO][/bold green] Word:")
		console.print(json.dumps(doc, indent=2, ensure_ascii=False))
		action = Prompt.ask("Choose action", choices=["insert", "skip", "exit"], default="insert")
		
		if action == "insert":
			db_client.insert_query(os.getenv('BACKEND_API_VERSION'), doc)
			console.print(f"[bold green][INFO][/bold green] Inserted {doc['word']} into MongoDB.")
		elif action == "skip":
			console.print(f"[bold yellow][INFO][/bold yellow] Skipped {doc['word']}.")
			continue
		elif action == "exit":
			console.print("[bold blue][INFO][/bold blue] Exiting the program.")
			break
