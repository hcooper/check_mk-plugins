#!/usr/bin/env python
# Copyright (c) 2010, Nick Anderson <nick@cmdln.org>
# All rights reserved.
 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
# ARE DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys
import time
import getpass
import optparse

from datetime import date
from string import Template

import XenAPI

__version__ = "1.2"
__author__ = "Nick Anderson <nick@cmdln.org>"
__website__ = "http://github.com/nickanderson/check_citrix_xenserver_license"

def main(session, options):
    """
    Get number of days until license expires 
    Return 0 if license not expired, 2 if expired
    """
    hosts = session.xenapi.host.get_all()
    host = hosts[0]
    record = session.xenapi.host.get_record(host)
    # Get the date part of the string
    expires = time.strptime(record["license_params"]["expiry"][0:8], 
		    "%Y%m%d")[0:3]
    # create date object for finding difference in days
    expires_on = date(int(expires[0]), int(expires[1]), int(expires[2]))
    expire_days = (expires_on - date.today()).days
    display = Template('XenServer License: $status | expire_days=%s' 
            %expire_days)

    if int(expire_days) > int(options.warning_days):
        print display.substitute(status='OK') 
        session.xenapi.session.logout()
        sys.exit(0)

    # If number of days until expire is less than warning
    elif int(expire_days) <= int(options.warning_days):
        if int(expire_days) <= int(options.critical_days):
            print display.substitute(status='CRITICAL Expiring in %s days'%expire_days) 
            session.xenapi.session.logout()
            sys.exit(2)
        else:
            print display.substitute(status='WARNING Expiring in %s days'%expire_days) 
            session.xenapi.session.logout()
            sys.exit(1)
    else:
        print display.substitute(status='Unknown')
        session.xenapi.session.logout()
        sys.exit(3)

if __name__ == "__main__":
    # define options
    op = optparse.OptionParser("usage: %prog [options]", 
            version = "%%prog v%s\nAuthor: %s\nWebsite: %s" % 
            (__version__, __author__, __website__))

    og_sess = optparse.OptionGroup(op, "Session Options")
    og_sess.add_option('--server',
            dest='server',
            help="xenserver host (default: %default)")
    og_sess.add_option('--username',
            dest='username',
            help="xenserver username (defaut: %default)")
    og_sess.add_option('--password',
            dest="password",
            help="xenserver password")
    op.add_option_group(og_sess)

    og_nag = optparse.OptionGroup(op, "Nagios Options")
    og_nag.add_option('-c',
            dest='critical_days',
            help="critical threshold for days (default: %default)")
    og_nag.add_option('-w',
            dest='warning_days',
            help="warn threshold for days (default: %default)")
    op.add_option_group(og_nag)

    op.set_defaults(server='localhost',
            username = 'root',
            password = '',
            warning_days = 30,
            critical_days = 10)

    # parse and validate
    (options, args) = op.parse_args()
    if options.password == '':
        options.password = getpass.getpass("password: ")

    # First acquire a valid session by logging in:
    session = XenAPI.Session("https://"+options.server)
    try:
        session.xenapi.login_with_password(options.username, options.password)
    except XenAPI.Failure, e:
        if e.details[0]=='HOST_IS_SLAVE':
            session=XenAPI.Session('https://'+e.details[1])
            session.login_with_password(options.username,options.password)
    except:
        print 'XenServer License: Unknown, could not establish session'
        sys.exit(3)

    main(session, options)
