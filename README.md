##UV
uv is a fast Python package and project manager from Astral. It can handle virtual environments, Python versions, dependencies, and dependency locking, replacing much of the traditional pip + venv workflow.

Install uv once on your system:

curl -LsSf https://astral.sh/uv/install.sh | sh

Then initialize it inside each project:

cd my-project
uv init

For an existing simple project, uv init --no-package can also be useful.

Add dependencies with:

uv add requests

Run Python inside the project's managed environment with:

uv run python main.py

uv manages the project's .venv, records dependencies in pyproject.toml, and creates uv.lock so the same dependency versions can be reproduced elsewhere.

After cloning an existing uv project, set it up with:

uv sync
