from setuptools import setup, find_packages

with open("README.md") as f:
    readme = f.read()

version = {}
with open("thingstodo/version.py") as f:
    exec(f.read(), version)

with open("requirements.txt") as f:
    install_requires = f.readlines()

setup(
    name="thingstodo",
    version=version["__version__"],
    description="Service for managing TODOs.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/e-k-m/thingstodo",
    author="Eric Matti",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="thingstodo",
    packages=find_packages(include=["thingstodo", "thingstodo.*"]),
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=install_requires,
    entry_points={"console_scripts": ["thingstodo-utils=thingstodo.cli:main"]},
)
