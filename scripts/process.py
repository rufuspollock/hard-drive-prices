# encoding: utf8
import os
import re
import urllib

import datautil.tabular

# original url of website (now offline)
# url = 'http://www.littletechshoppe.com/ns1625/winchest.html'

localfp = 'archive/winchest-20111107.html'

import dateutil.parser
import datetime

def get_tables():
    reader = datautil.tabular.HtmlReader()
    reader.read(open(localfp))
    tables = reader.tables
    wanted = tables[:4] + tables[5:7] + tables[8:10]
    out = datautil.tabular.TabularData()
    out.header = wanted[0].data[0]
    # TODO: rename W y to Warranty (years)
    out.header = [ x.replace('\n', ' ') for x in out.header ]
    out.header = ['Date', 'Normalized Cost', 'Manufacturer',
            'Capacity (GB)', 'Price', 'Warranty', 'Source' ]
    for t in wanted:
        out.data += t
    newdata = []
    current_date = None
    pergig = False
    for row in out.data:
        if len(row) == 2 and 'Note' not in row[0]: # a date
            # deal with messed up stuff like 2000 August 19-20
            datestr = row[0].split('-')[0]
            try:
                current_date = dateutil.parser.parse(datestr, default=datetime.datetime(1900, 1, 1))
            except:
                # some bad cases where you just have a note or comment ...
                print('Bad date: %s' % datestr)
                continue
            # get rid of secs ...
            current_date = str(current_date)[:10]
        # rows with e.g. Note XXX | some commment
        elif len(row) < 5:
            continue
        elif 'Source' in row[0]: # remove header from data
            # deal with switch to cost per GB
            if 'gigabyte' in row[5]:
                pergig = True
            continue
        else:
            newrow = cleanrow(row)
            if newrow is None:
                continue
            newdata.append([current_date] + newrow)
    out.data = newdata
    writer = datautil.tabular.CsvWriter()
    writer.write(out, open('data.csv', 'w'))

def cleanrow(row):
    source = row[0]
    manufacturer = row[1]
    warranty = row[2]
    capacity = row[3]
    price = row[4]
    if 'megabyte' in capacity:
        # megabyte or megabytes
        capacity = float(
            capacity.replace('megabyte', '').replace('s', '')
            ) / 1000.0
    elif 'gigabyte' in capacity:
        capacity = float(
            capacity.replace('gigabyte', '').replace('s', '')
            )
    elif 'terabyte' in capacity:
        capacity = float(
            capacity.replace('terabyte', '').replace('s', '')
            ) * 1000
    else:
        print('Bad capacity: %s' % capacity)
        print(row)
        return None
    try:
        price = float(price.replace('U$','').replace('$', '').replace(',', ''))
        costpergig = price / capacity
    except:
        # print('Bad price: %s' % price)
        # print(row)
        # some cases he does not have actual price just normed cost due to
        # complex calcs
        costpergig = float(row[5].replace('U$', '').replace('$', ''))
        # cost per mb not per gb
        if price not in ['Note 77', 'Note 85', 'Note 86', 'Note 87']:
            costpergig = costpergig * 1000.0
        price = capacity * costpergig
    manufacturer = manufacturer.replace('\n', ' ')
    newrow = [ costpergig, manufacturer, capacity, price, warranty, source ]
    return newrow


if __name__ == '__main__':
    get_tables()
