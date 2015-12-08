#!/usr/bin/python

# Download bookmarks from Xmarks(TM) as an HTML page.
# Copyright (C) 2012  Romain Lenglet <romain.lenglet@berabera.info>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import cookielib
import datetime
import getpass
import urllib
import urllib2
import re


def login(username, password):
    """Login into Xmarks.

    Args:
        username: The Xmarks username to use for login.
        password: The password to use for login.

    Returns:
        An URL opener with the right cookies set for accessing the
        logged in user's pages.
    """
    url = 'https://login.xmarks.com/login/login'

    cookie_jar = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))


    # First get an authentication token from the login page.
    first_login_page = opener.open(url).read()
    auth_token_match = re.search(
        '<input type="hidden" name="token" value="([^"]*)" />',
        first_login_page)
    auth_token = auth_token_match.group(1)

    # Then authenticate for real.
    params = {'token': auth_token,
              'username': username,
              'password': password}
    opener.open(url, urllib.urlencode(params)).read()

    return opener


def download_bookmarks_html(opener, username, date):
    """Get the user's bookmarks as an HTML page.

    Args:
        opener: An URL opener with the right cookies set for accessing
            the logged in user's pages.
        username: The username for which to retrieve bookmarks.
        date: A datetime.date specifying the snapshot of bookmarks to
            download.

    Returns:
        A string containing all the user's bookmarks as a HTML page.
    """
    url_format = 'https://my.xmarks.com/bookmarks/export_to_html/0/' \
                 '{username}-bookmarks-{date}.html'
    url = url_format.format(username=username, date=date.isoformat())

    return opener.open(url).read()


def logout(opener):
    """Logout from Xmarks.

    Args:
        opener: An URL opener with the right cookies set for accessing
            a logged in user's pages.
    """
    url = 'https://login.xmarks.com/logout'
    opener.open(url)


def main():
    parser = argparse.ArgumentParser(
        description='Download Xmarks(TM) bookmarks to the standard output.')
    parser.add_argument('username', action='store',
                        help='the Xmarks username')
    args = parser.parse_args()

    password = getpass.getpass()

    opener = login(args.username, password)
    today = datetime.date.today()
    bookmarks_html = download_bookmarks_html(opener, args.username, today)
    logout(opener)

    print '%s' % (bookmarks_html,)


if __name__ == '__main__':
    main()
