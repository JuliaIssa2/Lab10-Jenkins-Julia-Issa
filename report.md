# EECE 439 Lab 10 Report

Name: Julia Issa

## Pipeline changes

The original pipeline had Setup, Lint, Test, and Deploy stages. Setup created
a virtual environment, Lint checked style, Test ran tests, and Deploy only
printed a deployment message. I adapted the commands to Windows `bat` steps
and used `.venv\Scripts\python.exe` directly without activating the environment.

I added Coverage using coverage.py. It runs the pytest suite with branch
coverage for `app.py` and `deploy.py`, prints the results, and produces
`coverage.xml` for Jenkins to archive. Tests themselves are excluded from the
coverage measurement.

I added Security Scan using Bandit. It scans the application and deployment
script explicitly, so it does not scan the virtual environment. Findings are
printed and saved as an artifact. A nonzero Bandit exit status fails the stage.

The Deploy stage now runs `deploy.py`. It creates a local deployment folder,
copies `app.py`, executes the copied application, and compares its output with
the expected greeting. Success creates `smoke-test.txt`. Jenkins archives the
copied application and smoke-test evidence after a successful build. This is
a local deployment; no remote server is involved.

## Tests and local results

Local checks passed on Windows using Python 3.11.9 on November 21, 2026.

| Check | Observed result |
| --- | --- |
| Application | Printed `Hello, World from Julia Issa!` |
| pytest | 6 tests passed; XML test report generated |
| unittest | 6 tests passed |
| flake8 | Passed for `app.py`, `deploy.py`, and `tests` |
| Coverage | `app.py` 100%, `deploy.py` 93%, total 94% including branches |
| Coverage XML | Generated `coverage.xml` successfully |
| Bandit | No issues identified; 0 low, medium, or high findings |
| Local deployment | Copied application ran; smoke test passed |
| Deployed application | Printed the expected greeting when run directly |
| Dependency consistency | `pip check` found no broken requirements |

Coverage measured 29 statements and 6 branch exits. One statement and one
branch exit were not covered: the deployment script's command-line entry
point is run separately in the local smoke test rather than inside the pytest
coverage run. The coverage configuration excludes tests, virtual environments,
and deployment copies. Bandit scanned 32 lines of application and deployment
code without disabling checks or skipping findings.

The six unittest tests cover the World greeting, another name, an empty name,
the application entry point, a successful deployment, and rejection of
incorrect smoke-test output. The same tests can run through pytest.

## Jenkins build results

Jenkins job `Python-CI-CD` completed build **#3** on **November 21, 2026**
with final status **SUCCESS**. The build took **1 minute 27 seconds** and used
branch `main` from
[Lab10-Jenkins-Julia-Issa](https://github.com/JuliaIssa2/Lab10-Jenkins-Julia-Issa).

All six pipeline stages passed:

| Stage | Verified result |
| --- | --- |
| Setup | Passed using Python 3.11.9 |
| Lint | flake8 passed |
| Test | 6 of 6 tests passed |
| Coverage | `app.py` 100%, `deploy.py` 93%, overall 94% |
| Security Scan | Bandit found 0 security issues |
| Deploy | Local deployment succeeded and the smoke test returned PASS |

The deployed application printed `Hello, World from Julia Issa!`. Deployment
was local to the Jenkins workspace; it did not deploy to a remote server.

The build archived these artifacts:

- `coverage.xml`
- `reports/tests.xml`
- `reports/bandit.txt`
- `deployment/app.py`
- `deployment/smoke-test.txt`

## Submission status

The repository is available at
https://github.com/JuliaIssa2/Lab10-Jenkins-Julia-Issa on branch `main`.
`submission.txt` contains only this repository URL for submission.
Collaborator invitations for `NourSN2004`, `HusseinMoukalled`, and
`RanimTahmoush` have not yet been verified.
