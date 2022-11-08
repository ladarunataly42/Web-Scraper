from mongoengine import ValidationError, EmailField, DynamicDocument, StringField


class Users(DynamicDocument):
    email = EmailField(required=True, unique=True),
    password = StringField(required=True)
