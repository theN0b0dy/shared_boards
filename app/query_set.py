from pymodm.queryset import QuerySet


class UserQuerySet(QuerySet):
    def get_by_id(self, id):
        return self.raw({'_id': id})
    
    def get_by_email(self, email):
        return self.raw({'email': email})