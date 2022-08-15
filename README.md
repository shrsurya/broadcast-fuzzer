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

### Requirements:
1. Get [Android Platform Tools](https://developer.android.com/studio/releases/platform-tools) 
2. Add path the to adb command line tool as an environment variable <br />
`export ADB_PATH='path/to/adb'` <br>
**OR** <br>
While using buzz, provide adb path with each run. 
example. <br>
`buzz --adb 'path to adb executable'`
3. Create a `SEED` folder with seed data [example](https://git.uwaterloo.ca/stqam-1225/class/project-s4suryan-s28hao-sstharap/-/tree/master/SEED)

4. You can use an android emulator or a physical device but make sure that only one is connected/active at a time

5. If using a physical device, enable [USB debugging](https://developer.android.com/studio/debug/dev-options#enable). 

6. Ensure that the target application is installed on the device.

7. Ensure that the target application has permission to access files and folders on the phone.

### Obtaining the manifest file:

Source Code Available:
- If the source code of the target application is available then the manifest can be obtained from the app source code.

Source Code Unavailable:

- If the source code is unavailable the manifest can be obtained by decompiling the target APK using [Apktool](https://ibotpeaches.github.io/Apktool/).

    The following steps explain how use Apktool and adb to extract the manifest file from the target APK.

    1. Pull the APK from the android device - [Instructions](https://stackoverflow.com/questions/4032960/how-do-i-get-an-apk-file-from-an-android-device) 

    2. Use Apktool on the APK to decompile it as follows. <br>
    `$ apktool d test.apk -o decompiledApp`

    3. `AndroidManifest.xml` can now be obtained from the `decompiledApp` directory


### Using Buzz:
1. `buzz --help` - Learn more about each option
2. `buzz -m 'path to AndroidManifest.xml'` - parse manifest file
3. `buzz -m 'path to AndroidManifest.xml' -p` - parse manifest file and print
4. `buzz -m 'path to AndroidManifest.xml' -g -dr 100` - generate 100 fuzzed data files for each intent in the AndroidManifest
5. `buzz -m 'path to AndroidManifest.xml' -g -dr 3 -e -sp 'path to SEED folder' -dp 'path to data generation folder' -adb 'path to adb executable'` generate 3 fuzzed data files for each intent. -adb, -sp and -dp are used to specify the paths

### Error Filtering:

Error keyword filter in buzz can be modified to listen to only specific errors. This can be done by changing the `ERROR_PHRASES` list in `SOURCES/broadcast_fuzzer/constants.py`. Currently the error listener runs a simple string search for these given keywords and the package name.

### Demo:

We have tested a few apps using our tool. The video recording of these tests are available on this repository.

