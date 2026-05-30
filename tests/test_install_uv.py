"""Tests for install_uv.py - uv bootstrap and venv management utilities.

Unit tests use mocking to verify logic without actual installations.
Functional tests exercise real uv operations (require network + uv availability).
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path
from unittest import mock

import pytest

# Ensure the project root is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import install_uv


# ---------------------------------------------------------------------------
# Unit Tests – get_venv_python / get_venv_pip
# ---------------------------------------------------------------------------

class TestGetVenvPython:
    """Test get_venv_python returns correct platform-specific paths."""

    def test_default_venv_dir_windows(self):
        with mock.patch.object(sys, "platform", "win32"):
            result = install_uv.get_venv_python()
        assert result == Path("venv/Scripts/python.exe")

    def test_default_venv_dir_linux(self):
        with mock.patch.object(sys, "platform", "linux"):
            result = install_uv.get_venv_python()
        assert result == Path("venv/bin/python")

    def test_custom_venv_dir_windows(self):
        with mock.patch.object(sys, "platform", "win32"):
            result = install_uv.get_venv_python("my_venv")
        assert result == Path("my_venv/Scripts/python.exe")

    def test_custom_venv_dir_linux(self):
        with mock.patch.object(sys, "platform", "linux"):
            result = install_uv.get_venv_python("my_venv")
        assert result == Path("my_venv/bin/python")


class TestGetVenvPip:
    """Test get_venv_pip returns correct platform-specific paths."""

    def test_default_venv_dir_windows(self):
        with mock.patch.object(sys, "platform", "win32"):
            result = install_uv.get_venv_pip()
        assert result == Path("venv/Scripts/pip.exe")

    def test_default_venv_dir_linux(self):
        with mock.patch.object(sys, "platform", "linux"):
            result = install_uv.get_venv_pip()
        assert result == Path("venv/bin/pip")

    def test_custom_venv_dir_windows(self):
        with mock.patch.object(sys, "platform", "win32"):
            result = install_uv.get_venv_pip("my_venv")
        assert result == Path("my_venv/Scripts/pip.exe")

    def test_custom_venv_dir_linux(self):
        with mock.patch.object(sys, "platform", "linux"):
            result = install_uv.get_venv_pip("my_venv")
        assert result == Path("my_venv/bin/pip")


# ---------------------------------------------------------------------------
# Unit Tests – ensure_uv
# ---------------------------------------------------------------------------

class TestEnsureUv:
    """Test ensure_uv bootstrapping logic."""

    @mock.patch("shutil.which", return_value="/usr/bin/uv")
    def test_returns_path_when_uv_found(self, mock_which):
        result = install_uv.ensure_uv()
        assert result == "/usr/bin/uv"
        mock_which.assert_called_once_with("uv")

    @mock.patch("install_uv.subprocess.check_call")
    @mock.patch("install_uv.Path")
    @mock.patch.dict(os.environ, {"PATH": "/usr/bin"})
    @mock.patch("shutil.which")
    def test_installs_uv_on_linux_when_not_found(self, mock_which, mock_path, mock_check_call):
        # First call returns None (not found), second call returns path after install
        mock_which.side_effect = [None, "/home/user/.local/bin/uv"]
        with mock.patch.object(sys, "platform", "linux"):
            result = install_uv.ensure_uv()
        assert result == "/home/user/.local/bin/uv"
        mock_check_call.assert_called_once()
        call_args = mock_check_call.call_args
        assert "curl" in call_args[0][0]

    @mock.patch("install_uv.subprocess.check_call")
    @mock.patch("install_uv.Path")
    @mock.patch.dict(os.environ, {"PATH": "C:\\Users\\test\\bin"})
    @mock.patch("shutil.which")
    def test_installs_uv_on_windows_when_not_found(self, mock_which, mock_path, mock_check_call):
        mock_which.side_effect = [None, "C:\\Users\\test\\.local\\bin\\uv.exe"]
        with mock.patch.object(sys, "platform", "win32"):
            result = install_uv.ensure_uv()
        assert result == "C:\\Users\\test\\.local\\bin\\uv.exe"
        mock_check_call.assert_called_once()
        call_args = mock_check_call.call_args
        assert "powershell" in call_args[0][0]

    @mock.patch("install_uv.subprocess.check_call")
    @mock.patch.dict(os.environ, {"PATH": "/usr/bin"})
    @mock.patch("shutil.which", return_value=None)
    def test_raises_runtime_error_when_install_fails(self, mock_which, mock_check_call):
        with mock.patch.object(sys, "platform", "linux"):
            with pytest.raises(RuntimeError, match="Failed to install uv"):
                install_uv.ensure_uv()


# ---------------------------------------------------------------------------
# Unit Tests – create_venv
# ---------------------------------------------------------------------------

class TestCreateVenv:
    """Test create_venv calls uv with correct arguments."""

    @mock.patch("install_uv.find_existing_venv", return_value=None)
    @mock.patch("install_uv.subprocess.check_call")
    def test_default_args(self, mock_check_call, mock_find):
        result = install_uv.create_venv("/usr/bin/uv")
        mock_check_call.assert_called_once_with(
            ["/usr/bin/uv", "venv", "--python", "3.11", "--seed", "venv"]
        )
        assert result == "venv"

    @mock.patch("install_uv.find_existing_venv", return_value=None)
    @mock.patch("install_uv.subprocess.check_call")
    def test_custom_args(self, mock_check_call, mock_find):
        result = install_uv.create_venv("/usr/bin/uv", path="my_env", python_version="3.12")
        mock_check_call.assert_called_once_with(
            ["/usr/bin/uv", "venv", "--python", "3.12", "--seed", "my_env"]
        )
        assert result == "my_env"

    @mock.patch("install_uv.subprocess.check_call")
    def test_reuses_existing_venv_with_pip(self, mock_check_call):
        """If an existing venv is found with pip, skip creation and seeding."""
        with mock.patch("install_uv.find_existing_venv", return_value="venv"):
            with mock.patch("install_uv.get_venv_pip", return_value=Path("venv/Scripts/pip.exe")):
                with mock.patch.object(Path, "exists", return_value=True):
                    result = install_uv.create_venv("/usr/bin/uv")
        assert result == "venv"
        mock_check_call.assert_not_called()

    @mock.patch("install_uv.subprocess.check_call")
    def test_reuses_dot_venv(self, mock_check_call):
        """If .venv is found with pip, reuse it."""
        with mock.patch("install_uv.find_existing_venv", return_value=".venv"):
            with mock.patch("install_uv.get_venv_pip", return_value=Path(".venv/bin/pip")):
                with mock.patch.object(Path, "exists", return_value=True):
                    result = install_uv.create_venv("/usr/bin/uv")
        assert result == ".venv"
        mock_check_call.assert_not_called()

    @mock.patch("install_uv.subprocess.check_call")
    def test_seeds_existing_venv_without_pip(self, mock_check_call):
        """If existing venv lacks pip, seed it with uv venv --seed."""
        mock_pip_path = mock.MagicMock(spec=Path)
        mock_pip_path.exists.return_value = False
        with mock.patch("install_uv.find_existing_venv", return_value="venv"):
            with mock.patch("install_uv.get_venv_pip", return_value=mock_pip_path):
                result = install_uv.create_venv("/usr/bin/uv")
        assert result == "venv"
        mock_check_call.assert_called_once_with(
            ["/usr/bin/uv", "venv", "--seed", "venv"]
        )


# ---------------------------------------------------------------------------
# Unit Tests – find_existing_venv
# ---------------------------------------------------------------------------

class TestFindExistingVenv:
    """Test find_existing_venv detects existing venvs."""

    def test_returns_none_when_no_venv_exists(self, tmp_path):
        """No venv directories exist."""
        import os
        old_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            result = install_uv.find_existing_venv("venv")
            assert result is None
        finally:
            os.chdir(old_cwd)

    def test_finds_venv_at_preferred_path(self, tmp_path):
        """Detects venv at the preferred 'venv' path."""
        import os
        old_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            # Create a fake venv with just the python executable
            python = install_uv.get_venv_python("venv")
            python.parent.mkdir(parents=True)
            python.touch()

            result = install_uv.find_existing_venv("venv")
            assert result == "venv"
        finally:
            os.chdir(old_cwd)

    def test_finds_dot_venv_as_fallback(self, tmp_path):
        """Detects .venv when preferred 'venv' doesn't exist."""
        import os
        old_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            python = install_uv.get_venv_python(".venv")
            python.parent.mkdir(parents=True)
            python.touch()

            result = install_uv.find_existing_venv("venv")
            assert result == ".venv"
        finally:
            os.chdir(old_cwd)

    def test_prefers_venv_over_dot_venv(self, tmp_path):
        """When both exist, prefers 'venv' over '.venv'."""
        import os
        old_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            for name in ("venv", ".venv"):
                python = install_uv.get_venv_python(name)
                python.parent.mkdir(parents=True)
                python.touch()

            result = install_uv.find_existing_venv("venv")
            assert result == "venv"
        finally:
            os.chdir(old_cwd)

    def test_custom_preferred_path(self, tmp_path):
        """Checks custom preferred path first."""
        import os
        old_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            python = install_uv.get_venv_python("my_env")
            python.parent.mkdir(parents=True)
            python.touch()

            result = install_uv.find_existing_venv("my_env")
            assert result == "my_env"
        finally:
            os.chdir(old_cwd)

    def test_skips_venv_without_python(self, tmp_path):
        """A venv directory without python executable is not detected."""
        import os
        old_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            Path("venv").mkdir()
            # No python executable created
            result = install_uv.find_existing_venv("venv")
            assert result is None
        finally:
            os.chdir(old_cwd)


