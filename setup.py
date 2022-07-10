from setuptools import setup, find_packages

setup(
    name='brodcast-fuzzer',
    version='1.0.0.1',
    python_requires='>3.6',
    description='Tool to fuzz android broadcast receivers',
    author='s4suryan',
    #author_email="",
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
        'console_scripts':['brodcast-fuzzery=brodcast-fuzzer:cli']
    }
)
