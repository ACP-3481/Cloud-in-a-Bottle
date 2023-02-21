
class EventHandler:

    def __init__(self):
        self.Event_Register = {}
        self.EVENT_NAME = 0
        self.EVENT_DESCRIPTION = 1

    def add_event(self, event_id: int, event_name: str, event_description: str):
        if event_id not in self.Event_Register:
            self.Event_Register[event_id] = [event_name, event_description]
        else:
            print("Error: event_id already exists")

    def remove_event(self, event_id: int):
        if event_id in self.Event_Register:
            del self.Event_Register[event_id]
        else:
            print("Error: event_id does not exist")

    def describe_event(self, event_id: int):
        print(self.Event_Register[event_id])
        return self.Event_Register[event_id]
