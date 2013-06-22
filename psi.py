#!/usr/bin/env python

from bs4 import BeautifulSoup
import argparse
import time
import urllib2
import json
import re

_PSI_SOURCE = "http://app2.nea.gov.sg/anti-pollution-radiation-protection/air-pollution/psi/past-24-hour-psi-readings"
_PSI_DATE_PATTERN = "\\b\\d?\\d (jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec) \\d{4}\\b"
_DATE_FMT = "%d %b %Y"

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("output", help="output file")
	parser.add_argument("-t", "--tabsize", type=int, default=2, help="number of spaces to indent JSON")
	args = parser.parse_args()

	date, psi_values = scrape_NEA()
	psi_info = _process_psi(date, psi_values)
	json_str = json.dumps(psi_info, indent=args.tabsize)
	
	with open(args.output, "w") as f:
		f.write(json_str)

def _process_psi(date, psi_values):
	struct = dict()
	hist_struct = dict()

	last = None
	for hr in range(len(psi_values)):
		hr_val = psi_values[hr]
		
		# Compute the hour of the last update.
		if hr_val != None:
			last = hr

		# Associate each value with the hour it was seen.
		hist_struct[hr] = psi_values[hr]

	struct["date"] = date
	struct["last_update"] = last
	struct["history"] = hist_struct

	return struct

def scrape_NEA():
	source_html = urllib2.urlopen(_PSI_SOURCE).read()
	dom = BeautifulSoup(source_html)

	# Scrape and parse the date from the header.
	header = dom.find_all("h1")[2].string.strip()
	matches = re.search(_PSI_DATE_PATTERN, header, flags=re.IGNORECASE)
	if matches == None:
		date = None
	else:
		raw_date = matches.group(0)
		date = _parse_datetime(raw_date)

	# Scrape PSI rows.
	psi_table = dom.find_all("table")[1] # PSI values are in the first table.
	psi_rows = psi_table.find_all("tr")[1:][::2]

	raw_psi_values = list()
	for row in psi_rows:
		for td in row.find_all("td")[1:]: # The first column of each PSI row is some human text.
			val = td.find(text=True).string.strip()
			raw_psi_values.append(val)

	psi_values = map(_parse_raw_value, raw_psi_values)
	return (date, psi_values)

def _parse_datetime(dtval):
	try:
		parsed = int(time.mktime(time.strptime(dtval, _DATE_FMT)))
	except ValueError:
		parsed = None
	return parsed

def _parse_raw_value(val):
	try:
		parsed = float(val)
	except ValueError:
		parsed = None
	return parsed

if __name__ == '__main__':
	main()
