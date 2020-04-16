"""
Run 'pip install .' from the current directory to install relevant packages.
"""
from setuptools import setup

setup(
    name="dry_rock",
    version="1.0",
    description="Retrieves weather data and makes a html report.",
    author="Rory Sullivan",
    author_email="codingrory@gmail.com",
    url="https://github.com/Rory-Sullivan/Dry-Rock",
    packages=["dry_rock"],  # same as name
    install_requires=["beautifulsoup4", "requests", "lxml", "jinja2"],
    extras_require={
        "dev": ["eslint", "pycodestyle", "black"],
        "test": ["coverage"],
    },
    python_requires=">=3.6",
)
