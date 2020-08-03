import logging

from settings import brew_db_url, BREWERY_DB_API_KEY
import requests


def run():
    response = requests.get(f"{brew_db_url}/beers", params={'key': BREWERY_DB_API_KEY})
    body = response.json()
    if body['totalResults'] > 0:
        description = 'not found'
        if 'description' in body['data'][0]:
            description = body['data'][0]['description']
        elif 'style' in body['data'][0]:
            description = body['data'][0]['style']['description']
        print(description)
    print('not found')


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()
