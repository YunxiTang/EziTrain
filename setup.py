from setuptools import setup, find_packages

setup(
    name="ezitrain",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy",
    ],
    author="yunxi tang",
    author_email="tangyunxi000@gmail.com",
    description="A Python package for easy model training",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/YunxiTang/EziTrain",
)