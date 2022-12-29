"""
test_backspace_between_dots.py

Copyright 2012 Andres Riancho

This file is part of w4af, http://w4af.org/ .

w4af is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

w4af is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with w4af; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""
import unittest
from unittest.case import skip

from w4af.core.data.parsers.doc.url import URL
from w4af.core.data.url.HTTPRequest import HTTPRequest
from w4af.plugins.evasion.backspace_between_dots import backspace_between_dots


@skip('URL normalization breaks evasion. @see: 4fa67fbb')
class TestEvasion(unittest.TestCase):
    
    def test_no_modification(self):
        
        bbd = backspace_between_dots()

        u = URL('http://www.w4af.com/')
        r = HTTPRequest(u)
        self.assertEqual(bbd.modify_request(r).url_object.url_string,
                         'http://www.w4af.com/')

    def test_modify_basic(self):
        
        bbd = backspace_between_dots()
        
        u = URL('http://www.w4af.com/../')
        r = HTTPRequest(u)
        self.assertEqual(bbd.modify_request(r).url_object.url_string,
                         'http://www.w4af.com/.%41%08./')

    def test_modify_with_filename(self):
        
        bbd = backspace_between_dots()
        
        u = URL('http://www.w4af.com/abc/def/.././jkl.htm')
        r = HTTPRequest(u)
        self.assertEqual(bbd.modify_request(r).url_object.url_string,
                         'http://www.w4af.com/abc/def/.%41%08././jkl.htm')
        #
        #    The plugins should not modify the original request
        #
        self.assertEqual(u.url_string,
                         'http://www.w4af.com/abc/def/.././jkl.htm')