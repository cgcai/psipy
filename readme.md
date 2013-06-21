PSI Tools
===
A collection of scripts to monitor the haze disaster in Singapore that began in mid-June 2013.

##Aim
The following scripts and APIs are made available so that interested parties may monitor the situation as it develops, or develop their software solutions based on structured data.

Currently, the only data being collected is the 3-hourly PSI readings published by NEA (link below). Interpretation of this data is left to the user.

Timestamps are in GMT and follow the Unix convention.

##psi-notify.py
Sends an SMS alert using `notify.py` when NEA's 3-hourly PSI reading changes significantly.

##psi.py
Scrapes NEA's [website](http://app2.nea.gov.sg/anti-pollution-radiation-protection/air-pollution/psi/psi-and-pm2-5-readings), parses 3-hour PSI information, and presents it as a JSON object that can be easily used in other applications.

To reduce load on the web page, you should run this script as a cron job and redirect it's `stdout` to a static file which your application retrieves. 

The human-formatted JSON can be obtained from [psi.qxcg.net](http://psi.qxcg.net).

There is no point in setting a very high refresh rate as NEA's website is only updated every hour. Currently, `cron` updates PSI every 4th, 12th, and 36th minute of the hour only.

##historian.py
Keeps a log of 3-hourly PSI readings published by NEA. 

The existing log can be accessed at [psi.qxcg.net/history.txt](http://psi.qxcg.net/history.txt). The historian is run after `psi.py` completes.