from . import projectcontroller
import unittest


class ProjectController_Test(unittest.TestCase):

	def setUp(self):
		self.maxDiff = None

	def setupProject(self, **kwds):
		project = projectcontroller.ProjectController(**kwds)
		return project

	def test_getattr(self):
		proj = self.setupProject(
			is_paid = True,
			)
		self.assertEqual(proj.is_paid, True)


# vim: noet ts=4 sw=4
