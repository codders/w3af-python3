"""
test_misc_settings.py

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

import pytest

from w4af.core.controllers.misc_settings import MiscSettings
from w4af.core.data.options.option_types import (
    BOOL, INT, FLOAT, STRING, URL, IPPORT, LIST,
    REGEX, COMBO, INPUT_FILE, OUTPUT_FILE, PORT, URL_LIST,
    FORM_ID_LIST)

OPTION_TYPES = (BOOL, INT, FLOAT, STRING, URL, IPPORT, LIST, REGEX, COMBO,
                INPUT_FILE, OUTPUT_FILE, PORT, URL_LIST, FORM_ID_LIST)


@pytest.mark.smoke
class TestMiscSettings(unittest.TestCase):
    def test_basic(self):
        opt_lst = MiscSettings().get_options()

        for opt in opt_lst:
            self.assertIn(opt.get_type(), OPTION_TYPES)
            self.assertTrue(opt.get_name())
            self.assertEqual(opt, opt)

            # Just verify that this doesn't crash and that the types
            # are correct
            self.assertIsInstance(opt.get_name(), str)
            self.assertIsInstance(opt.get_desc(), str)
            self.assertIsInstance(opt.get_type(), str)
            self.assertIsInstance(opt.get_help(), str)
            self.assertIsInstance(opt.get_value_str(), str)
