# EECE 439 Lab 10 Jenkins for DevOps Automation

Julia Issa's Python project prints `Hello, World from Julia Issa!` and uses a
Windows Jenkins pipeline to check and deploy it locally. It uses Python 3.11,
unittest, pytest, flake8, coverage.py, Bandit, Git, and Jenkins.

## Files

- `app.py`: greeting function and command-line entry point.
- `tests/test_app.py`: unittest tests, also collected by pytest.
- `deploy.py`: copies the application to `deployment/`, runs it, and records
  a smoke test in `deployment/smoke-test.txt`.
- `requirements.txt`: pinned development dependencies.
- `.coveragerc`: measures project source, excluding tests and generated copies.
- `Jenkinsfile_Julia_Issa`: declarative Windows pipeline.
- `Lab10_Julia_Issa_Final_Report.docx`: changes, verification results, and Jenkins execution status.
- `submission.txt`: verified GitHub repository URL for submission.
- `.gitignore`: excludes environments, generated files, and common secrets.

## Run locally in PowerShell

From the project root, use an installed Python 3.11 executable to create the
environment. If the Windows Python launcher works:

```powershell
py -3.11 -m venv .venv
```

Alternatively, use the existing Python installation by its full path:

```powershell
& 'C:\Users\Acer\AppData\Local\Programs\Python\Python311\python.exe' -m venv .venv
```

Then run the checks without activating the environment:

```powershell
& '.\.venv\Scripts\python.exe' -m pip install -r requirements.txt
& '.\.venv\Scripts\python.exe' app.py
& '.\.venv\Scripts\python.exe' -m pytest -v
& '.\.venv\Scripts\python.exe' -m unittest discover -s tests -v
& '.\.venv\Scripts\python.exe' -m flake8 app.py deploy.py tests
& '.\.venv\Scripts\python.exe' -m coverage run -m pytest -v
& '.\.venv\Scripts\python.exe' -m coverage report -m
& '.\.venv\Scripts\python.exe' -m coverage xml -o coverage.xml
& '.\.venv\Scripts\python.exe' -m bandit app.py deploy.py
& '.\.venv\Scripts\python.exe' deploy.py
```

Deployment only copies into the local `deployment` folder. The smoke test runs
that copied application and checks its exact greeting. A failed check raises
an error. No remote deployment is performed.

## Pipeline stages

1. **Setup** creates `.venv`, displays Python and pip versions, and installs dependencies.
2. **Lint** checks application, deployment script, and tests with flake8.
3. **Test** runs verbose pytest tests and writes an XML test report.
4. **Coverage** reruns tests with branch coverage, prints a report, and writes `coverage.xml`.
5. **Security Scan** scans `app.py` and `deploy.py` with Bandit and displays its report.
6. **Deploy** copies and smoke-tests the application locally.

Every command runs in its own Jenkins `bat` step so a nonzero exit status fails
the build. Report artifacts are archived even when a stage fails. Deployment
artifacts are archived only after success. No extra workspace-cleanup or test
report plugin is required. The workspace is retained for inspection.

## GitHub repository

Repository: [Lab10-Jenkins-Julia-Issa](https://github.com/JuliaIssa2/Lab10-Jenkins-Julia-Issa)

Branch: `main`. The repository URL is recorded in `submission.txt`.

In the repository, open **Settings > Collaborators > Add people** and invite
`NourSN2004`, `HusseinMoukalled`, and `RanimTahmoush` if needed. These invitations
have not yet been verified; check their status before considering them complete.

## Verified Jenkins build

Job `Python-CI-CD`, build **#3**, finished with **SUCCESS** on
**November 21, 2026**, in **1 minute 27 seconds** using branch `main`.
All six stages passed: Setup used Python 3.11.9, flake8 passed, all 6 tests
passed, coverage was 100% for `app.py`, 93% for `deploy.py`, and 94% overall,
Bandit found 0 security issues, and local deployment succeeded.

The smoke test returned **PASS**, and the application printed
`Hello, World from Julia Issa!`. Deployment was local to the Jenkins workspace;
no remote server was used.

The build archived `coverage.xml`, `reports/tests.xml`, `reports/bandit.txt`,
`deployment/app.py`, and `deployment/smoke-test.txt`. See `Lab10_Julia_Issa_Final_Report.docx` for the
stage results.

## Configure Jenkins

1. Open `http://localhost:8080/` and sign in locally.
2. Choose **New Item**, enter `Python-CI-CD`, choose **Pipeline**, and click **OK**.
3. Under **Pipeline**, choose **Pipeline script from SCM**, then **Git**.
4. Set the repository URL to
   `https://github.com/JuliaIssa2/Lab10-Jenkins-Julia-Issa.git`.
5. Set the branch specifier to `*/main` and Script Path to
   `Jenkinsfile_Julia_Issa`. Save the job.
6. Run on a Windows node. The Jenkins service account needs permission to run
   Python and Git, write to its workspace, and download packages. For a private
   repository, select credentials stored in Jenkins through its UI.
7. The default `PYTHON_EXE` is `py`, which uses `py -3.11`. If that is unavailable
   to the service, first run the job to load its parameters, then use **Build
   with Parameters** and set `PYTHON_EXE` to an absolute Python 3.11 executable
   path. The existing installation path is
   `C:\Users\Acer\AppData\Local\Programs\Python\Python311\python.exe`; confirm the
   service account can access it. Do not include quote characters in the value.
8. Click **Build Now** or **Build with Parameters**. Open the build number and
   **Console Output**. Verify Setup, Lint, Test, Coverage, Security Scan, and
   Deploy all finish successfully and the build ends with `Finished: SUCCESS`.
9. Inspect the archived `coverage.xml`, `reports/tests.xml`, `reports/bandit.txt`,
   `deployment/app.py`, and `deployment/smoke-test.txt`.
10. For future builds, update `Lab10_Julia_Issa_Final_Report.docx` with the actual results as needed.
    Submit `submission.txt` as required by the lab.

Pipeline reference: [Jenkins declarative syntax](https://www.jenkins.io/doc/book/pipeline/syntax/).
