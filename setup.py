from setuptools import setup, find_packages

# Read the contents of your README file
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="software-properties-station",
    version="0.0.1",  # Updated version
    author="Vic Thacker",  # Updated author
    author_email="vic.thacker@fastmail.fm",  # Updated author email
    description="A tool for software properties in GhostBSD",  # Updated description
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ghostbsd/software-properties-station",  # Updated URL
    package_dir={
        'software_properties_station': 'software_properties_station',  # Main package
        'config': 'config',  # Config package
        'repo': 'repo',  # Repo package
        'ui': 'ui',  # UI package
    },
    packages=['software_properties_station', 'config', 'repo', 'ui'],  # Include all packages
    include_package_data=True,  # Include additional files specified in MANIFEST.in
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Environment :: X11 Applications :: GTK",
    ],
    python_requires=">=3.6",  # Specify Python version compatibility
    install_requires=[
        "PyGObject>=3.36.0",  # GTK bindings for Python
    ],
    entry_points={
        'console_scripts': [
            'software-properties-station=software_properties_station.main:main',  # Main entry point for CLI/GUI
        ],
    },
    license="BSD-3-Clause",
)

