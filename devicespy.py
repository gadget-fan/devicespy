#!/usr/bin/python

# The "os" module is used for the statusCheck function
# The "mysql.connector" module use is obvious
import os
import mysql.connector
import httplib, urllib
from time import localtime, strftime
import time


#Define the ping function
def statusCheck(hostname):

        ping_response = os.system("ping -c 1 -w5 " + hostname + " > /dev/null 2>&1")
        if ping_response == 0:
                return 'ON'
        else:
                return 'OFF'


def poststatus():
  #Define the query that will select which hosts to check for status
  #Execute the query and process the results
  #Connect to the database
  cnx = mysql.connector.connect(user='homemanager', password='homepass', database='HomeDeviceMonitor')
  hostlistquery = ("SELECT * FROM DeviceList WHERE monitor = 'YES'")
  cursor = cnx.cursor()
  cursor.execute(hostlistquery)
  rows = cursor.fetchall()
  for row in rows:
        status = statusCheck(row[2])
        params = urllib.urlencode({'field1': row[1], 'field2': status,'key':'GMZPZSBWFIQLZHYW'})
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.HTTPConnection("api.thingspeak.com:80")

        try:
                conn.request("POST", "/update", params, headers)
                response = conn.getresponse()
                print row[1] + " at IP " + row[2] + " is " + status + " at " + strftime("%a, %d %b %Y %H:%M:%S", localtime())
                print params
                print response.status, response.reason
                data = response.read()
                conn.close()
        except:
                print "connection failed"

  cursor.close()
  cnx.close()

# Execute the main loop every 60 seconds (thingspeak api limit of 15 secs)
if __name__ == "__main__":
        while True:
                poststatus()
                time.sleep(60) 
