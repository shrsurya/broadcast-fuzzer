broadcast-fuzzer
==================

Overview
----------- 
A cli(command-line-interface) tool to fuzz android broadcasts

Installation:
Option 1: \
`pip install git+ssh://git@github.com/shri94/broadcast-fuzzer.git`

Option 2: \
1. `git clone https://github.com/shri94/broadcast-fuzzer.git`
2. `cd broadcast-fuzzer`
4. `pip3 install .`

Usage:
1. `bfuzz -m 'path to AndroidManifest.xml -p`(parse manifest file and print manifest data found)