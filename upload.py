import os
import shutil
import subprocess


def upload_files(activate_venv=True, venv_name="venv"):
    """
    Build and upload the package to PyPI using Twine.
    """
    python_cmd = os.path.join(venv_name, "Scripts", "python") if activate_venv else "python"

    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)

    # Build package
    print("🔨 Building the package...")
    subprocess.run([python_cmd, "-m", "build"], check=True)

    # Upload package
    print("🚀 Uploading to PyPI...")
    twine_cmd = [
        python_cmd,
        "-m",
        "twine",
        "upload",
        "dist/*",
        "-u",
        "__token__",
        "-p",
        __read_token(),
        "--verbose"
    ]
    subprocess.run(twine_cmd, check=True)

    # Cleanup
    print("🧹 Cleaning up dist and egg-info directories...")
    shutil.rmtree(os.path.join(base_dir, "dist"))
    for sub_dir in os.listdir(base_dir):
        if sub_dir.endswith(".egg-info"):
            shutil.rmtree(os.path.join(base_dir, sub_dir))

    print("✅ Upload complete!")


def __read_token():
    """
    Read the PyPI token from a local file.
    """
    with open("pipy_token", "r") as f:
        return f.readline().strip()


if __name__ == "__main__":
    upload_files(activate_venv=True)
