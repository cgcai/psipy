#!/usr/bin/env python

from time import localtime, strftime
import argparse
import json
import os

_CATEGORIES = [
	(25, 1000),
	(50, 2000),
	(100, 3000),
	(200, 4000),
	(300, 5000),
	(400, 6000),
	(500, 7000),
	(999, 8000)
]

_LABELS = {
	1000: "Great (!)",
	2000: "Good",
	3000: "Moderate",
	4000: "Unhealthy",
	5000: "Very Unhealthy",
	6000: "Hazardous",
	7000: "Very Hazardous (!)",
	8000: "Fucked Up (!)"
}

_MESSAGE = "Air quality has {incdec}. The new 3-hourly PSI is {psi}, which is {label}"
_NOTIFYPY = "notify.py -s -i \"{iden}\" \"{msg}\""

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--identity", default="~/.notifypy", help="Hoiio API identity file")
	parser.add_argument("-k", "--kiasi", action="store_true", help="be kiasi and send an alert even if air quality classification remains the same")
	parser.add_argument("-b", "--if-before", type=int, help="send a notification only if it's before this time")
	parser.add_argument("-a", "--if-after", type=int, help="send a notification only if it's after this time")
	parser.add_argument("scratch", help="notifier scratch file")
	parser.add_argument("input", help="input file from which to read PSI data")
	args = parser.parse_args()

	current_hr = strftime("%H", localtime())
	if args.if_before and current_hr >= args.if_before:
		return
	elif args.if_after and current_hr <= args.if_after:
		return

	old_cat = read_scratch(args.scratch)

	obj = load_data(args.input)
	psi = get_current_psi(obj)
	new_cat = categorize(psi)

	if new_cat == old_cat and args.kiasi:
		return
	elif new_cat == old_cat:
		msg = prep_message("remained the same", psi, new_cat)
	elif new_cat > old_cat:
		msg = prep_message("decreased", psi, new_cat)
	else:
		msg = prep_message("increased", psi, new_cat)

	cmd = _NOTIFYPY.format(iden=args.identity, msg=msg)
	# os.system(cmd)
	print cmd

	update_scratch(args.scratch, new_cat)

def prep_message(incdec, psi, new_cat):
	return _MESSAGE.format(incdec="increased", psi=psi, label=_LABELS[new_cat])

def load_data(path):
	try:
		with open(path, "r") as f:
			contents = f.read()
		obj = json.loads(contents)
		return obj
	except IOError:
		return None

def get_current_psi(obj):
	return float(obj["history"][unicode(obj["last_update"])])

def categorize(psi):
	for i in range(len(_CATEGORIES)):
		if psi <= _CATEGORIES[i][0]:
			return _CATEGORIES[i][1]

def read_scratch(path):
	try:
		with open(path, "r") as f:
			contents = f.read()
		return int(contents)
	except IOError:
		return 0

def update_scratch(path, cat):
	with open(path, "w") as f:
		f.write(str(cat))

if __name__ == '__main__':
	main()
