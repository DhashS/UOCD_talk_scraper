from bs4 import BeautifulSoup
from parse import compile
import pandas as pd

with open('./renaming_report.php') as f:
    offline_site = f.read()

#Let's just scrape it out of the alerts
resp_str = "javascript:alert('A member of the public renamed {} to {} on {} at a renaming event because: \\n\\n\\n----------------------------------\\n\\n\\n{}\\n\\n\\n----------------------------------')"

p = compile(resp_str)

soup = BeautifulSoup(offline_site, 'html.parser')
tbls = soup.find_all('td')

cols = ["old_name", "new_name", "time", "text", "bid"]
df = pd.DataFrame(columns=cols)

#grab all alerts and parse them
txts = [p.parse(x.a.get('href')) for x in tbls if not str(x).find('alert') == -1]
#if it has a $ char and isn't an alert
bids = [x.contents[0][1:] for x in tbls if not str(x).find('$') == -1 and str(x).find('alert') == -1]

#rack em' stack em'
for txt, b in zip(txts, bids):
    new_row = pd.DataFrame([list(txt) + [float(b)]], columns=cols)
    df = df.append(new_row)

#they're datetimes now
df.time = df.time.map(pd.to_datetime)

#slap an index on there
#http://stackoverflow.com/questions/18878308/pandas-reindex-unsorts-dataframe#18878413
df.index = range(1,len(df) + 1)

#spit it out!
df.to_csv('./cambridge_street_rename.csv')

