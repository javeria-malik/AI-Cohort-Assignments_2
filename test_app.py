import json
import os
import unittest
from unittest.mock import MagicMock

# Import functions from app
import app


class MockSessionState(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            return None

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError:
            pass


class TestTaskTracker(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_tasks.json"
        app.TASKS_FILE = self.test_file
        app.st.session_state = MockSessionState()
        app.st.session_state.tasks = []
        app.st.session_state.file_error = False
        app.st.error = MagicMock()

        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_missing_file_loads_empty_list(self):
        """Test opening the app when tasks.json is missing."""
        tasks = app.load_tasks()
        self.assertEqual(tasks, [])
        self.assertFalse(app.st.session_state.file_error)

    def test_save_and_load_tasks(self):
        """Test saving and loading valid tasks."""
        sample_tasks = [{"title": "Read Python notes", "done": False}]
        app.save_tasks(sample_tasks)
        loaded = app.load_tasks()
        self.assertEqual(loaded, sample_tasks)

    def test_add_valid_task(self):
        """Test adding a valid task."""
        app.st.session_state.tasks = []
        app.add_task("Learn Streamlit")
        self.assertEqual(len(app.st.session_state.tasks), 1)
        self.assertEqual(app.st.session_state.tasks[0], {"title": "Learn Streamlit", "done": False})

        # Verify persistence to JSON file
        with open(self.test_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data, [{"title": "Learn Streamlit", "done": False}])

    def test_add_empty_task(self):
        """Test attempting to add an empty or whitespace task."""
        app.st.session_state.tasks = []
        app.add_task("   ")
        self.assertEqual(len(app.st.session_state.tasks), 0)

    def test_complete_task(self):
        """Test marking a task as completed."""
        app.st.session_state.tasks = [
            {"title": "Task 1", "done": False},
            {"title": "Task 2", "done": False},
        ]
        app.complete_task(0)
        self.assertTrue(app.st.session_state.tasks[0]["done"])
        self.assertFalse(app.st.session_state.tasks[1]["done"])  # Other task untouched

        # Check file
        loaded = app.load_tasks()
        self.assertTrue(loaded[0]["done"])
        self.assertFalse(loaded[1]["done"])

    def test_delete_task(self):
        """Test deleting a task."""
        app.st.session_state.tasks = [
            {"title": "Task 1", "done": False},
            {"title": "Task 2", "done": True},
        ]
        app.delete_task(0)
        self.assertEqual(len(app.st.session_state.tasks), 1)
        self.assertEqual(app.st.session_state.tasks[0]["title"], "Task 2")

        # Check file
        loaded = app.load_tasks()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0]["title"], "Task 2")

    def test_corrupted_json_handling(self):
        """Test handling malformed JSON gracefully without overwriting."""
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("{ invalid json [")

        loaded = app.load_tasks()
        self.assertEqual(loaded, [])
        self.assertTrue(app.st.session_state.file_error)

        # Attempting save_tasks while file_error is True should NOT overwrite the file
        success = app.save_tasks([{"title": "New Task", "done": False}])
        self.assertFalse(success)

        # Confirm the file still has the original corrupt content preserved
        with open(self.test_file, "r", encoding="utf-8") as f:
            raw = f.read()
        self.assertEqual(raw, "{ invalid json [")

    def test_task_counts_and_isolation(self):
        """Test task counts and that modifying one task does not affect others."""
        app.st.session_state.tasks = []
        app.add_task("Task Alpha")
        app.add_task("Task Beta")
        app.add_task("Task Gamma")

        # Initial counts
        total = len(app.st.session_state.tasks)
        completed = sum(1 for t in app.st.session_state.tasks if t.get("done", False))
        pending = total - completed
        self.assertEqual(total, 3)
        self.assertEqual(completed, 0)
        self.assertEqual(pending, 3)

        # Complete only Beta (index 1)
        app.complete_task(1)
        self.assertFalse(app.st.session_state.tasks[0]["done"])
        self.assertTrue(app.st.session_state.tasks[1]["done"])
        self.assertFalse(app.st.session_state.tasks[2]["done"])

        # Check counts again
        completed = sum(1 for t in app.st.session_state.tasks if t.get("done", False))
        pending = len(app.st.session_state.tasks) - completed
        self.assertEqual(completed, 1)
        self.assertEqual(pending, 2)

        # Delete Task Alpha (index 0)
        app.delete_task(0)
        self.assertEqual(len(app.st.session_state.tasks), 2)
        self.assertEqual(app.st.session_state.tasks[0]["title"], "Task Beta")
        self.assertTrue(app.st.session_state.tasks[0]["done"])
        self.assertEqual(app.st.session_state.tasks[1]["title"], "Task Gamma")
        self.assertFalse(app.st.session_state.tasks[1]["done"])

    def test_app_restart_persists_tasks(self):
        """Test that restarting the app preserves saved tasks."""
        app.st.session_state.tasks = []
        app.add_task("Persisted Task")

        # Simulate fresh app startup
        app.st.session_state.tasks = app.load_tasks()
        self.assertEqual(len(app.st.session_state.tasks), 1)
        self.assertEqual(app.st.session_state.tasks[0]["title"], "Persisted Task")

    def test_non_list_json_handling(self):
        """Test handling JSON that is valid JSON but not a list (e.g. dict)."""
        with open(self.test_file, "w", encoding="utf-8") as f:
            json.dump({"title": "Not in a list"}, f)

        loaded = app.load_tasks()
        self.assertEqual(loaded, [])
        self.assertTrue(app.st.session_state.file_error)


if __name__ == "__main__":
    unittest.main()

