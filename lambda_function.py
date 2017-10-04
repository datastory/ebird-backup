# coding: utf-8
from credentials import login
import requests
from bs4 import BeautifulSoup
import re
import boto3

def lambda_handler(event, context):
    s3 = boto3.resource('s3')

    payload = {
        'username': login['user'],
        'password': login['pass'],
        'execution': 'e1s1'
    }

    p = requests.post('https://secure.birds.cornell.edu/cassso/login?service=https%3A%2F%2Febird.org%2Febird%2Flogin%2Fcas%3Fportal%3Debird', 
                      data=payload, allow_redirects=False
                     )

    headers = {
       'Cookie': 'EBIRD_SESSIONID=' + p.cookies['JSESSIONID'] + '; eBirdLoggedIn=true' 
    }

    #all available lists in ebird
    r = requests.get('http://ebird.org/ebird/eBirdReports?cmd=SubReport&currentRow=1&rowsPerPage=1000000&sortBy=date&order=desc', headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')

    lists = []
    for lst in soup.find_all('a', href=re.compile('ebird/view/checklist')):
        lst_id = lst.get('href').split('/')[-1].split('?')[0]
        if lst_id not in lists:
            lists.append(lst_id)

    # filters out already downloaded lists
    bucket = s3.Bucket(login['bucket'])
    for obj in bucket.objects.filter(Prefix='ebird'):
        name = obj.key.split('/')[1].split('.')[0]
        if name in lists:
            lists.remove(name)

    # downloads and writes lists
    for lst in lists:
        r = requests.get('http://ebird.org/ebird/view/checklist/download?subID=' + lst, headers=headers)
        
        bucket = s3.Object(login['bucket'], 'ebird/' + lst + '.csv')
        bucket.put(Body=r.content)