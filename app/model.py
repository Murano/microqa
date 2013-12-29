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
    
    
class User(Document):
    username = StringField(max_length=80, unique=True, required=True)
    email = StringField(max_length=120, unique=True, required=True)
    password = StringField(max_length=64, required=True)

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
        
    def __unicode__(self):
        return self.username