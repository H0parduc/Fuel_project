import datetime
import requests
import os
from bs4 import BeautifulSoup


def monday_data():
    td = datetime.date.today()
    current_monday = td + datetime.timedelta(days=-td.weekday(), weeks=0)
    monday = current_monday.strftime("%d%m%y")
    return monday


def url_csv():
    r = requests.get("https://www.gov.uk/government/statistics/weekly-road-fuel-prices")
    soup = BeautifulSoup(r.content, 'html.parser')
    for a_tag in soup.find_all('a', href=True):
        if a_tag['href'].endswith('.csv'):
            return a_tag['href']


def download_file():
    # check if file already exists
    mo = monday_data()
    url = url_csv()
    filename = f'CSV_{mo}.csv'

    if not os.path.isfile(filename):
        print('Downloading File')
        response = requests.get(url)
        # Check if the response is ok (200)
        print(response.status_code)
        if response.status_code == 200:
            # Open file and write the content
            with open(filename, 'wb') as file:
                # A chunk of 128 bytes
                for chunk in response:
                    file.write(chunk)
    else:
        print('File exists')
