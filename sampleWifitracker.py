import subprocess
import time
from time import gmtime,strftime, sleep
import argparse
import csv
import string
import gps
import os
#os.system('sudo systemctl stop gpsd.socket')
#os.system('sudo systemctl disable gpsd.socket')
#os.system('sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock')
#time.sleep(2)
#sleep for 2 seconds
#
parser = argparse.ArgumentParser(description='Display WLAN signal strength.')
parser.add_argument(dest='interface', nargs='?', default='wlan0',
                help='wlan interface (default: wlan0)')
args = parser.parse_args()
session = gps.gps("localhost", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
updateTime = strftime("%Y-%m-%d %H-%M-%S", gmtime())
download_dir = "wifiGPS_" + updateTime + ".csv" #where you want the file to be downloaded to 
csv = open(download_dir, "w") 
#"w" indicates that you're writing strings to the file
columnTitleRow = "link, strength, lat, long\n"
csv.write(columnTitleRow)
csv.close()



try:

    while True:
        

    # update wifi report
	    cmd = subprocess.Popen('iwconfig %s' % args.interface, shell=True,
	                   stdout=subprocess.PIPE)
	    updateTime = strftime("%Y-%m-%d %H-%M-%S", gmtime())
	    # update gps
	    report = session.next()
	            # Wait for a 'TPV' report and display the current time
	            # To see all report data, uncomment the line below
	#        print report
	    if report['class'] == 'TPV' and  hasattr(report, 'lon') and hasattr(report, 'lat'):
	        for line in cmd.stdout:
	            if 'Link Quality' in line:
	                # get link quality
	                link = ""
	                link1 = line.split("=")
	                link2 = link1[1].split(" ")
	                link += link2[0]

	                # get strength
	                strength = string.replace(link1[2]," dBm","")

	                # get geo
	                latitude = report.lat
	                longitude = report.lon
	                # line.lstrip(' ') + 
	                row = link.strip() +","+ strength.strip() +","+ str(latitude) +","+str(longitude)+"\n"
	                print updateTime
	                print row
	                csv = open(download_dir, "a")
	                csv.write(row)
	                csv.close()
	                break
	            elif 'Not-Associated' in line:
	            	latitude = report.lat
	                longitude = report.lon
	                bad_row = "0" +","+ "0" +","+ str(latitude) +","+str(longitude)+"\n"
	                print bad_row
	                csv = open(download_dir, "a")
	                csv.write(bad_row)
	                csv.close()
	            time.sleep(1)
	            #latitude = report.lat
	            #longitude = report.lon
	            #print latitude,longitude
	        #print "while loop ..."
	        #print str(counter)
except KeyError:
            print "KeyError"
            pass
except KeyboardInterrupt:
            print "KeyboardInterrupt"
            quit()
except StopIteration:
            session = None


