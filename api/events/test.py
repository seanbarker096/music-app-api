from api.events.tags.tag_event_subject import TagEventSubject

if __name__ == "__main__":
    producer = TagEventSubject()

    producer.publishEvent({})
