from yamlns import namespace as ns


class ProjectController:

	_allowed = [
		'is_paid',
	]

	def __init__(self, **kwds):
		for name in kwds:
			if name not in self._allowed:
				raise AttributeError(name)
		for name, value in kwds.items():
			setattr(self, name, value)

	def __setattr__(self, name, value):
		if name not in self._allowed:
			raise AttributeError(name)
		return super(ProjectController, self)
			.__setattr__(name, value)
		raise AttributeError(name)

	def changes(self):
		return ns()



# vim: noet ts=4 sw=4
