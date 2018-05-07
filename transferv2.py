#!/usr/bin/python2.7

# Retrieves APNIC transfer data, massages into Google Chart
# Produces "apnic_transfers.html" output
# Shows transactions per month, and prefixes per month (in /24s)

# Lindsay Hill (lindsay@lkhill.com), 20150503

# TODO:
# Add option to ignore current, incomplete month
# Automatically handle missing months

import urllib
import re
from datetime import datetime

xfers_by_month = {}
prefixes_by_month = {}

url = "ftp://ftp.apnic.net/public/transfers/apnic/transfer-apnic-latest"

opener = urllib.FancyURLopener({})
f = opener.open(url)
raw_data = f.readlines()


output = open('apnic_transfers.csv', 'w')

for line in raw_data:
    a_check = re.search('^ipv4\|', line)
    if a_check:
        xfer_year_month = line.split("|")[9][:6]
        xfer_date = datetime.strptime(xfer_year_month, '%Y%m')
        prefixlen = line.split("|")[1].split('/')[1]
        prefixes = pow(2, 24 - int(prefixlen))
        xfers_by_month[xfer_date] = xfers_by_month.get(xfer_date, 0) + 1
        prefixes_by_month[xfer_date] = prefixes_by_month.get(xfer_date,
                                                             0) + prefixes

# Add missing months:
# (Should really figure out programmatic way of doing this)
# e.g. do some sort of step through dates, automatically identify gaps
# Or just get chart to treat null as 0?

missing_months = ["201012", "201102"]
for missing_month in missing_months:
    xfer_date = datetime.strptime(missing_month, '%Y%m')
    xfers_by_month[xfer_date] = 0
    prefixes_by_month[xfer_date] = 0

for month in sorted(xfers_by_month.keys()):
    output.write('%s,%s,%s\n' %
                 (month.strftime('%B %Y'),
                  xfers_by_month[month], prefixes_by_month[month]))

output.close()
