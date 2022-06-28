import logging
logger = logging.getLogger(__name__)


class BrodcastFuzzer(object):
    """
    A class to handle the various functionalities of
    brodcast fuzzer
    """
    def __init__(self, **kwargs) -> None:
        """Configure self and execute"""
        pass

    def extract_apk(self, apk_path, extract_folder):
        """
        Use apktool to extract apk file
        apk_path: absolute path the apk file
        extract_folder:
        apktool d -s yourapk.apk -o yourfolder 

        Assumes: user has apktool installed
        """
        pass

    def extract_xml(self):
        """
        <manifest>
            package
            <application>
                list of [<service> // or <activity> or <receiver>
                    android:name
                    <intent-filter>
                        <action>
                            android:name
                        </action>
                        <data>
                            android:mimeType
                        </data>
                    <intent-filter>
                </service> // or </activity> or </receiver> ]
            </application>
        </maifest>
        """
        pass