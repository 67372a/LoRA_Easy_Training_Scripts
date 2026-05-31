"""Shared utility to ensure uv is available and manage venv creation.

Called by install.py, backend/installer.py, and backend/updater.py.
Works on Windows, Linux, and Google Colab.
"""

import subprocess
import shutil
import sys
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

PLATFORM = "windows" if sys.platform == "win32" else "linux" if sys.platform == "linux" else ""


def ensure_uv() -> str:
    """Ensure uv is installed and return the path to the uv executable.

    If uv is not found on PATH, downloads and installs it using the
    standalone installer (curl on Linux, PowerShell on Windows).
    After installation, falls back to known install locations if PATH
    lookup still fails.
    """
    uv_path = shutil.which("uv")
    if uv_path:
        logger.info(f"uv found at: {uv_path}")
        return uv_path

    logger.info("uv not found, installing via standalone installer...")
    if sys.platform == "win32":
        subprocess.check_call(
            [
                "powershell",
                "-ExecutionPolicy",
                "ByPass",
                "-c",
                "irm https://astral.sh/uv/install.ps1 | iex",
            ]
        )
    else:
        subprocess.check_call(
            "curl -LsSf https://astral.sh/uv/install.sh | sh",
            shell=True,
        )

    # Re-check PATH after install
    uv_path = shutil.which("uv")
    if not uv_path:
        # Fallback: check common install locations
        if sys.platform == "win32":
            candidate = Path(os.environ.get("USERPROFILE", "")) / ".local" / "bin" / "uv.exe"
        else:
            candidate = Path.home() / ".local" / "bin" / "uv"
        if candidate.exists():
            uv_path = str(candidate)
            # Also add to current process PATH so child processes can find it
            bin_dir = str(candidate.parent)
            if bin_dir not in os.environ.get("PATH", ""):
                os.environ["PATH"] = bin_dir + os.pathsep + os.environ.get("PATH", "")

    if not uv_path:
        raise RuntimeError(
            "Failed to install uv. Please install manually: "
            "https://docs.astral.sh/uv/getting-started/installation/"
        )

    logger.info(f"uv installed at: {uv_path}")
    return uv_path


def find_existing_venv(preferred: str = "venv") -> str | None:
    """Check for an existing venv at the preferred path and `.venv`.

    Returns the path to the first existing venv found (preferred path
    is checked first), or None if no venv exists.

    Args:
        preferred: The preferred venv directory name (default: "venv").

    Returns:
        Path string to existing venv, or None.
    """
    candidates = [preferred]
    if preferred != ".venv":
        candidates.append(".venv")

    for candidate in candidates:
        python = get_venv_python(candidate)
        if python.exists():
            logger.info(f"Found existing venv at '{candidate}'")
            return candidate
    return None


def create_venv(uv: str, path: str = "venv", python_version: str = "3.11") -> str:
    """Create a virtual environment using uv, or reuse an existing one.

    Checks for an existing venv at the requested path and `.venv` before
    creating. If a venv already exists, it is reused and no new venv is
    created.

    The venv is seeded with pip, setuptools, and wheel so that pip is
    available inside the venv (matching traditional venv behavior).

    Args:
        uv: Path to the uv executable.
        path: Directory for the virtual environment (default: "venv").
        python_version: Python version to use (default: "3.11").

    Returns:
        Path string to the venv (either existing or newly created).
    """
    existing = find_existing_venv(path)
    if existing:
        logger.info(f"Reusing existing venv at '{existing}'")
        pip = get_venv_pip(existing)
        if not pip.exists():
            logger.info(f"Seeding existing venv at '{existing}' with pip/setuptools/wheel...")
            subprocess.check_call([uv, "venv", "--seed", existing])
        return existing

    logger.info(f"Creating venv at '{path}' with Python {python_version}...")
    subprocess.check_call([uv, "venv", "--python", python_version, "--seed", path])
    logger.info(f"Venv created at '{path}'")
    return path


def get_venv_python_version(venv_dir: str = "venv") -> str:
    """Detect the Python version (e.g. '3.11') from an existing venv.

    Runs the venv's python executable to query its version. Falls back
    to the current interpreter's version if the venv python is not found.

    Args:
        venv_dir: The venv directory (default: "venv").

    Returns:
        Version string like "3.11".
    """
    python = get_venv_python(venv_dir)
    if python.exists():
        try:
            result = subprocess.run(
                [str(python), "-c",
                 "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"],
                capture_output=True, text=True, timeout=10,
            )
            if result.returncode == 0:
                version = result.stdout.strip()
                logger.info(f"Detected venv Python version: {version}")
                return version
        except (subprocess.TimeoutExpired, OSError) as e:
            logger.warning(f"Failed to detect venv Python version: {e}")

    # Fallback: use current interpreter version
    version = f"{sys.version_info.major}.{sys.version_info.minor}"
    logger.warning(f"Could not detect venv Python, falling back to system Python {version}")
    return version


def get_venv_python(venv_dir: str = "venv") -> Path:
    """Get the path to the Python executable inside the venv.

    Args:
        venv_dir: The venv directory (default: "venv").

    Returns:
        Path to python executable.
    """
    if sys.platform == "win32":
        return Path(venv_dir) / "Scripts" / "python.exe"
    return Path(venv_dir) / "bin" / "python"


def get_venv_pip(venv_dir: str = "venv") -> Path:
    """Get the path to pip inside the venv.

    Args:
        venv_dir: The venv directory (default: "venv").

    Returns:
        Path to pip executable.
    """
    if sys.platform == "win32":
        return Path(venv_dir) / "Scripts" / "pip.exe"
    return Path(venv_dir) / "bin" / "pip"


def uv_pip_install(uv: str, *args: str, venv_path: str = "venv") -> None:
    """Run 'uv pip install' with the given arguments, targeting a venv.

    Uses the venv directory path for --python so uv recognizes it as a
    virtual environment and scopes all package operations to it.

    Args:
        uv: Path to the uv executable.
        *args: Additional arguments passed to 'uv pip install'.
        venv_path: Path to the venv directory (default: "venv").
    """
    cmd = [uv, "pip", "install", "--python", str(Path(venv_path)), *args]
    logger.info(f"Running: {' '.join(cmd)}")
    subprocess.check_call(cmd)
