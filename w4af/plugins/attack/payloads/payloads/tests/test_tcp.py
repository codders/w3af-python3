"""
test_tcp.py

Copyright 2012 Andres Riancho

This file is part of w4af, https://w4af.readthedocs.io/ .

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
import pytest

from w4af.plugins.attack.payloads.payloads.tests.apache_payload_test_helper import ApachePayloadTestHelper
from w4af.plugins.attack.payloads.payload_handler import exec_payload


@pytest.mark.w4af_moth
class TestTCP(ApachePayloadTestHelper):

    EXPECTED_RESULT = {'0.0.0.0:3306', '0.0.0.0:80'}

    def test_tcp(self):
        result = exec_payload(self.shell, 'tcp', use_api=True)

        local_addresses = []
        for key, conn_data in result.items():
            local_addresses.append(conn_data['local_address'])

        local_addresses = set(local_addresses)

        for expected_local_address in self.EXPECTED_RESULT:
            self.assertIn(expected_local_address, local_addresses)
