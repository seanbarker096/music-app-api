from api.events.event_consumer import EventConsumer


class EventProducer:
    def addObserver(self, observer: EventConsumer):
        pass

    def publishEvent(self, event: any):
        pass
