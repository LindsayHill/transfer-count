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


output = open('apnic_transfers.html', 'w')

for line in raw_data:
    a_check = re.search('^ipv4\|', line)
    if a_check:
        xfer_year_month = line.split("|")[9][:6]
        xfer_date = datetime.strptime(xfer_year_month, '%Y%m')
        prefixlen = line.split("|")[1].split('/')[1]
        prefixes = pow(2, 24-int(prefixlen))
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

pre_table = '''
<html>
<head>
</head>
<body>
<script type="text/javascript" src="https://www.google.com/jsapi"></script>
<script type="text/javascript">
google.load("visualization", "1.1", {packages: ["corechart"]});
google.setOnLoadCallback(drawChart);
function drawChart() {
var data = new google.visualization.DataTable();
data.addColumn("datetime", "Year/Month");
data.addColumn("number", "Transactions");
data.addColumn("number", "Prefixes (/24s)");
data.addRows([
'''
output.write('%s' % (pre_table))

for month in sorted(xfers_by_month.keys()):
    output.write('[new Date(%s000),%s,%s],\n' %
                 (month.strftime('%s'),
                  xfers_by_month[month], prefixes_by_month[month]))
post_table = '''
]);
var options = {
title: "APNIC Transfers per month",
hAxis: {
format: "MMM yyyy",
gridlines: {count: "-1"},
},
seriesType: "bars",
series: {
0: {targetAxisIndex: 0, type: "line"},
1: {targetAxisIndex: 1, type: "bars"},
},
vAxes: {
0: {title: "Transactions", side: "left"},
1: {title: "Prefixes (/24s)", side: "right"},
},
};
var chart = new google.visualization.ComboChart(document.getElementById("ch"));
var date_formatter = new google.visualization.DateFormat({
pattern: "MMM yyyy"
});
date_formatter.format(data, 0);
chart.draw(data, options);
function resizeHandler () {
chart.draw(data, options);
}
if (window.addEventListener) {
window.addEventListener("resize", resizeHandler, false);
}
else if (window.attachEvent) {
window.attachEvent("onresize", resizeHandler);
}
}
</script>
<div STYLE="min-height: 500px" id="ch"></div>
</body>
</html>
'''

output.write('%s' % (post_table))

output.close()
