from typing import Dict

from app.constants import STATIC_KIND, FIELD_KIND, ARG_KIND, VAR_KIND, NONE_KIND


class Symbol:
    def __init__(self, sym_name: str, sym_type: str, sym_kind: str, running_index: int):
        self.name = sym_name
        self.type = sym_type
        self.kind = sym_kind
        self.running_index = running_index

    def __str__(self) -> str:
        return f"s_name: {self.name}| type: {self.type}| kind: {self.kind}| index: {self.running_index}"


class SymbolTable:
    def __init__(self) -> None:
        self.class_table: Dict[str, Symbol] = {}  #: dict[str: Symbol]
        self.func_table: Dict[str, Symbol] = {}
        self.table: Dict[str, Symbol] = self.class_table
        self.counter = {
            STATIC_KIND: 0,
            FIELD_KIND: 0,
            ARG_KIND: 0,
            VAR_KIND: 0,
            NONE_KIND: 0,
        }

    def start_subroutine(self) -> None:
        self.table = self.func_table
        self.counter[VAR_KIND] = 0
        self.counter[ARG_KIND] = 0
        self.func_table.clear()

    def start_sub(self) -> None:
        self.table = self.func_table

    def define(self, name: str, type: str, kind: str) -> None:
        sym = Symbol(name, type, kind, self.counter[kind])
        self.counter[kind] += 1
        self.table[name] = sym

    def var_count(self, kind: str) -> int:
        return self.counter.get(kind, 0)

    def kind_of(self, name: str) -> str:
        symbol = self.table.get(name, None)
        if symbol:
            return symbol.kind
        return NONE_KIND

    def type_of(self, name: str) -> str:
        return self.table[name].type

    def index_of(self, name: str) -> int:
        return self.table[name].running_index

    def end_sub_routine(self) -> None:
        self.table = self.class_table

    def __str__(self) -> str:
        string = " func_table: \n"
        for val in self.func_table.values():
            string += str(val) + "\n"
        string += " class_table: \n"
        for val in self.class_table.values():
            string += str(val) + "\n"
        return string
