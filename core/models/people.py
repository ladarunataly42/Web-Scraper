from mongoengine import DynamicDocument, StringField, IntField, DateTimeField


class People(DynamicDocument):
    name = StringField(required=True),
    about_life_events = StringField(required=False),
    about_details = StringField(required=False),
    about_family_and_relationships = StringField(required=False),
    friends = IntField(required=False),
    about_contact_and_basic_info = StringField(required=False),
    about_work_and_education = StringField(required=False),
    url_fb = StringField(required=True, unique=True),
    url_instagram = StringField(required=False),
    created_at = DateTimeField(required=False)

    # def __str__(self):
    #     return f'{self.people_id}-{self.first_name}-{self.last_name}-{self.link}'
