from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

setup(
    name='broadcast-fuzzer',
    version='1.0.0.1',
    python_requires='>3.7',
    description='Tool to fuzz android broadcast receivers',
    author='s4suryan',
    author_email="s4suryan@uwaterloo.ca",
    license = 'MIT',
    long_description = long_description,
    packages=find_packages('SOURCES'),
    package_dir={'':'SOURCES'},
    include_package_data=True,
    install_requires = [requirements],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts':['bfuzz=broadcast_fuzzer:cli']
    }
)
