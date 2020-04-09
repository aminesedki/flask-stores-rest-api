from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))

    items = db.relationship('ItemModel', lazy = 'dynamic')

    def __init__(self, name):
        self.name = name

    def json_format(self):
        return {'name': self.name, 'items': [item.json_format() for item in self.items.all()]}

    def save_to_db(self): # INSERT AND UPDTAE
        db.session.add(self)
        db.session.commit()


    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_item_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
