import requests
import os
import json
import sys
import subprocess
import logging
from requests.auth import HTTPBasicAuth
from prettytable import PrettyTable


logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

te_apiURL = 'https://api.thousandeyes.com'
te_apiVersion = 'v6'
te_fullApiURL = f'{te_apiURL}/{te_apiVersion}/'

new_line = '\n'
tab = '\t'

class teApi:
    def __init__(self, username, authToken, accountGroupId=None):
        self.te_user=username
        self.te_authToken=authToken
        self.headers={'Content-Type': 'application/json',
                      'Accept':'application/json'
                      }
        if(accountGroupId is not None):
            self.te_params.update({'aid' : accountGroupId})

    def call(self,method,url,body={}):
        '''
        Function to make GET/POST requests
        '''
        try:
            if method == 'GET':
                response=requests.get(url, auth=HTTPBasicAuth(self.te_user,self.te_authToken),headers=self.headers)
                logging.debug(f'URL: {url} {new_line+tab}GET - {response.status_code}{new_line+tab}Headers: {self.headers}')
            elif method == 'POST':
                response=requests.post(url, auth=HTTPBasicAuth(self.te_user,self.te_authToken),headers=self.headers,json=body)
                logging.debug(f'URL: {url} {new_line+tab}POST - {response.status_code}{new_line+tab}Headers: {self.headers}{new_line+tab}Body: {body}')
            response.raise_for_status()
        except requests.exceptions.RequestException as e:        
            logging.error(e)
            sys.exit(-1)
        return response.json()


    def agents (self):
        api_url = f'{te_fullApiURL}agents.json'
        r = self.call('GET',api_url)
        return r
    def agentDetails (self, agentId): 
        api_url = f'{te_fullApiURL}agents/{agentId}.json'
        r = self.call('GET',api_url)
        return r
    def updateAgent (self, agentId,body): 
        api_url = f'{te_fullApiURL}agents/{agentId}/update.json'
        r = self.call('POST',api_url,body)
        return r

def find_enterprise(query):
    IDs=list()
    for value in query:
        if value['agentType'] != "Cloud":
            IDs.append(value["agentId"])
    return IDs

def compare_target_ip(agents):
    t = PrettyTable(['Id','Name', 'IP','Target_IP'])
    t2 = PrettyTable(['Id','Name', 'IP','Target_IP'])
    t.align = "l"
    t2.align = "l"
    agents_id=[]
    for value in agents:
        agent_details=user.agentDetails(str(value))['agents'][0]
        if agent_details['ipAddresses'][0] != agent_details['targetForTests']:
            t.add_row([agent_details['agentId'],agent_details['agentName'],agent_details['ipAddresses'][0],agent_details['targetForTests']])
            agents_id.append([agent_details['agentId'],agent_details['agentName'],agent_details['ipAddresses'][0],agent_details['targetForTests']])
    if len(json.loads(t.get_json_string()))==1:
        print("No mismatch found in Enterprise agents!")
        sys.exit(0)
    print(f"{'*'*10}Mismatched IPs{'*'*10}")
    print(t)
    ans=answer_prompt("Update all matches? (y/n): ")

    for agent in agents_id:
        if ans == 'n':
            confirm=answer_prompt(f"Update ip of {agent[1]} (y/n): ")
            if confirm != 'n':
                update=user.updateAgent(agent[0],{"targetForTests":agent[2]})['agents'][0]
                t2.add_row([update['agentId'],update['agentName'],update['ipAddresses'][0],update['targetForTests']])
            continue
        else:
            update=user.updateAgent(agent[0],{"targetForTests":agent[2]})['agents'][0]
            t2.add_row([update['agentId'],update['agentName'],update['ipAddresses'][0],update['targetForTests']])

    print(f"{'*'*10}Updated IPs{'*'*10}")
    print(t2)


def answer_prompt(message):
    while True:
        update_all = input(message)
        if update_all.lower() == 'y':
            break
        elif update_all.lower() == 'n':
            break
        else:
            # User entered an invalid input, so prompt again
            print("Invalid input. Please enter 'y' or 'n'.")
    return update_all


if __name__ == '__main__':
    email=f"{subprocess.check_output(['whoami']).decode().strip()}@thousandeyes.com"

    user=teApi(username=email,authToken=os.getenv('TOKEN'))
    agents_id=find_enterprise(user.agents()['agents'])
    compare_target_ip(agents_id)


