"""
download_decorator.py

Copyright 2010 Andres Riancho

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
import w4af.core.controllers.output_manager as om


def download_debug(fn):
    def new(self, remote_filename, local_filename):
        #   Run the original function
        result = fn(self, remote_filename, local_filename)

        msg = 'download( "' + remote_filename + '" , "' + \
            local_filename + '") == ' + result

        #   Print the message to the debug output
        om.out.debug(msg)

        #   Return the result
        return result

    return new
