import os;
from dotenv import load_dotenv;

load_dotenv();

import client;

with open('user.xml', 'r') as file:
	user_p = file.read()
 
system_p = os.getenv('SYSTEM_PROMPT');

print(user_p.replace('$words', 'abandon ability able').replace('$idStarts', '1001'));

dsclient = client.DeepSeekClient();
print(dsclient.generate_query(system_p, user_p.replace('$words', 'abandon ability able').replace('$idStarts', '1001')).choices[0].message.content);