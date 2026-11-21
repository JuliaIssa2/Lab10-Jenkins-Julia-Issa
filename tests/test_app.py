import io
import runpy
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from app import greet
from deploy import deploy


class TestApp(unittest.TestCase):
    def test_greet_world(self):
        self.assertEqual(greet("World"), "Hello, World from Julia Issa!")

    def test_greet_name(self):
        self.assertEqual(greet("Julia"), "Hello, Julia from Julia Issa!")

    def test_greet_empty_name(self):
        self.assertEqual(greet(""), "Hello,  from Julia Issa!")

    def test_app_main(self):
        output = io.StringIO()
        with redirect_stdout(output):
            runpy.run_path("app.py", run_name="__main__")
        self.assertEqual(output.getvalue(), "Hello, World from Julia Issa!\n")

    def test_local_deployment(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "deployment"
            with redirect_stdout(io.StringIO()):
                deployed_app = deploy(destination)
            self.assertEqual(
                deployed_app.read_text(encoding="utf-8"),
                Path("app.py").read_text(encoding="utf-8"),
            )
            evidence = destination / "smoke-test.txt"
            self.assertIn("Smoke test: PASS", evidence.read_text())

    def test_deployment_rejects_bad_output(self):
        with tempfile.TemporaryDirectory() as directory:
            evidence = Path(directory) / "smoke-test.txt"
            evidence.write_text("Smoke test: PASS", encoding="utf-8")
            with patch("deploy.runpy.run_path"):
                with self.assertRaises(RuntimeError):
                    deploy(directory)
            self.assertFalse(evidence.exists())


if __name__ == "__main__":
    unittest.main()
