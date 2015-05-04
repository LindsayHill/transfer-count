# transferCount.py - produces Google Chart showing APNIC IPv4 Transfers

This script generates an HTML page containing a Google Chart for all APNIC ipv4 transfers.

It pulls the current statistics from APNIC, then figures out how many transactions took place per month, and how many prefixes were transferred, in /24s.


## TODO

* Provide option to not include current month (so that we don't get odd-looking data for incomplete month)
* Rewrite so that it automatically updates whenever the graph is loaded
* Automatically handle months when there was no data. If we don't include in table, then chart will interpolate. But needs to be shown as zero for that month. Currently fills in data for the two missing months so far, and assumes that we won't have any more 'missing' months
* Get similar data for other RIRs. Would need to figure out how to handle inter-RIR transfers (don't want to double-count)
