from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
                        'price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument(
                        'store_id',
                        type=int,
                        required=True,
                        help="Every item should have a store id !!!"
                        )
    @jwt_required()
    def get(self, name):

        item = ItemModel.find_item_by_name(name)
        if item is not None:
            return item.json_format(), 200
        else:
            return {'message': f"item named {name} not found"}, 404

    def post(self, name):
        if ItemModel.find_item_by_name(name):
            return {'message': f"item with name {name} already existe."}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": f"An error occurred inserting the item named {name}."}, 500

        return item.json_format(), 201

    def delete(self, name):

        item = ItemModel.find_item_by_name(name)

        if item:
            item.delete_from_db()

        return {'message': f"Item named {name} succssefully deleted."}

    def put(self, name):

        data = Item.parser.parse_args()
        item = ItemModel.find_item_by_name(name)
        if item is None:
                item = ItemModel(name, **data)
        else:
            item.price = data['price']

        try:
            item.save_to_db()
        except:
            return {"message": f"An error occurred while inserting or updating the item named {name}."}, 500

        return item.json_format()


class ItemsList(Resource):
    @jwt_required()
    def get(self):
        return {'items': [item.json_format() for item in ItemModel.query.all()]}
