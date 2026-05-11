from pathlib import Path

from setuptools import find_packages, setup


def read_requirements() -> list[str]:
    """Read runtime requirements from requirements.txt."""
    content = Path("requirements.txt").read_text(encoding="utf-8")
    return [line.strip() for line in content.splitlines() if line.strip() and not line.startswith("#")]


setup(
    name="orca-gui",
    version="6.1.0",
    author="Ajay Khanna",
    description="GUI interface for generating ORCA quantum chemistry input files",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=read_requirements(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "orca-gui=orca_gui.app:main",
        ],
    },
)
