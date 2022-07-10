
class intent_filter(object):
    def __init__(self, parent_type, parent_name, action_name, data_mimetype) -> None:
        # Parent can be a: Activity, Service or a Receiver
        self.parent_type = parent_type
        self.parent_name = parent_name
        self.action_name = action_name
        self.data_mimetype = data_mimetype

    def __repr__(self) -> str:
        return self.parent_type +": "+ self.parent_name + "\naction_name: "+ self.action_name+ "\ndata_mimetype: "+ self.data_mimetype