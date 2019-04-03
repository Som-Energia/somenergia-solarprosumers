from .projectcontroller import ProjectController
import unittest
from yamlns import namespace as ns


class ProjectController_Test(unittest.TestCase):

	def setUp(self):
		self.maxDiff = None

	def test_getattr(self):
		proj = ProjectController(
			is_paid = True,
			)
		self.assertEqual(proj.is_paid, True)
		self.assertEqual(proj.changes(), ns())


# vim: noet ts=4 sw=4
