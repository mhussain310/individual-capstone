from setuptools import setup, find_packages

# Read the requirements from the requirements.txt file
with open("requirements.txt") as f:
    install_requires = f.read().splitlines()

setup(
    name="individual_capstone",
    version="0.1.0",
    description="My capstone project.",
    author="Mo",
    author_email="m-hussain21@outlook.com",
    url="",
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            "run_etl=scripts.run_etl:main",
            "run_tests=tests.run_tests:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
