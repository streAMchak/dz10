import sqlite3
import requests
from bs4 import BeautifulSoup
from datetime import datetime

conn = sqlite3.connect('weather.db')
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS weather (
    datetime TEXT,
    temperature REAL
)
''')

conn.commit()

url = 'https://weather.com/'  
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

temperature_tag = soup.find('span', class_='CurrentConditions--tempValue--3KcTQ')

if temperature_tag:
    temperature = float(temperature_tag.text.replace('°', '')) 
else:
    temperature = None
    print("Не вдалося знайти температуру.")

if temperature is not None:
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cur.execute('''
    INSERT INTO weather (datetime, temperature)
    VALUES (?, ?)
    ''', (current_datetime, temperature))
    conn.commit()

conn.close()
