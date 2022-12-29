"""
test_bing_spider.py

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
import pytest

from w4af.plugins.tests.helper import PluginTest, PluginConfig, MockResponse


def responses(fmt, expected_urls):
    return [MockResponse(fmt % eu, 'Response body.') for eu in expected_urls]

@pytest.mark.fails
class TestBingSpider(PluginTest):

    target_url = 'http://www.bonsai-sec.com/'
    target_url_fmt = 'http://www.bonsai-sec.com/%s'

    _run_configs = {
        'cfg': {
            'target': target_url,
            'plugins': {'crawl': (PluginConfig('bing_spider'),)}
        }
    }
    EXPECTED_URLS = (
        'es/education/', 'en/clients/', 'es/', 'services/',
        'research/', 'blog/', 'education/', 'es/research/',
        'blog', 'es/clients/', '',
    )

    MOCK_RESPONSES = responses(target_url_fmt, EXPECTED_URLS)

    def test_found_urls(self):
        cfg = self._run_configs['cfg']
        self._scan(cfg['target'], cfg['plugins'])

        urls = self.kb.get_all_known_urls()

        found_urls = set(str(u) for u in urls),
        expected_urls = set((self.target_url + end) for end in self.EXPECTED_URLS)
        
        self.assertEqual(found_urls, expected_urls)
