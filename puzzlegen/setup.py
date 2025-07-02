from setuptools import setup

setup(
    name="puzzlegen",
    version="0.1.0",
    author="Caroline DAKOURE",
    author_email="caroline.dakoure@umontreal.ca",
    url="https://github.com/carodak/puzzlegen",
    install_requires=[
        "matplotlib"
    ],
    description="Procedural Match-3 Puzzle Generator and Solver",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)