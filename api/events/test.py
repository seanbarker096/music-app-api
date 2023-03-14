from api.events.tags.tag_event_producer import TagEventProducer

if __name__ == "__main__":
    producer = TagEventProducer()

    producer.publishEvent({})
