from .projectcontroller import ProjectController
import unittest
from yamlns import namespace as ns
import datetime


def isodate(isodatestring):
    return datetime.datetime.strptime(isodatestring, "%Y-%m-%d").date()


class StateController_Test(unittest.TestCase):

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


	def test_getattr_badAttribute(self):
		proj = ProjectController()
		with self.assertRaises(AttributeError) as ctx:
			value = proj.im_bad
		self.assertEqual(format(ctx.exception), "im_bad")

	def test_setattr_badAttribute(self):
		proj = ProjectController()
		with self.assertRaises(AttributeError) as ctx:
			proj.im_bad = True
		self.assertEqual(format(ctx.exception), "im_bad")

	def test_setattr_properAttribute(self):
		proj = ProjectController(is_paid=False)
		proj.is_paid = True
		self.assertEqual(proj.is_paid, True)
		self.assertEqual(proj.changes(), ns(is_paid=True))


class ProjectController_Test(unittest.TestCase):

	from .testutils import assertNsEqual

	def test_preregister(self):
		proj = ProjectController()
		proj.preregister(
			current_date = isodate('2019-02-01'),
			member_id = 200,
			contract_id = None, # 400
			campaign_id = 2,
		)
		self.assertNsEqual(proj.changes(), """
is_paid: false
registration_date: 2019-02-01
""")








# vim: noet ts=4 sw=4
