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

    def setupProject(self, **kwds):
        kwds.setdefault('log', ['previous content'])
        return ProjectController(**kwds)

    def assertActionResult(self, proj, expectedChanges, addedLog=None):
        changes = ns(proj.changes())
        self.assertNsEqual(changes, expectedChanges)
        expectedLog = ns(log=['previous content'])
        if addedLog is not None:
            if addedLog:
                expectedLog.log.append(ns.loads(addedLog))
            self.assertNsEqual(expectedLog, ns(log=proj.log))

    def test_addlog_whenEmpty(self):
        proj = self.setupProject()
        self.assertActionResult(proj, {}, {})

    def test_addlog_single(self):
        proj = self.setupProject()
        proj.addlog(
            action='test',
            date=isodate('2019-01-01'),
            key='value'
            )
        self.assertActionResult(proj, {}, """
            action: test
            date: 2019-01-01
            key: value
            """)

    def test_preregister(self):
        proj = self.setupProject()
        proj.preregister(
            current_date = isodate('2019-02-01'),
            member_id = 200,
            contract_id = None, # 400
            campaign_id = 2,
        )
        self.assertActionResult(proj, """
            status: preregistered
            is_paid: false
            registration_date: 2019-02-01
        """)







# vim: et ts=4 sw=4
