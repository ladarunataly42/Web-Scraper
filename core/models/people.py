from mongoengine import DynamicDocument, StringField, IntField, DateTimeField, ImageField


class People(DynamicDocument):
    name = StringField(required=True),
    birthday = DateTimeField(required=False),
    phone = StringField(required=False),
    address = StringField(required=False),
    profile_picture = ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)
    likes_picture = IntField(required=False),
    friends = IntField(required=False),
    education = StringField(required=False),
    city = StringField(required=False),
    hometown = StringField(required=False),
    relationship = StringField(required=False),
    work = StringField(required=False),
    hobbies = StringField(required=False),
    url_fb = StringField(required=True, unique=True),
    url_instagram = StringField(required=False),
    created_at = DateTimeField(required=False)

    # def __str__(self):
    #     return f'{self.people_id}-{self.first_name}-{self.last_name}-{self.link}'
