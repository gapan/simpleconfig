# vim:et:sta:sts=4:sw=4:ts=8:tw=79:
#
# Copyright (c) 2011-2021 George Vlahavas
#
# Written by George Vlahavas <vlahavas~at~gmail~dot~com>

__version__ = '0.3'

import collections

class SimpleConfig:
    """This is a class for managing simple configuration files with
    python. By simple, it means that they are simple text files,
    there are no sections and all options in the configuration files
    use a strict "OPTION=value" format, with no spaces between
    'OPTION', '=' and 'value'. The same 'OPTION' can be used more
    than once, so you can have multiple values.
    You can call it like this:
    from simpleconfig import SimpleConfig
    c = SimpleConfig('/path/to/configfile')
    """

    def __init__(self, configfile):
        self.configfile = configfile
        with open(configfile, 'r') as f:
            self.configopts = collections.OrderedDict()
            for line in f:
                # Yes, we don't read any commented out lines. We
                # might lose them afterwards when writing the
                # file, but I don't want to deal with that, it's
                # simpler this way.
                if line.lstrip(' ').startswith('#'):
                    pass
                else:
                    # also leave out any lines that are
                    # obviously not config lines (they don't
                    # have an = sign)
                    if '=' in line:
                        option = line.partition('=')[0]
                        value = line.partition('=')[2].replace('\n', '')
                        if option in self.configopts:
                            self.configopts[option].append(value)
                        else:
                            self.configopts[option] = [ value ]

    def get_options(self):
        """Returns a list of all available options.
        """
        return list(self.configopts.keys())

    def get(self, option):
        """Returns the first matching option in the file. Raises
        a ValueError if there is no match.
        """
        if option in self.configopts:
            return self.configopts[option][0]
        raise ValueError('No option with the name {}'.format(option))

    def get_all(self, option):
        """Returns a list of matching options in the file. This
        can be used for options that can have more than one
        values.
        Raises a ValueError if there is no match for option.
        """
        if option in self.configopts:
            return self.configopts[option]
        raise ValueError('No option with the name {}'.format(option))

    def change(self, option, oldval, newval):
        """Changes an old value of an option to a new value.
        If there are multiple matches, it changes all of them.
        Raises a ValueError if there is no match for option/oldval.
        """
        if option in self.configopts:
            if oldval in self.configopts[option]:
                for n, val in enumerate(self.configopts[option]):
                    if val == oldval:
                        self.configopts[option][n] = newval
                return
        raise ValueError('No option with the name {opt} and value {val}'
                .format(opt=option, val=oldval))

    def set(self, option, newval):
        """Assigns a new value to an existing option. If there
        are multiple options with the same name, it will only
        change the first occurence.
        Raises a ValueError if there is no match for option.
        """
        if option in self.configopts:
            self.configopts[option][0] = newval
        else:
            raise ValueError('No option with the name {}'.format(option))

    def add(self, option, value):
        """Adds a new option/value to the config."""
        if option in self.configopts:
            self.configopts[option].append(value)
        else:
            self.configopts[option] = [ value ]

    def remove(self, option, value):
        """Remove an option/value pair from the config. If there
        are multiple occurences it will remove all of them.
        Raises a ValueError if there is no match for the
        option/value pair.
        """
        found = False
        if option in self.configopts:
            if value in self.configopts[option]:
                found = True
                self.configopts[option][:] = [x for x in
                        self.configopts[option] if x != value]
            if len(self.configopts[option]) == 0:
                self.configopts.pop(option)
        if not found:
            raise ValueError('No option with the name {opt} and value {val}'
                    .format(opt=option, val=value))

    def remove_all(self, option):
        """Removes an option from the config. If multiple
        instances are found, it deletes all of them.
        """
        if option in self.configopts:
            self.configopts.pop(option)
        else:
            raise ValueError('No option with the name {}'.format(option))

    def write(self):
        """Writes configuration options back to the file."""
        with open(self.configfile, 'w') as f:
            for option in self.configopts:
                for value in self.configopts[option]:
                    f.write('{opt}={val}\n'.format(opt=option,val=value))

