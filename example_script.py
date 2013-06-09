# Import module statements
import re, sys, httplib, urllib
from bs4 import BeautifulSoup
from mechanize import ParseResponse, urlopen, urljoin

# To read the information about a device, you will need the proper device ID. Enter device ID from the web URL in place of XXXXXXXXXX.
if len(sys.argv) == 1:
    uri = "https://graph.api.smartthings.com/device/show/XXXXXXXXXX"
else:
    uri = sys.argv[1]

# Open URL and parse out information to see what forms are required to login
response = urlopen(urljoin(uri, ""))
forms = ParseResponse(response, backwards_compat=False)
form = forms[0]
# Uncomment line below to print out the form names used for logging in
#print form

# Enter information for username and password. Must put information in quotes.
form["j_username"] = "username"
form["j_password"] = "password"

# Send login information and read webpage data
text_data = urlopen(form.click()).read()

# START DATA PARSING
# Get HTML code of web page to parse through
soup = BeautifulSoup(text_data)

# Find line that has desired data. This case grabs the line with temperature.
text = soup.find_all(text=re.compile("temperature"))

# Get indices to parse out desired data
start_idx = text[0].index(':')+2
end_idx = text[0].index('F')-1

# Store information in a variable
var1 = text[0][start_idx:end_idx]

# Repeat for other sensors
text_data = urlopen('https://graph.api.smartthings.com/device/show/YYYYYYYY').read()
soup = BeautifulSoup(text_data)
text = soup.find_all(text=re.compile("temperature"))
start_idx = text[0].index(':')+2
end_idx = text[0].index('F')-1
var2 = text[0][start_idx:end_idx]

# SEND DATA TO THINGSPEAK
# Package data together in the next line. The temp data is low by about 4 degrees so I added 4. Get your API KEY from the Channel you set up on ThingSpeak.
params = urllib.urlencode({'field1': str(int(var1)+5), 'field2': str(int(var2)+5), 'key':'YOUR API KEY'})

# Other code to send information to ThingSpeak
headers = {"Content-type": "application/x-www-form-urlencoded","Accept":"text/plain"}
conn = httplib.HTTPConnection("api.thingspeak.com:80")
conn.request("POST", "/update", params, headers)
response = conn.getresponse()
#print response.status, response.reason
data = response.read()
conn.close()
