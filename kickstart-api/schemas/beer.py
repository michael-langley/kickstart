from marshmallow import Schema, fields, post_load
from models.beer import Beer
from uuid import uuid1


class CreateBeerSchema(Schema):
    name = fields.Str(required=True)
    style = fields.Str(required=True)
    quantity = fields.Int(required=True)

    @post_load
    def make_beer(self, data, **kwargs):
        beer_args = {'id': str(uuid1()), **data}
        return Beer(**beer_args)


class UpdateBeerSchema(Schema):
    id = fields.Str(required=True)
    name = fields.Str(required=True)
    style = fields.Str(required=True)
    quantity = fields.Int(required=True)
    description = fields.Str()

    @post_load
    def make_beer(self, data, **kwargs):
        return Beer(**data)


class BeerResponseSchema(Schema):
    id = fields.Str(required=True)
    name = fields.Str(required=True)
    style = fields.Str(required=True)
    quantity = fields.Int(required=True)
    description = fields.Str()
