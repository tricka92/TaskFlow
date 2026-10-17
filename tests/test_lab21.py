import os
import tempfile
import unittest

from domain.models import Project, Task, Workspace
from storage.app_settings import AppSettings, load_settings, save_settings
from storage.pickle_storage import load_workspace, save_workspace
from storage.report_cache import get_report
from utils.bintree_codec import TreeNode, deserialize, serialize


class TreeCodecTests(unittest.TestCase):
    def test_empty_tree(self):
        self.assertIsNone(deserialize(serialize(None)))

    def test_single_node(self):
        self.assertEqual(deserialize(serialize(TreeNode(7))), TreeNode(7))

    def test_negative_and_big_values(self):
        t = TreeNode(-5, TreeNode(2_000_000_000), TreeNode(-2_000_000_000))
        self.assertEqual(deserialize(serialize(t)), t)

    def test_bad_header(self):
        with self.assertRaises(ValueError):
            deserialize(b"XXX\x00")

    def test_truncated(self):
        with self.assertRaises(ValueError):
            deserialize(serialize(TreeNode(1, TreeNode(2)))[:-2])

    def test_extra_bytes(self):
        with self.assertRaises(ValueError):
            deserialize(serialize(TreeNode(1)) + b"\x00")


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.p = lambda name: os.path.join(self.dir.name, name)

    def tearDown(self):
        self.dir.cleanup()

    def test_workspace_roundtrip(self):
        ws = Workspace()
        pr = Project(1, "A"); pr.add_task(Task(1, "t")); ws.add_project(pr)
        save_workspace(ws, self.p("w.pkl"))
        self.assertEqual(load_workspace(self.p("w.pkl")), ws)

    def test_missing_workspace_is_empty(self):
        self.assertEqual(load_workspace(self.p("nope.pkl")), Workspace())

    def test_settings_roundtrip_and_defaults(self):
        s = AppSettings(window_width=1280, last_project_id=3)
        save_settings(s, self.p("s.json"))
        self.assertEqual(load_settings(self.p("s.json")), s)
        self.assertEqual(load_settings(self.p("none.json")), AppSettings())

    def test_corrupted_settings(self):
        with open(self.p("s.json"), "w") as f:
            f.write("{не json")
        self.assertEqual(load_settings(self.p("s.json")), AppSettings())

    def test_cache_second_call_from_cache(self):
        pr = Project(1, "A"); pr.add_task(Task(1, "t"))
        _, first = get_report(pr, self.p("c.pkl"), delay=0)
        _, second = get_report(pr, self.p("c.pkl"), delay=0)
        self.assertFalse(first)
        self.assertTrue(second)

    def test_cache_invalidated_when_tasks_change(self):
        pr = Project(1, "A"); pr.add_task(Task(1, "t"))
        get_report(pr, self.p("c.pkl"), delay=0)
        pr.add_task(Task(2, "u"))
        _, from_cache = get_report(pr, self.p("c.pkl"), delay=0)
        self.assertFalse(from_cache)


if __name__ == "__main__":
    unittest.main()
