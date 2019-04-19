"""A setuptools setup module."""

from os import path
from setuptools import setup, find_packages


def get_dist_dir():
    """Get the current directory."""
    return path.abspath(path.dirname(__file__))


def get_long_description():
    """Read long description from README.md file."""
    filepath = path.join(get_dist_dir(), "README.md")
    with open(filepath, encoding="utf-8") as readme_file:
        return readme_file.read()


def get_package_version():
    """Read package version number from the file."""
    filepath = path.join(get_dist_dir(), "version.txt")
    with open(filepath, encoding="utf-8") as version_file:
        return version_file.read().strip()


def get_requirements():
    """Read requirements from the file."""
    filepath = path.join(get_dist_dir(), "requirements.txt")
    with open(filepath, encoding="utf-8") as requirements:
        return list(map(lambda s: s.strip(), requirements.readlines()))


setup(
    name="wallpaperdownloader",
    version=get_package_version(),
    description="Wallpaper downloader code challenge (by Ostrovok)",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Konstantin Vinogradov",
    author_email="mail@k-vinogradov.ru",
    packages=find_packages(exclude=["tests"]),
    entry_points={
        "console_scripts": ["wallpaperdownloader=wallpaperdownloader:main"]
    },
    install_requires=get_requirements(),
)
