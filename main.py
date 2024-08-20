import requests
import discord
import math
import random
import pandas
from os import system
system('clear')

# /////////// /////////// ///////////
try:
    response = requests.get('https://cat-fact.herokuapp.com/facts')
    response.raise_for_status()
    if response.ok:
        print(f"Status Code: {response.status_code}")
except requests.exceptions.HTTPError as http_err:
    print(f"HTTP Error occurred: {http_err}")
except Exception as err:
    print(f"Error: {err}")

# /////////// /////////// ///////////
cat_facts_df = pandas.DataFrame(data=response.json())
random_fact_val = random.randint(0, len(cat_facts_df))
print(cat_facts_df['text'][1])