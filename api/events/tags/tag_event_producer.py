from api.events.event_consumer import EventConsumer
from api.events.event_producer import EventProducer
from api.events.tags.event_objects.tag_event import TagEvent
from api.events.tags.posts_tag_event_consumer import PostsTagEventConsumer


class TagEventProducer(EventProducer):
    observers = [
        PostsTagEventConsumer,
        PostsTagEventConsumer,
    ]

    def __init__(self):
        self.initialize_observers()

    def initialize_observers(self):
        self.observers = [observer({}) for observer in self.observers]

    def addObserver(self, observer: EventConsumer):
        ...

    def publishEvent(self, event: TagEvent):
        for observer in self.observers:
            observer.consume(event)
