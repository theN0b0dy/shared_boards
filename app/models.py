from pymodm import MongoModel, fields
from pymodm.manager import Manager

from query_set import UserQuerySet

userQuerySetManager = Manager.from_queryset(UserQuerySet)

class User(MongoModel):
    id = fields.CharField(primary_key=True)
    name = fields.CharField()
    email = fields.EmailField()
    password = fields.CharField()
    
    objects = userQuerySetManager()

    class Meta:
        connection_alias = "flask_app"
    

class Board(MongoModel):
    id = fields.CharField(primary_key=True)
    title = fields.CharField()
    description = fields.CharField()
    user = fields.ReferenceField(User)

    class Meta:
        connection_alias = "flask_app"