# ---------------------------------------------------------------------------
# Unit Tests – uv_pip_install
# ---------------------------------------------------------------------------

class TestUvPipInstall:
    """Test uv_pip_install constructs correct commands."""

    @mock.patch("install_uv.subprocess.check_call")
    def test_basic_install(self, mock_check_call):
        install_uv.uv_pip_install("/usr/bin/uv", "-r", "requirements.txt")
        mock_check_call.assert_called_once_with(
            ["/usr/bin/uv", "pip", "install", "--python", "venv", "-r", "requirements.txt"]
        )

    @mock.patch("install_uv.subprocess.check_call")
    def test_custom_venv_path(self, mock_check_call):
        install_uv.uv_pip_install(
            "/usr/bin/uv", "-U", "torch~=2.7.1",
            "--index-url", "https://download.pytorch.org/whl/cu128",
            venv_path="sd_scripts/venv",
        )
        expected_venv = str(Path("sd_scripts/venv"))
        mock_check_call.assert_called_once_with(
            [
                "/usr/bin/uv", "pip", "install", "--python",
                expected_venv,
                "-U", "torch~=2.7.1",
                "--index-url", "https://download.pytorch.org/whl/cu128",
            ]
        )

    @mock.patch("install_uv.subprocess.check_call")
    def test_force_reinstall_no_deps(self, mock_check_call):
        install_uv.uv_pip_install(
            "/usr/bin/uv", "-U", "--force-reinstall", "--no-deps",
            "git+https://github.com/example/repo",
        )
        cmd = mock_check_call.call_args[0][0]
        assert "--force-reinstall" in cmd
        assert "--no-deps" in cmd
        assert "git+https://github.com/example/repo" in cmd

    @mock.patch("install_uv.subprocess.check_call")
    def test_editable_install(self, mock_check_call):
        install_uv.uv_pip_install("/usr/bin/uv", "-U", "-e", "../custom_scheduler/.")
        cmd = mock_check_call.call_args[0][0]
        assert "-e" in cmd
        assert "../custom_scheduler/." in cmd


