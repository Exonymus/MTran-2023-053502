from core.language import *
from dataclasses import dataclass


@dataclass()
class LiteralTableItem:
    itemId: int
    itemType: LiteralTypes
    itemValue: str


@dataclass()
class VariableTableItem:
    itemBlockId: int
    itemBlockLevel: int
    itemName: str
    itemType: VariableTypes


class LiteralTable:
    def __init__(self):
        self.Literals = []
        self.LiteralToTableItem = {}

    def push(self, value, type) -> int:
        if value in self.LiteralToTableItem:
            return self.LiteralToTableItem.get(value).itemId

        id = len(self.Literals)
        table_item = LiteralTableItem(id, type, value)

        self.Literals.append(table_item)
        self.LiteralToTableItem[value] = table_item

        return id

    def get(self, id) -> LiteralTableItem:
        return self.Literals[id]
