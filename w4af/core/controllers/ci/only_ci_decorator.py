"""
only_ci_decorator.py

Copyright 2013 Andres Riancho

This file is part of w4af, https://w4af.net/ .

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
from functools import wraps
from w4af.core.controllers.ci.detect import is_running_on_ci


def only_ci(decorated_func):
    """
    This decorator runs the function that's being decorated only if the code
    is being run in CI environment.
    """
    @wraps(decorated_func)
    def _inner_func(*args, **kwds):
        if is_running_on_ci():
            return decorated_func(*args, **kwds)
    
    return _inner_func