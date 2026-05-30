from pathlib import Path
from sys import platform
from subprocess import check_call
import json
import os

from install_uv import ensure_uv, uv_pip_install, find_existing_venv

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def main():
    uv = ensure_uv()
    venv_path = find_existing_venv("venv") or "venv"

    uv_pip_install(uv, "-U", "-r", "requirements.txt", venv_path=venv_path)
    config = Path("config.json")
    config_dict = json.loads(config.read_text()) if config.exists() else {}
    if "run_local" in config_dict and config_dict["run_local"]:
        check_call("git submodule update --init --recursive", shell=platform == "linux")
        os.chdir("backend")
        check_call(
            f"{sys.executable} updater.py",
            shell=platform == "linux",
        )


if __name__ == "__main__":
    import sys
    main()
