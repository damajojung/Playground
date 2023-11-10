import time
from bs4 import BeautifulSoup
import requests
import os

# Define the name of the folder you want to create
folder_name = "job_openings"

# Check if the folder exists, and create it if it doesn't
if not os.path.exists(folder_name):
    os.makedirs(folder_name)


def find_jobs():   
    html_text = requests.get('https://data-jobs.ch/search?terms=Data+Scientist').text

    soup = BeautifulSoup(html_text, 'lxml')
    job_list = soup.find_all('ul', class_ = 'resultlist')
    for job in job_list:
        jobs = job.find_all('li', class_ = 'item')
        for idx, j in enumerate(jobs):
            try:
                title = j.find('a', class_ = 'title').text.replace('\n', '')
                location = j.find('span', class_='location').text.replace('\n', '')
                company = j.find('span', class_='company').text.replace('\n', '')
                more_info = j.find('a', class_='title')['href']
            except:
                print("An exception occurred")

            with open(f'{folder_name}/{idx}.txt') as f:
                f.write(f'Job title: {title.strip()}\n')
                f.write(f'Location: {location.strip()}\n')
                f.write(f'Company Name: {company.strip()}\n')
                f.write(f'More Info: {more_info.strip()}\n')
            print(f'File saved: {idx}')


if __name__ == '__main__':
    while True:
        find_jobs()
        time_wait = 10
        print(f'Waiting {time_wait} minutes...')
        time.sleep(time_wait * 60)
