"""
info_set.py

Copyright 2015 Andres Riancho

This file is part of w3af, http://w3af.org/ .

w3af is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

w3af is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with w3af; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""
import textwrap

from jinja2 import Template, StrictUndefined

from w3af.core.data.fuzzer.mutants.empty_mutant import EmptyMutant
from w3af.core.data.kb.info import Info


class InfoSet(object):
    """
    This class represents a set of Info instances which are grouped together
    by the plugin developer.

    The inspiration for this class comes from vulnerabilities like cross-domain
    javascript where Info instances can be grouped by a common attribute such
    as the remote domain.

    This class allows us to represent this sentence:
        "The target application includes javascript source from the insecure
         domain foo.com, the URLs where this was found are <long list here>"

    Representing the same without this class would look like:
        "The target application includes javascript source from the insecure
         domain foo.com, the vulnerable URL is X"
        ...
        "The target application includes javascript source from the insecure
         domain foo.com, the vulnerable URL is N"

    First I thought about adding these features directly to the Info class, but
    it would have been harder to refactor the whole code and the end result
    would have been difficult to read.

    Note that:
        * It can hold both Info and Vuln instances.

        * It's going to use the first Info instance to retrieve important things
          such as severity, name, description, etc. Those should all be common
          to the set being hold here.

    :see: https://github.com/andresriancho/w3af/issues/3955
    """
    TEMPLATE = None
    ITAG = None

    def __init__(self, info_instances):
        if not len(info_instances):
            raise ValueError('Empty InfoSets are not allowed')

        if not isinstance(info_instances, list):
            raise TypeError('info_instances must be a list')

        for info in info_instances:
            if not isinstance(info, Info):
                raise TypeError('info_instances list items must be Info sub'
                                '-classes, found "%r" instead' % info)

        self.infos = info_instances
        self._mutant = EmptyMutant()

    def add(self, info):
        self.infos.append(info)

    def extend(self, infos):
        self.infos.extend(infos)

    @property
    def first_info(self):
        return self.infos[0]

    def get_name(self):
        return self.first_info.get_name()

    def get_desc(self, with_id=False):
        if self.TEMPLATE is None:
            return self.first_info.get_desc(with_id=with_id)

        # We render the template using the information set data
        context = {'urls': [str(u) for u in self.get_urls()],
                   'uris': [str(u) for u in self.get_uris()],
                   'severity': self.get_severity(),
                   'name': self.get_name(),
                   'id': self.get_id(),
                   'method': self.get_method(),
                   'plugin': self.get_plugin_name()}
        context.update(self.first_info.items())

        template = Template(textwrap.dedent(self.TEMPLATE),
                            undefined=StrictUndefined,
                            trim_blocks=True,
                            lstrip_blocks=True)
        return template.render(context)

    def get_id(self):
        all_ids = []
        for info in self.infos:
            all_ids.extend(info.get_id())
        return list(set(all_ids))

    def get_urls(self):
        all_urls = []
        for info in self.infos:
            all_urls.append(info.get_url())
        return list(set(all_urls))

    def get_uris(self):
        all_urls = []
        for info in self.infos:
            all_urls.append(info.get_uri())
        return list(set(all_urls))

    def get_mutant(self):
        """
        :return: An EmptyMutant instance. Note that there is no setter for
                 self._mutant, this is correct since we always want to return
                 an empty mutant

                 This method was added mostly to ease the initial implementation
                 and avoid major changes in output plugins which were already
                 handling Info instances.
        """
        return self._mutant

    def get_method(self):
        return self.first_info.get_method()

    def get_url(self):
        """
        :return: One of the potentially many URLs which are related to this
                 InfoSet. Use with care, usually as an example of a vulnerable
                 URL to show to the user.

                 For the complete list of URLs see get_urls()
        """
        return self.first_info.get_url()

    def get_uri(self):
        """
        :return: One of the potentially many URIs which are related to this
                 InfoSet. Use with care, usually as an example of a vulnerable
                 URL to show to the user.

                 For the complete list of URLs see get_uris()
        """
        return self.first_info.get_uri()

    def get_plugin_name(self):
        return self.first_info.get_plugin_name()

    def get_token_name(self):
        """
        :return: None, since the Info objects stored in this InfoSet might have
                 completely different values for it, and it's not possible to
                 return one that represents all.
        """
        return None

    def get_token(self):
        """
        :return: None, since the Info objects stored in this InfoSet might have
                 completely different values for it, and it's not possible to
                 return one that represents all.
        """
        return None

    def get_uniq_id(self):
        """
        :return: A uniq identifier for this InfoSet instance. Since InfoSets are
                 persisted to SQLite and then re-generated for showing them to
                 the user, we can't use id() to know if two info objects are
                 the same or not.
        """
        concat_all = ''

        for info in self.infos:
            concat_all += info.get_uniq_id()

        return str(hash(concat_all))

    def get_attribute(self, attr_name):
        return self.first_info.get(attr_name, None)

    def __getitem__(self, item):
        """
        Does the same as get_attribute but with a different signature, had to
        add it to make the InfoSet behave more like an Info
        """
        return self.first_info[item]

    def get_severity(self):
        return self.first_info.get_severity()

    def match(self, info):
        """
        When an Info sub-class wants to know if it should be added to an InfoSet
        it calls InfoSet.match(Info).

        In case it's not clear, this is the method which controls how Infos are
        grouped in InfoSets.

        :param info: The Info instance which wants to know if it matches this
                     InfoSet

        :return: True if they do match
        """
        assert self.ITAG is not None, 'Need to specify unique id tag'
        return info[self.ITAG] == self.get_attribute(self.ITAG)

    def __eq__(self, other):
        return self.get_uniq_id() == other.get_uniq_id()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return '<info_set instance for: "%s" - len: %s>' % (self.get_name(),
                                                            len(self.infos))
