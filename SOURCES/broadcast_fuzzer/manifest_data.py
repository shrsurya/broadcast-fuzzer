import xml.etree.ElementTree as ET

class mainfest_data(object):
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
    #TAGS = ['service', 'receiver', 'activity']
    def __init__(self, mainfest_xml) -> None:
        self.mainfest_xml = mainfest_xml
        self.manifest_package_name = ""
        self.intent_filters = []
        self.extract_xml()

    def extract_xml(self):
        print("Parsing file: ", self.mainfest_xml)
        tree = ET.parse(self.mainfest_xml)
        # root is <manifest>
        root = tree.getroot()
        self.manifest_package_name = root.attrib['package']
        application_tag = []
        for child in root.findall('application'):
            application_tag = child

        for child in application_tag:
            if child.tag == "activity" or child.tag == "service" or child.tag == "receiver":
                self.get_intent_filters(child)

    def get_intent_filters(self, sar):
        # sar: Service, activity, reciever
        sar_type = sar.tag
        sar_name = sar.attrib["{http://schemas.android.com/apk/res/android}name"]
        for sar_child in sar:
            if sar_child.tag == "intent-filter":
                # we only care about activities that have a data tag
                action_name = ""
                data_mimetype = ""
                for sar_child_child in sar_child:
                    if sar_child_child.tag == "action":
                        action_name = sar_child_child.attrib["{http://schemas.android.com/apk/res/android}name"]
                    elif sar_child_child.tag == "data":
                        try:
                            data_mimetype = sar_child_child.attrib["{http://schemas.android.com/apk/res/android}mimeType"]
                        except:
                            pass
                if data_mimetype != "":
                    intent = intent_filter(sar_type, sar_name, action_name, data_mimetype)
                    self.intent_filters.append(intent)

class intent_filter(object):
    def __init__(self, sar_type, sar_name, action_name, data_mimetype) -> None:
        # sar: Service, activity, reciever
        self.sar_type = sar_type
        self.sar_name = sar_name
        self.action_name = action_name
        self.data_mimetype = data_mimetype

    def __repr__(self) -> str:
        return self.sar_type +": "+ self.sar_name + "\naction_name: "+ self.action_name+ "\ndata_mimetype: "+ self.data_mimetype

# if __name__ == "__main__":
#     md = mainfest_data("")
#     print(len(md.intent_filters))
#     for intent in md.intent_filters:
#         print(intent)