from setuptools import setup, find_packages

setup(
    name='broadcast-fuzzer',
    version='1.0.0.1',
    python_requires='>3.6',
    description='Tool to fuzz android broadcast receivers',
    author='s4suryan',
    author_email="s4suryan@uwaterloo.ca",
    packages=find_packages('SOURCES'),
    package_dir={'':'SOURCES'},
    include_package_data=True,
    install_requires=[
        'click',
        'requests',
        'six',
        'pyyaml'
    ],
    entry_points={
        'console_scripts':['broadcast-fuzzer=broadcast-fuzzer:cli']
    }
)
