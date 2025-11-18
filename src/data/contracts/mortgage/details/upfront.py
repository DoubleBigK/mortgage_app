from typing import TypedDict

class Base(TypedDict):
    commission: int
    apprisal: int
    annex: int
    TOTAL: int

class Additional(TypedDict):
    insurance: int
    other: int
    TOTAL: int