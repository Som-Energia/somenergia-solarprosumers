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

	def changes(self):
		return ns()



# vim: noet ts=4 sw=4
