from ...db import models
from ...db.crud import ResourceBase


class Stock(ResourceBase):
    orm_meta = models.Stock
    _primary_keys = ('id',)
