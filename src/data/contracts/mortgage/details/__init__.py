from . import base, extened
from typing import TypedDict

class Base(TypedDict):
    cashflows: base.CashFlows
    upfront: base.Upfront

class Extended(TypedDict):
    cashflows: extened.CashFlows
    upfront: extened.Upfront
