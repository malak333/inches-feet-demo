# inches-feet-demo

Repository for an inches/feet conversion application built with Assemblywright.

This repository is initialized for reviewed feature publication. Application code
has not yet been published.

## Validation and publication

Changes reach `main` through pull requests. The required **Windows Python
validation** check must pass against the current base branch, including for
administrators. Assemblywright independently reviews generated features before
requesting publication and merges only after required checks pass.

CI uses Python 3.12 on Windows. It tests its validation runner, installs
`requirements.txt` when present, checks Python syntax, and runs the application's
`unittest` suite under `tests/`. Qt tests use `QT_QPA_PLATFORM=offscreen`.
Python application code without discovered passing tests is rejected.

Until application code is published, CI validates only this exact repository
scaffold. A successful scaffold check does not claim application test coverage.
