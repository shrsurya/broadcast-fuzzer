broadcast-fuzzer
==================

Overview
----------- 
A cli(command-line-interface) tool to fuzz android broadcasts

Installation:
Option 1: \
`pip3 install git+ssh://git@github.com/shrsurya/broadcast-fuzzer.git`

Option 2:
1. `git clone https://github.com/shrsurya/broadcast-fuzzer.git`
2. `cd broadcast-fuzzer`
4. `pip3 install .`

Requirements:
1. [Android Platform Tools](https://developer.android.com/studio/releases/platform-tools)
2. Add adb path as an environment variable 'ADB_PATH', or provide adb path with each run. 
example. `buzz --adb 'path to adb executable'`
3. `SEED/` folder with seed files [example](https://github.com/shrsurya/broadcast-fuzzer/tree/main/SEED)

Usage:
1. `buzz --help` - Learn more about each option
2. `buzz -m 'path to AndroidManifest.xml'` - parse manifest file
3. `buzz -m 'path to AndroidManifest.xml' -p` - parse manifest file and print
4. `buzz -m 'path to AndroidManifest.xml' -g -dr 100` - generate 100 fuzzed data files for each intent in the AndroidManifest
5. `buzz -m 'path to AndroidManifest.xml' -g -dr 100 -sp 'path to SEED folder' -dp 'path to data generation folder'`
