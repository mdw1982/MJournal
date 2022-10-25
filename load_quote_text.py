import time
from random import random

import requests


## function that gets the random quote
def get_random_quote():
    try:
        ## making the get request
        response = requests.get("https://quote-garden.herokuapp.com/api/v3/quotes/random")
        if response.status_code == 200:
            ## extracting the core data
            json_data = response.json()
            data = json_data['data']

            ## getting the quote from the data
            #print(data[0]['quoteText'])
            return data[0]['quoteText']
        else:
            print("Error while getting quote")
    except:
        print("Something went wrong! Try Again!")


#print(get_random_quote())
badcount = 0
with open('quotes.txt', 'w') as file:
    for q in range(100):
        text = get_random_quote()
        if text == "None":
            badcount += 1
            continue
        #print(q)
        file.writelines(text +'\n')
        t = random()
        print(q, f"\tsleep time: {t}")
        time.sleep(t)
print(f"received None {badcount} times")
print("I'm finished!")