import bs4 as bs
import pandas as pd
import urllib.request
import arrow

day = arrow.utcnow().shift(days=+1).format('ddd MMM D')

print(day)

page = urllib.request.urlopen('https://spotthestation.nasa.gov/sightings/view.cfm?\
country=United_States&region=North_Carolina&city=New_Bern#.W83_6mhKiUm')
soup = bs.BeautifulSoup(page, 'lxml')

table = soup.find('table')
rows = table.find_all('tr')

tab = []
for tr in rows:
    td = tr.find_all('td')
    row = [tr.text.strip() for tr in td if tr.text.strip()]
    if row:
        tab.append(row)

df = pd.DataFrame(tab, columns=['Date', 'Visible', 'Max Height', 'Appears', 'Disappears', 'Share'])
del df['Share']
#print(df)

new = df['Date'].str.split(',', n = 1, expand=True)
df['Day']=new[0]
df['Time']=new[1]
df.drop(columns=['Date'], inplace=True)
iss = pd.DataFrame(df, columns=['Day', 'Time', 'Visible', 'Max Height', 'Appears', 'Disappears'])
#print(iss)

def message():
    for row in iss.itertuples():
        if day in row:
            return'\nISS can be seen on ' + row.Day + ' at' + row.Time + '.' \
            + ' It will appear at ' + row.Appears + ' and disappear at ' + row.Disappears + \
            '.' +' It will be visible for ' + row.Visible + '.'

(message())