# ---------------------------------------------------------------------------
# Unit Tests – PLATFORM constant
# ---------------------------------------------------------------------------

class TestPlatformConstant:
    """Verify PLATFORM is set correctly in install_uv module."""

    def test_platform_is_set(self):
        assert install_uv.PLATFORM in ("windows", "linux", "")


# ---------------------------------------------------------------------------
# Unit Tests – standalone backend import
# ---------------------------------------------------------------------------

class TestBackendStandaloneImport:
    """Verify backend/install_uv.py can be imported independently (no parent repo needed)."""

    def test_backend_install_uv_importable(self):
        """Import backend/install_uv.py directly (simulating standalone backend clone)."""
        import importlib.util
        backend_dir = Path(__file__).resolve().parent.parent / "backend"
        spec = importlib.util.spec_from_file_location(
            "backend_install_uv", str(backend_dir / "install_uv.py")
        )
        backend_uv = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(backend_uv)

        # Verify all expected functions exist
        assert hasattr(backend_uv, "ensure_uv")
        assert hasattr(backend_uv, "create_venv")
        assert hasattr(backend_uv, "uv_pip_install")
        assert hasattr(backend_uv, "get_venv_python")
        assert hasattr(backend_uv, "get_venv_pip")
        assert hasattr(backend_uv, "PLATFORM")

    def test_backend_installer_importable_from_backend_dir(self):
        """Verify backend/installer.py can import from local install_uv.py."""
        import importlib.util
        backend_dir = Path(__file__).resolve().parent.parent / "backend"
        # Temporarily add backend to sys.path to simulate standalone execution
        backend_str = str(backend_dir)
        original_path = sys.path.copy()
        try:
            sys.path.insert(0, backend_str)
            spec = importlib.util.spec_from_file_location(
                "backend_installer", str(backend_dir / "installer.py")
            )
            backend_installer = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(backend_installer)

            # Verify key functions exist
            assert hasattr(backend_installer, "setup_venv")
            assert hasattr(backend_installer, "setup_config")
            assert hasattr(backend_installer, "check_git_install")
        finally:
            sys.path[:] = original_path


