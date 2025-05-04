from setuptools import setup, find_packages

setup(
    name="matart",
    version="0.1.0",
    packages=find_packages(),    # will now pick up the matart/ folder
    install_requires=[
        "PySide6",
        "pycairo"
    ],
    entry_points={
        "console_scripts": [
            "matart=matart.app:main"
        ],
    },
)
