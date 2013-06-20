psi.py
===
Scrapes NEA's [website](http://app2.nea.gov.sg/anti-pollution-radiation-protection/air-pollution/psi/psi-and-pm2-5-readings), parses 3-hour PSI information, and presents it as a JSON object that can be easily used in other applications.

To reduce load on the web page, you should run this script as a cron job and redirect it's `stdout` to a static file which your application retrieves. 

There is no point in setting a very high refresh rate as NEA's website is only updated every hour.