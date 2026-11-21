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
- `report.md`: changes, verification results, and Jenkins execution status.
- `submission.txt`: replace the marked placeholder after creating the repository.
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

## Prepare GitHub

GitHub CLI was not found in this session. Create a repository named
`Lab10-Jenkins-Julia-Issa` under `JuliaIssa2` on GitHub, with no initial README,
license, or gitignore. Then run these commands from this folder:

```powershell
git branch -M main
git add .gitignore .coveragerc app.py deploy.py tests/test_app.py requirements.txt Jenkinsfile_Julia_Issa README.md report.md submission.txt
git commit -m "Complete Jenkins CI/CD lab"
git remote add origin https://github.com/JuliaIssa2/Lab10-Jenkins-Julia-Issa.git
git push -u origin main
```

Use Git's normal sign-in prompt; keep credentials out of project files. After
verifying the repository opens on GitHub, put its actual URL alone in
`submission.txt`, commit that change, and push it. The suggested URL above is
not confirmation that a repository exists.

In the repository, open **Settings > Collaborators > Add people** and invite
`NourSN2004`, `HusseinMoukalled`, and `RanimTahmoush`. Verify each invitation is
listed. No invitations have been sent by this project setup.

## Configure Jenkins

1. Open `http://localhost:8080/` and sign in locally.
2. Choose **New Item**, enter `Python-CI-CD`, choose **Pipeline**, and click **OK**.
3. Under **Pipeline**, choose **Pipeline script from SCM**, then **Git**.
4. Set the repository URL to your verified GitHub repository URL. For the
   suggested repository it is
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
10. Update `report.md` with the actual build number, result, and observed output,
    then commit and push. Submit `submission.txt` as required by the lab.

Jenkins API access returned HTTP 403 in this session. No authenticated Jenkins
build or Jenkins declarative linter validation has been performed. Both remain
**Pending Jenkins execution**. Local checks do not prove the Jenkins job passes.

Pipeline reference: [Jenkins declarative syntax](https://www.jenkins.io/doc/book/pipeline/syntax/).
