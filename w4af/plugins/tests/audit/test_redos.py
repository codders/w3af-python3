"""
test_redos.py

Copyright 2018 Andres Riancho

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
import re
import time

from w4af.plugins.tests.helper import PluginTest, PluginConfig, MockResponse
from w4af.core.data.parsers.doc.url import URL


class ReDosMockResponse(MockResponse):
    def get_response(self, http_request, uri, response_headers):
        """
        Overwrite the mock response with one simple objective: add a delay
        which depends on the length of the redos parameter.
        """
        response_headers.update({'status': self.status})
        response_headers.update(self.headers)

        uri = URL(http_request.url)
        qs = uri.get_querystring()
        redos_param = qs.get(b'redos')[0]

        delay = len(redos_param) / 13.0
        time.sleep(delay)

        return self.status, response_headers, self.body


class TestREDoS(PluginTest):

    target_url = 'http://httpretty/re?redos='

    _run_configs = {
        'cfg': {
            'target': target_url,
            'plugins': {
                'audit': (PluginConfig('redos'),),
            }
        }
    }

    MOCK_RESPONSES = [
              ReDosMockResponse(url=re.compile(r'http://httpretty/re\?redos=.*'),
                                body='dummy'),
    ]

    def test_found_redos(self):
        cfg = self._run_configs['cfg']
        self._scan(cfg['target'], cfg['plugins'])
        vulns = self.kb.get('redos', 'redos')
        
        expected = [('re', 'redos')]
        self.assertExpectedVulnsFound(expected, vulns)
        self.assertAllVulnNamesEqual('ReDoS vulnerability', vulns)


class TestREDoSNegative(PluginTest):
    target_url = 'http://httpretty/re?redos='

    _run_configs = {
        'cfg': {
            'target': target_url,
            'plugins': {
                'audit': (PluginConfig('redos'),),
            }
        }
    }

    MOCK_RESPONSES = [
            MockResponse(url=re.compile(r'http://httpretty/re\?redos=.*'),
                         body='dummy',
                         delay=0.1),
    ]

    def test_found_redos(self):
        cfg = self._run_configs['cfg']
        self._scan(cfg['target'], cfg['plugins'])
        vulns = self.kb.get('redos', 'redos')

        self.assertEqual(len(vulns), 0)
