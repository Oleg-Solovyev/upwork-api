import upwork
from pprint import pprint
from upwork.routers import auth
from upwork.routers.jobs import search
import json
from upwork.routers.activities import team
from upwork.routers.reports import time
from urllib.parse import quote
import pandas as pd
import csv


def get_desktop_client():
    """Emulation of a desktop application.
    Your key should be created with the project type "Desktop".
    Returns: ``upwork.Client`` instance ready to work.
    """
    print("Emulating desktop app")
    
    #consumer_key = input('Please enter consumer key: > ')
    #consumer_secret = input('Please enter key secret: > ')
    #config = upwork.Config({'consumer_key': consumer_key, 'consumer_secret': consumer_secret})
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
    
    # For further use you can store ``access_toket`` and
    # ``access_token_secret`` somewhere
    
    return client

if __name__ == '__main__':
    client = get_desktop_client()
    
    try:
        print("My info")
        pprint(auth.Api(client).get_user_info())
        # docs: https://developers.upwork.com/?lang=python#jobs_search-for-jobs
        resp = search.Api(client).find({'q': 'Talend', 'paging':'0;100'})
        #pprint(search.Api(client).find({'q': 'opencart'}))
        
        #jobs = search.Api(client).find({'q': 'kotlin'})
        #pprint(jobs)
        #with open('jobs.txt', 'w') as outfile:
        #    json.dump(jobs, outfile)
        
        # This APP has no access to requested resource    
        #data = team.Api(client).add_activity('mycompany', 'mycompany', {'code': 'team-task-001', 'description': 'Description', 'all_in_company': '1'})
        #pprint(data)
        #with open('data.txt', 'w') as outfile:
        #    json.dump(data, outfile)
        
        #pprint(time.Gds(client).get_by_freelancer_full('oleg-solovyev', {'tq': quote('SELECT task, memo WHERE worked_on >= "2020-05-01" AND worked_on <= "2020-06-01"')}))
        
    except Exception as e:
        print("Catch or log exception details")
        raise e
    
# https://developers.upwork.com/?lang=python#contracts-and-offers_list-freelancers-offers

jobs = resp['jobs']

with open('mycsvfile.csv', 'w') as f:  # You will need 'wb' mode in Python 2.x
    w = csv.DictWriter(f, jobs[1].keys())
    w.writeheader()
    
    for i in range(len(jobs)):
        w.writerow(jobs[i])


#with open('clientCountry.csv', 'w') as f:  # You will need 'wb' mode in Python 2.x
#    for i in range(len(jobs)):
#        f.write(jobs[i]['client']['country'])
#        f.write('\n')

# https://developers.upwork.com/?lang=python#jobs

