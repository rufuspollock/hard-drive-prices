import os
import re
import urllib

import simplejson as sj

import econ.data
# import BeautifulSoup as bs
from econ.data import Retriever

cache = os.path.join(os.path.dirname(__file__), 'cache')
retriever = Retriever(cache)

url = 'http://www.littletechshoppe.com/ns1625/winchest.html'

localfp = retriever.retrieve(url)
# soup = bs.BeautifulSoup(open(localfp).read())

import dateutil.parser
import datetime

def get_tables():
    reader = econ.data.HtmlReader()
    reader.read(open(localfp))
    tables = reader.tables
    wanted = tables[:4] + tables[5:7] + tables[8:10]
    out = econ.data.TabularData()
    out.header = wanted[0][0]
    # TODO: rename W y to Warranty (years)
    out.header = [ x.replace('\n', ' ') for x in out.header ]
    out.header = ['Date', 'Cost per MB ($)' ] + out.header[:-2]
    for t in wanted:
        out.data += t
    newdata = []
    current_date = None
    for row in out.data:
        if len(row) < 3: # a date
            # deal with messed up stuff like 2000 August 19-20
            datestr = row[0].split('-')[0]
            current_date = dateutil.parser.parse(datestr, default=datetime.datetime(1900, 1, 1))
            # get rid of secs ...
            current_date = str(current_date)[:10]
        elif 'Source' in row[0]: # remove header from data
            # TODO: deal with switch to cost per GB
            continue
        else:
            costpermeg = row[-1].replace('U$','').replace('$', '').replace(',', '')
            newrow = [ current_date, costpermeg ] + row[:-2]
            newdata.append(newrow)
    out.data = newdata
    writer = econ.data.CsvWriter()
    writer.write(open('data.csv', 'w'), out)

if __name__ == '__main__':
    get_tables()
