from bs4 import BeautifulSoup
import requests
import csv
from selenium import webdriver
from datetime import datetime
from datetime import timedelta
import time
import os

d_airport = '/m/04jpl'
a_airport = ['GVA', 'DUB', 'VIE', 'CPH', 'MAD', 'ATH', 'AGP', 'CDG', 'AMS', 'LIS', 'BCN', 'PMI', 'FNC', 'NCE', 'WAW']
flight_date = '2020-03-27'

driver = webdriver.Chrome('/Users/blazkranjcev/Downloads/chromedriver')

def click_more():
    click_more = driver.find_element_by_class_name(
        'gws-flights-results__dominated-link')
    driver.execute_script("arguments[0].click();", click_more)
    time.sleep(5)

i = 0
listSize = len(a_airport)
while i < listSize:
    csv_name = f'{a_airport[i]}_{flight_date}.csv'
    csv_file = open(csv_name, 'a')

    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(
    ['Carrier', 'Airport Code', 'Flight hours', 'Stops', 'Price', 'DateObtained'])

    url = f'https://www.google.com/flights?lite=0#flt={d_airport}.{a_airport[i]}.{flight_date};c:GBP;e:1;sd:1;t:f;tt:o'
    driver.get(url)
    time.sleep(2)

    click_more()

    # test

    time.sleep(5)

    html = driver.execute_script("return document.documentElement.outerHTML")
    sel_soup = BeautifulSoup(html, 'html.parser')

    source = driver.page_source
    soup = BeautifulSoup(source, 'lxml')

    # scraper part

    for element in sel_soup.find_all('div', class_='gws-flights-results__collapsed-itinerary'):

        carrier = element.find(
            'div', class_='gws-flights-results__carriers').text
        flight_times = element.find(
            'div', class_='gws-flights-results__times').text
        stops = element.find('div', class_='gws-flights-results__stops').text

        try:
            price = element.find(
                'div', class_='gws-flights-results__price').text
            airport_code = element.find(
                'div', class_='gws-flights-results__airports').text
        except Exception as e:
            price = None
            airport_code = None

        dateObtained = datetime.now()

        csv_writer.writerow(
            [carrier, airport_code, flight_times, stops, price, dateObtained])

    csv_file.close()
    i += 1


driver.close()