# ---------------------------------------------------------------------------
# Functional Tests – real uv operations (require uv + network)
# ---------------------------------------------------------------------------

def _find_uv():
    """Locate uv binary, returning None if not found."""
    uv = shutil.which("uv")
    if uv:
        return uv
    candidate = Path.home() / ".local" / "bin" / "uv"
    return str(candidate) if candidate.exists() else None


@pytest.mark.skipif(_find_uv() is None, reason="uv not available for functional tests")
class TestFunctionalCreateVenv:
    """Functional tests that create real venvs with uv.

    These tests require uv to be installed and available.
    """

    def test_create_venv_with_seed(self, tmp_path):
        """Create a venv and verify pip is available inside it."""
        venv_dir = str(tmp_path / "test_venv")
        uv = _find_uv()

        install_uv.create_venv(uv, venv_dir, "3.11")

        python = install_uv.get_venv_python(venv_dir)
        pip = install_uv.get_venv_pip(venv_dir)

        assert python.exists(), f"Python not found at {python}"
        assert pip.exists(), f"pip not found at {pip}"

        # Verify pip is callable
        result = subprocess.run(
            [str(python), "-m", "pip", "--version"],
            capture_output=True, text=True,
        )
        assert result.returncode == 0, f"pip --version failed: {result.stderr}"

    def test_uv_pip_install_basic(self, tmp_path):
        """Install a simple package via uv pip install."""
        venv_dir = str(tmp_path / "test_venv")
        uv = _find_uv()

        install_uv.create_venv(uv, venv_dir, "3.11")
        # Install a tiny package to verify pip install works
        install_uv.uv_pip_install(uv, "toml", venv_path=venv_dir)

        python = install_uv.get_venv_python(venv_dir)
        result = subprocess.run(
            [str(python), "-c", "import toml; print(toml.__version__)"],
            capture_output=True, text=True,
        )
        assert result.returncode == 0, f"toml import failed: {result.stderr}"

    def test_uv_pip_install_requirements(self, tmp_path):
        """Install from a requirements file via uv pip install."""
        venv_dir = str(tmp_path / "test_venv")
        uv = _find_uv()

        install_uv.create_venv(uv, venv_dir, "3.11")

        req_file = tmp_path / "requirements.txt"
        req_file.write_text("toml~=0.10.2\nrequests~=2.32.5\n")

        install_uv.uv_pip_install(uv, "-r", str(req_file), venv_path=venv_dir)

        python = install_uv.get_venv_python(venv_dir)
        result = subprocess.run(
            [str(python), "-c", "import toml; import requests; print('OK')"],
            capture_output=True, text=True,
        )
        assert result.returncode == 0, f"Import failed: {result.stderr}"
        assert "OK" in result.stdout
