import io
import runpy
import shutil
from contextlib import redirect_stdout
from pathlib import Path


def deploy(destination=None):
    project = Path(__file__).resolve().parent
    destination = Path(destination) if destination else project / "deployment"
    destination.mkdir(parents=True, exist_ok=True)
    evidence_path = destination / "smoke-test.txt"
    evidence_path.unlink(missing_ok=True)
    deployed_app = destination / "app.py"
    shutil.copy2(project / "app.py", deployed_app)

    output = io.StringIO()
    with redirect_stdout(output):
        runpy.run_path(str(deployed_app), run_name="__main__")
    expected = "Hello, World from Julia Issa!"
    if output.getvalue().strip() != expected:
        raise RuntimeError("The deployed application failed its smoke test.")

    evidence = (
        f"Local deployment: {deployed_app}\n"
        f"Smoke test: PASS\n{expected}\n"
    )
    evidence_path.write_text(evidence, encoding="utf-8")
    print(evidence, end="")
    return deployed_app


if __name__ == "__main__":
    deploy()
