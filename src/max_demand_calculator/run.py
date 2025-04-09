# run.py
import os
import sys
import subprocess
from pathlib import Path

def is_poetry_environment():
    # Check via env var or if using .venv path
    return os.getenv("POETRY_ACTIVE") == "1" or ".venv" in sys.executable

def relaunch_with_poetry(script_path: Path):
    print("♻️  Relaunching using Poetry environment...")
    project_root = script_path.parents[2]  # Go up to project root
    os.chdir(project_root)

    try:
        result = subprocess.run(
            ["poetry", "run", "python", str(script_path)],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"❌ Poetry relaunch failed: {e}")
    sys.exit(0)

if __name__ == "__main__":
    this_script = Path(__file__).resolve()

    if not is_poetry_environment():
        relaunch_with_poetry(this_script)

    # ✅ Safe to import after environment confirmed
    import streamlit.web.cli as stcli

    app_path = this_script.parent / "e_app.py"

    if not app_path.exists():
        print("❌ ERROR: Could not find e_app.py in the same directory as run.py.")
        sys.exit(1)

    print("🚀 Launching the Max Demand Calculator App... This will open in your browser.")
    sys.argv = ["streamlit", "run", str(app_path)]
    sys.exit(stcli.main())