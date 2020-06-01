from bs4 import BeautifulSoup
import openpyxl
import requests
import sendmail
import os

def check_scrape(html):
    soup = BeautifulSoup(html)

    for a in soup.find_all('a', href=True):
        print("Found the URL:", a['href'])

def scrape_file(file,email):
    wb = openpyxl.load_workbook(file)
    ws = wb.active
    for row in ws.iter_rows(min_row=2):
        status = check_webpage(row[0].value,row[1].value)
        if  status == 1:
            row[2].value = 'Found'
        elif status == 0:
            row[2].value = 'Not Found'
        else:
            row[2].value = 'Error'

    wb.save(file)
    sendmail.send_attachment(email,file)

def check_webpage(link,webpage):
    try:
        data = requests.get(webpage,verify=False).text
        return 1 if link in data else 0
    except:
        return 2

