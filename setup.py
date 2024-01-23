from setuptools import find_packages, setup

with open("README.md") as f:
    long_description = f.read()

setup(
    name="pydatalib2",
    version="0.0.3",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        # Add any dependencies here
    ],
    author='Suresh Chandra Sekar',  # noqa
    maintainer='Nithesh',  # noqa
    description="pydatalib2 is a utilities igniting innovation and efficiency in development.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sureshchandras3kar/pydatalib2",
    license="Apache License 2.0",
    python_requires=">=3.6",
    tests_require=[
        "pytest"
    ],
    keywords=[
        "python",
        "utilities",
        "development",
        "efficiency",
        "data processing",
        "text manipulation",
        "file management",
        "data structures"
    ],
    classifiers=[
        "Development Status ::  1 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache License 2.0",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
)
