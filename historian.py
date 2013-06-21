#!/usr/bin/env python

import argparse
import json

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("scratch", help="historian scratch file")
	parser.add_argument("input", help="input file from which to read PSI data")
	parser.add_argument("history", help="file to write PSI history to")
	args = parser.parse_args()

	last_ts = read_scratch(args.scratch)
	psi = load_data(args.input)
	last_ts, new_entries = process(psi, last_ts)
	append_history(args.history, new_entries)
	update_scratch(args.scratch, last_ts)

def process(data, last_ts):
	base_date = int(data["date"])	
	new_entries = list()
	for hour, value in sorted(data["history"].items(), key=lambda kv: int(kv[0]))[:int(data["last_update"]) + 1]:
		time = base_date + int(hour) * 3600
		if time > last_ts:
			new_entries.append((time, value))
			last_ts = time
	return (last_ts, new_entries)

def load_data(path):
	try:
		with open(path, "r") as f:
			contents = f.read()
		obj = json.loads(contents)
		return obj
	except IOError:
		return None

def read_scratch(path):
	try:
		with open(path, "r") as f:
			contents = f.read()
		return int(contents)
	except IOError:
		return 0

def update_scratch(path, ts):
	with open(path, "w") as f:
		f.write(str(ts))

def append_history(path, new_entries):
	with open(path, "a") as f:
		for (ts, val) in new_entries:
			f.write("{timestamp} {value}\n".format(timestamp=ts, value=val))

if __name__ == '__main__':
	main()
