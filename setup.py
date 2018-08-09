import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MetaKnight",
    version="0.0.1",
    author="Yael Eisenberg, Laura Stordy, Matt Uffenheimer",
    author_email="laurastordy@gmail.com",
    description="A Python package for Kirby Calculus",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mattuff/KirbyCalculus",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3"
        ),
)
