from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_item_by_name(name)
        if store is not None:
            return store.json_format()

        return {"message": f"Store named {name} not found"},404

    def post(self, name):

        if StoreModel.find_item_by_name(name) is not None:
            return {"message": f"Store with name {name} already existe"}, 400

        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {"message": f"An error occurred inserting the store named {name}."}, 500
        return store.json_format(), 201


    def delete(self, name):
        store = StoreModel.find_item_by_name(name)
        if store:
            store.delete_from_db()

        return {"message": f"Store named {name} succssefully deleted"}, 200


class StoreList(Resource):
    def get(self):
        return {"Stores": [store.json_format() for store in StoreModel.query.all()]}
