from datetime import datetime

from mongoengine import *

from config import MONGO_DB_NAME

connect(MONGO_DB_NAME)

class Comment(EmbeddedDocument):
    username = StringField(required=True)
    body = StringField(required=True)

class Question(Document):
    username = StringField(required=True)
    title = StringField(required=True)
    body = StringField(required=True)
    tags = ListField()
    timestamp = DateTimeField(default=datetime.now())
    comments = ListField(EmbeddedDocumentField(Comment))

    meta = {
        'indexes': [
            {'fields': ['-tags'], 'sparse': True, 'types': False}
        ]
    }


class Tag(Document):
    tags = ListField(StringField())