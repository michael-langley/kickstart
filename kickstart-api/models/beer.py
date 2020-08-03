import json


class Beer:
    id: str
    name: str
    style: str
    quantity: int
    description: str

    def __init__(self, id: str, name: str, style: str, quantity: int, description: str = None):
        self.id = id
        self.name = name
        self.style = style
        self.quantity = quantity
        self.description = description

    @property
    def to_publishable(self):
        return json.dumps({
            'id': self.id,
            'name': self.name,
            'style': self.style,
            'quantity': self.quantity,
            'description': self.description
        })
