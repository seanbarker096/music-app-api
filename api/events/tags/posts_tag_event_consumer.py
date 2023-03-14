import json

from api.events.tags.event_objects.tag_event import TagEvent
from api.events.tags.tag_event_consumer import TagEventConsumer


class PostsTagEventConsumer(TagEventConsumer):
    def __init__(self, event):
        self.event = event
        print("init")

    def consume(self, event: TagEvent):
        print(f"Consuming event: {json.dumps((event))}")
