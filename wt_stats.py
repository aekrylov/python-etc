import os
import shelve
import time

import requests
from dotenv import load_dotenv

load_dotenv()

db = shelve.open('data/wt_stats', writeback=True)

if 'stats' not in db:
    db['stats'] = {}


if __name__ == '__main__':
    try:
        while True:
            stats = requests.get('https://wt.social/api/getuserstats', {
                '_token': os.getenv('WT_TOKEN'),
                'requester': 'https://wt.social/u/anton-krylov'
            }).json()[0]

            del stats['following']
            del stats['friends']
            del stats['isfollowing']

            db['stats'][int(time.time())] = stats
            db.sync()

            time.sleep(60)

    except KeyboardInterrupt:
        db.close()
