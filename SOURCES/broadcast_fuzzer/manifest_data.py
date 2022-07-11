import xml.etree.ElementTree as ET

class mainfest_data(object):
    """
    A structure used to represent useful data from the android manifest
    """
    # Global strings
    ANDROID_STR = "{http://schemas.android.com/apk/res/android}"
    ANDROID_STR_NAME = ANDROID_STR+"name"
    ANDROID_STR_MIMETYPE = ANDROID_STR+"mimeType"

    def __init__(self, mainfest_xml) -> None:
        self.mainfest_xml = mainfest_xml
        self.manifest_package_name = ""
        self.intent_filters = []
        self.extract_xml()

    def extract_xml(self):
        """
        Extracts required data fromthe AndroidManifest.xml file
        """
        tree = ET.parse(self.mainfest_xml)
        # root is <manifest> tag of the xml file
        root = tree.getroot()
        # Store the package name
        self.manifest_package_name = root.attrib['package']
        # contents of application tag extracted and stored
        application_tag = []
        for child in root.findall('application'):
            application_tag = child
        for child in application_tag:
            if child.tag == "activity" or child.tag == "service" or child.tag == "receiver":
                self.get_intent_filters(child)

    def get_intent_filters(self, sar):
        # sar: Service, activity, reciever
        # Get what type of sar being parsed
        sar_type = sar.tag
        # Get the current sar tags's name
        sar_name = sar.attrib[self.ANDROID_STR_NAME]
        # Get all useful intent filters within the current sar tag
        for sar_child in sar:
            if sar_child.tag == "intent-filter":
                # we only care about activities that have a data tag
                action_name = ""
                data_mimetype = ""
                for sar_child_child in sar_child:
                    # Action name is required for each intent filter
                    if sar_child_child.tag == "action":
                        action_name = sar_child_child.attrib[self.ANDROID_STR_NAME]
                    elif sar_child_child.tag == "data":
                        # if the data tag as mime type, it will get it
                        try:
                            data_mimetype = sar_child_child.attrib[self.ANDROID_STR_MIMETYPE]
                        # otherwise it will stay empty
                        except:
                            pass
                # if the intent doesn't have a mimeType, we dont care about it
                # Otherwise, we create a new intent filter and add it to the manifest_data object
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
#     md = mainfest_data("../../xmls/telegram_manifest.xml")
#     print(len(md.intent_filters))
#     for i in md.intent_filters:
#         print(i)