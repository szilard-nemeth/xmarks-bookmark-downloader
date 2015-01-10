'''
Created on 2013.06.03.

@author: szyszy
'''

import urllib.request

#url = "https://login.xmarks.com/?referrer=http%3A//www.xmarks.com/"
url = "https://login.xmarks.com/"
username = 'szyszy'
password = ''

passman = urllib.request.HTTPPasswordMgrWithDefaultRealm()
passman.add_password(None, url, username, password)

authhandler = urllib.request.HTTPBasicAuthHandler(passman)

opener = urllib.request.build_opener(authhandler)
urllib.request.install_opener(opener)

pagehandle = urllib.request.urlopen(url)
print(pagehandle.geturl())

#urllib.request.urlopen()
