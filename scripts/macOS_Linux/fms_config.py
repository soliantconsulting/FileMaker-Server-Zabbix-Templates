#!/usr/bin/python
#######################################################################
#    fms_config.py
#
#    Python script used for calling the FMS Admin API.
#    For macOS and FM Cloud
#    runs on the default Python 2.7 on both platforms
#
#    Wim Decorte <wdecorte@soliantconsulting.com>
#    version 1.1.0 - 2020-11-26 - 8:32 AM
#
#    Released under the GNU General Public License WITHOUT ANY WARRANTY.
#
#######################################################################

import requests
from requests.auth import HTTPBasicAuth
import sys

# works in FMC 1.17:
from urllib3.exceptions import InsecureRequestWarning
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# to disable the insecure SSL warnings since we are using localhost
# requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# old versions of requests had urlib3 in them, this seems to be more modern code
# import urllib3
# to disable the insecure SSL warnings since we are using localhost
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# read the passed arguments, first one is always the script name so our parameters start at 1

u = sys.argv[1]
p = sys.argv[2]
fms_version = sys.argv[3]
# server = "192.168.2.115" # should always be localhost in production, for testing, can change to something else
server = "localhost"

if fms_version == '17':
    url = "https://" + server + "/fmi/admin/api/v1/user/login"
    creds = {'username' : u ,
          'password' : p
           }
    headers = {"Content-Type": "application/json"}
    resp = requests.post(url, json=creds, headers=headers, verify=False)
elif fms_version == '17C':
    # there is no /fmi/ in the URL
    url = "https://" + server + "/admin/api/v1/user/login"
    creds = {'username' : u ,
          'password' : p
           }
    headers = {"Content-Type": "application/json"}
    resp = requests.post(url, json=creds, headers=headers, verify=False)
else:
    url = "https://" + server + "/fmi/admin/api/v2/user/auth"
    resp = requests.post(url, auth=HTTPBasicAuth(u, p), verify=False)

if resp.status_code != 200:
    # This means something went wrong.
    exit("could not get token - " + str(resp.status_code))
else:
    Jsonresponse = resp.json()
    if fms_version == '17' or fms_version == '17C':
        token = Jsonresponse['token']
    else:
        token = Jsonresponse['response']['token']


# if we're still running, call the config endpoint
if fms_version == '17C':
    # need to get the two cookies first, by going to the main login page    
    main_url = "https://" + server + "/console/templates/pages/comodocert/index.html"
    temp_response = requests.get(main_url, verify=False)
    csrf = temp_response.cookies['_csrf']
    xsrf = temp_response.cookies['XSRF-TOKEN']

    # then call the special config endpoint
    config_url = "https://" + server + "/onboarding/serverconfig"
    headers = {
        'Authorization' : "Bearer " + token,
        'X-XSRF-TOKEN' : xsrf
        }
    cookies = requests.cookies.RequestsCookieJar()
    cookies.set('_csrf', csrf)
    cookies.set('XSRF-TOKEN', xsrf)
    config = requests.get(config_url, headers=headers, cookies=cookies, verify=False)
else:
    config_url = "https://" + server + ":16000/fmi/admin/internal/v1/server/config"
    headers = {'Authorization' : "Bearer " + token}
    config = requests.get(config_url, headers=headers, verify=False)

# output what we received
print(config.text)

# delete the admin session
# log out to free up an admin console session
if fms_version == '17':
    logout_url = "https://" + server + "/fmi/admin/api/v1/user/logout/" + token
    logout = requests.post(logout_url, headers=headers, verify=False)
elif fms_version == '17C':
    logout_url = "https://" + server + "/admin/api/v1/user/logout/" + token
    logout = requests.post(logout_url, headers=headers,verify=False)
else:
    logout_url = url + "/" + token
    logout = requests.delete(logout_url, headers=headers,verify=False)

