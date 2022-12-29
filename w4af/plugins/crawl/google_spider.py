"""
google_spider.py

Copyright 2006 Andres Riancho

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
from w4af.core.data.options.opt_factory import opt_factory
from w4af.core.data.options.option_list import OptionList
from w4af.core.data.search_engines.bing import bing as bing

from w4af.core.controllers.plugins.crawl_plugin import CrawlPlugin
from w4af.core.controllers.exceptions import BaseFrameworkException, RunOnce
from w4af.core.controllers.misc.is_private_site import is_private_site
from w4af.core.controllers.misc.decorators import runonce


class google_spider(CrawlPlugin):
    """
    Search bing using bing API to get new URLs
    :author: Andres Riancho (andres.riancho@gmail.com)
    """

    def __init__(self):
        CrawlPlugin.__init__(self)

        # User variables
        self._result_limit = 300

    @runonce(exc_class=RunOnce)
    def crawl(self, fuzzable_request, debugging_id):
        """
        :param debugging_id: A unique identifier for this call to discover()
        :param fuzzable_request: A fuzzable_request instance that contains
                                    (among other things) the URL to test.
        """
        bing_se = bing(self._uri_opener)

        domain = fuzzable_request.get_url().get_domain()
        if is_private_site(domain):
            msg = 'There is no point in searching bing for "site:%s".'\
                  ' Bing doesn\'t index private pages.'
            raise BaseFrameworkException(msg % domain)

        try:
            b_results = bing_se.get_n_results('site:' + domain,
                                                self._result_limit)
        except:
            pass
        else:
            self.worker_pool.map(self.http_get_and_parse,
                                    [r.URL for r in b_results])

    def get_options(self):
        """
        :return: A list of option objects for this plugin.
        """
        ol = OptionList()

        d = 'Fetch the first "result_limit" results from the Bing search'
        o = opt_factory('result_limit', self._result_limit, d, 'integer')
        ol.add(o)

        return ol

    def set_options(self, options_list):
        """
        This method sets all the options that are configured using the user
        interface generated by the framework using the result of get_options().

        :param options_list: A dictionary with the options for the plugin.
        :return: No value is returned.
        """
        self._result_limit = options_list['result_limit'].get_value()

    def get_long_desc(self):
        """
        :return: A DETAILED description of the plugin functions and features.
        """
        return """
        This plugin finds new URL's using bing. It will search for
        "site:domain.com" and do GET requests all the URL's found in the result.

        One configurable parameter exists:
            - result_limit
        """
