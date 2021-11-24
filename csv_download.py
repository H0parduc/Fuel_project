import datetime
import requests
import os


def monday_data():
    td = datetime.date.today()
    current_monday = td + datetime.timedelta(days=-td.weekday(), weeks=0)
    monday = current_monday.strftime("%d%m%y")
    return monday


def url_csv():
    mo = monday_data()
    print(mo)
    url = 'https://assets.publishing.service.gov.uk/' \
          'government/uploads/system/uploads/' \
          'attachment_data/file/1033596/' \
          'CSV_' \
          + mo + \
          '.csv'
    # current
    # https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/
    # 1035134 # changed original was 1033596
    # /CSV_221121.csv

    return url


def download_file():
    # check if file already exists
    mo = monday_data()
    url = url_csv()
    print(mo)
    filename = f'CSV_{mo}.csv'
    print(filename)

    if not os.path.isfile(filename):
        print('Downloading File')
        response = requests.get(url)
        # Check if the response is ok (200)
        if response.status_code == 200:
            # Open file and write the content
            with open(filename, 'wb') as file:
                # A chunk of 128 bytes
                for chunk in response:
                    file.write(chunk)
        else:
            print('File exists')


download_file()
