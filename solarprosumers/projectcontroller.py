from yamlns import namespace as ns


class ProjectController:

	_allowed = [
		'is_paid',
	]

	def _checkAttribute(self, name):
		if name not in self._allowed:
			raise AttributeError(name)

		

	def __init__(self, **kwds):
		self._changes = ns()
		self._values = ns(kwds)
		for name in kwds:
			self._checkAttribute(name)

	def __setattr__(self, name, value):
		if not name.startswith('_'):
			self._checkAttribute(name)
			self._changes[name]=value
			self._values[name]=value
		return super(ProjectController, self).__setattr__(name, value)

	def __getattr__(self, name):
		self._checkAttribute(name)
		return self._values[name]

	def changes(self):
		return self._changes



# vim: noet ts=4 sw=4
