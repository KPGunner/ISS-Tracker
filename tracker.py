import bs4 as bs
import pandas as pd
import urllib.request
import arrow

# Pull current date. Shift one day ahead to see if ISS is coming tomorrow.
day = arrow.utcnow().shift(days=+1).format('ddd MMM D')
print(day)

# Establish page to scrape information from.
page = urllib.request.urlopen('https://spotthestation.nasa.gov/sightings/view.cfm?\
country=United_States&region=North_Carolina&city=New_Bern#.W83_6mhKiUm')
soup = bs.BeautifulSoup(page, 'lxml')

# Find the table with the ISS location information.
table = soup.find('table')
rows = table.find_all('tr')

# Pull every row in the table and add it to the table.
tab = []
for tr in rows:
    td = tr.find_all('td')
    row = [tr.text.strip() for tr in td if tr.text.strip()]
    if row:
        tab.append(row)

# Put the table in a Pandas DataFrame and establish column names.
df = pd.DataFrame(tab, columns=['Date', 'Visible', 'Max Height', 'Appears', 'Disappears', 'Share'])
del df['Share']

# Split the "Date" column to separate the date and time. Establish new columns and arrange
new = df['Date'].str.split(',', n=1, expand=True)
df['Day'] = new[0]
df['Time'] = new[1]
df.drop(columns=['Date'], inplace=True)
iss = pd.DataFrame(df, columns=['Day', 'Time', 'Visible', 'Max Height', 'Appears', 'Disappears'])


# Iterate through the DataFrame to find if tomorrow's date is included, parse row info for message composition.
def message():
    for row_info in iss.itertuples():
        if day in row_info:
            return '\nISS can be seen on ' + row_info.Day + ' at' + row_info.Time + '.' \
                   + ' It will appear at ' + row_info.Appears + ' and disappear at ' + row_info.Disappears + \
                   '.' + ' It will be visible for ' + row_info.Visible + '.'


(message())
