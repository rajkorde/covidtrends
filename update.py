import json
import datetime
from dateutil import parser
import requests

from constants import CONFIRMED_URL, RECOVERD_URL, DEATH_URL


def update_data():

    today = datetime.date.today()

    with open('update.json') as f:
        d = json.load(f)

    lu_date = parser.parse(d['last_updated']).date()

    if lu_date < today:

        failed = False
        try:
            confirmed = requests.get(CONFIRMED_URL)
            open('confirmed.csv', 'wb').write(confirmed.content)
        except Exception:
            failed = True
            print('Downloading confirmed file failed')
        else:
            print("Confirmed file downloaded")

        try:
            recovered = requests.get(RECOVERD_URL)
            open('recovered.csv', 'wb').write(recovered.content)
        except Exception:
            failed = True
            print('Downloading recovered file failed')
        else:
            print("Recovered file downloaded")

        try:
            death = requests.get(DEATH_URL)
            open('death.csv', 'wb').write(death.content)
        except Exception:
            failed = True
            print('Downloading death file failed')
        else:
            print("Death file downloaded")

        if failed is False:
            d['last_updated'] = str(today)
            with open('update.json', 'w') as f:
                json.dump(d, f)

    else:
        print('files are already up-to-date')
