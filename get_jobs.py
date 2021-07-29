# https://developers.upwork.com


import upwork
from pprint import pprint
from upwork.routers import auth
from upwork.routers.jobs import search
import json
from upwork.routers.activities import team
from upwork.routers.reports import time
from urllib.parse import quote
import pandas as pd
from datetime import date
import csv


# constants
TECH_LIST = ['Talend', 'Informatica', 'Datastage', 'Redshift', 'ODI', 'ETL', 'DWH', 'data warehouse']


def get_desktop_client():
    """Emulation of a desktop application.
    Your key should be created with the project type "Desktop".
    Returns: ``upwork.Client`` instance ready to work.
    """

    config = upwork.Config({'consumer_key': '0be06c2b526776ff48a458afac4b7c22', 'consumer_secret': '96d4284884277b83'})
    """Assign access_token and access_token_secret if they are known
    config = upwork.Config({\
            'consumer_key': 'xxxxxxxxxxx',\
            'consumer_secret': 'xxxxxxxxxxx',\
            'access_token': 'xxxxxxxxxxx',\
            'access_token_secret': 'xxxxxxxxxxx'})
    """
    
    client = upwork.Client(config)
    
    try:
        config.access_token
        config.access_token_secret
    except AttributeError:
        verifier = input(
            'Please enter the verification code you get '
            'following this link:\n{0}\n\n> '.format(
                client.get_authorization_url()))
        
        print('Retrieving keys.... ')
        access_token, access_token_secret = client.get_access_token(verifier)
        print('OK')
    
    return client


if __name__ == '__main__':
    client = get_desktop_client()
    
    try:
        with open(date.today().strftime('%Y-%m-%d') + '.csv', 'w') as f:
            for tech in TECH_LIST:
                resp = search.Api(client).find({'q':tech, 'paging':'0;100', 'days_posted':1})
                jobs = resp['jobs']

                if tech == TECH_LIST[0]:
                    w = csv.DictWriter(f, jobs[0].keys())
                    w.writeheader()

                for i in range(len(jobs)):
                    if 'agency'   in jobs[i]['snippet'].lower()\
                    or 'agencies' in jobs[i]['snippet'].lower():
                        w.writerow(jobs[i])
        
    except Exception as e:
        print("Catch or log exception details")
        raise e
