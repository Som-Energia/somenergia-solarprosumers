from .projectcontroller import ProjectController
import unittest
from yamlns import namespace as ns


class ProjectController_Test(unittest.TestCase):

	def assertExceptionMessage(self, e, text):
		self.assertEqual(forceUnicode(e.args[0]), text)

	def setUp(self):
		self.maxDiff = None

	def test_init_withNiceAttributes(self):
		proj = ProjectController(
			is_paid = True,
			)
		self.assertEqual(proj.is_paid, True)
		self.assertEqual(proj.changes(), ns())

	def test_init_withBadAttribute(self):
		with self.assertRaises(AttributeError) as ctx:
			proj = ProjectController(
				im_bad = True,
				)
		self.assertEqual(format(ctx.exception), "im_bad")



# vim: noet ts=4 sw=4
