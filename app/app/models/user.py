

# This could be a SQLAlchemy model,
# an ElasticSearch document, a MongoDB document, etc
class User:
    def __init__(self, first_name, surname):
        self.first_name = first_name
        self.surname = surname
