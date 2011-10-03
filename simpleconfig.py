# Copyright (c) 2011 George Vlahavas
#
# Written by George Vlahavas <vlahavas~at~gmail~dot~com>

__version__ = '0.2'

class SimpleConfig:
	"""This is a class for managing simple configuration files with
	python. By simple, it means that they are simple text files,
	there are no sections and all options in the configuration files
	use a strict "OPTION=value" format, with no spaces between
	'OPTION', '=' and 'value'. The same 'OPTION' can be used more
	than once, so you can have multiple values. For those reasons,
	no other existing config library can be used.
	You can call it like this:
	from simpleconfig import SimpleConfig
	c = SimpleConfig('/path/to/configfile')
	"""
	def __init__(self, configfile):
		self.configfile = configfile
		f = open(configfile, 'r')
		self.configopts=[]
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
					self.configopts.append([option, value])
		f.close()

	def read(self):
		"""Returns all options/values from the config file to a
		list. The list is formatted like:
		[[option, value], [option, value]...]
		"""
		return self.configopts

	def get(self, option):
		"""Returns the first matching option in the file. Raises
		a ValueError if there is no match.
		"""
		value = None
		for i in self.read():
			if i[0] == option:
				value = i[1]
				break
		# raise an exception if there is no such option
		if value is None:
			raise ValueError('No option with the name '+option)
		return value
	
	def get_all(self, option):
		"""Returns a list of matching options in the file. This
		can be used for options that can have more than one
		values.
		Raises a ValueError if there is no match for option.
		"""
		values = []
		for i in self.read():
			if i[0] == option:
				values.append(i[1])
		# raise an exception if there is no such option
		if values == []:
			raise ValueError('No option with the name '+option)
		return values

	def change(self, option, oldval, newval):
		"""Changes an old value of an option to a new value.
		Raises a ValueError if there is no match for
		option/oldval.
		"""
		found = False
		for i in self.configopts:
			if i[0] == option and i[1] == oldval:
				i[1] = newval
				found = True
		if not found:
			raise ValueError('No option with the name '+option+' and value '+oldval)

	def set(self, option, newval):
		"""Assigns a new value to an existing option. If there
		are multiple options with the same name, it will only
		change the first occurence.
		Raises a ValueError if there is no match for
		option.
		"""
		found = False
		for i in self.configopts:
			if i[0] == option:
				i[1] = newval
				found = True
		if not found:
			raise ValueError('No option with the name '+option)
	
	def add(self, option, value):
		"""Adds a new option/value to the config."""
		self.configopts.append([option, value])

	def remove(self, option, value):
		"""Remove an otion/value pair from the config. If there
		are multiple occurences it will only remove all of them.
		Raises a ValueError if there is no match for the
		option/value pair.
		"""
		found = False
		items_to_remove = []
		for i in self.configopts:
			if i[0] == option and i[1] == value:
				items_to_remove.append(i)
				found = True
		if not found:
			raise ValueError('No option with the name '+option+' and value '+value)
		else:
			for i in items_to_remove:
				self.configopts.remove(i)

	def remove_all(self, option):
		"""Removes an option from the config. If multiple
		instances are found, it deletes all of them.
		"""
		found = False
		items_to_remove = []
		for i in self.configopts:
			if i[0] == option:
				items_to_remove.append(i)
				found = True
		if not found:
			raise ValueError('No option with the name '+option)
		else:
			for i in items_to_remove:
				self.configopts.remove(i)

	def write(self):
		"""Writes configuration options back to the file."""
		f = open(self.configfile, 'w')
		for i in self.configopts:
			f.write(i[0]+'='+i[1]+'\n')
		f.close()

