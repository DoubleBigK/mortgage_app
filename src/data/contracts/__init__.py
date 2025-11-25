from . import mortgage
from typing import TypedDict

class Mortgage(TypedDict):
    settings: mortgage.Settings
    details: mortgage.Details
    summaries: mortgage.Summaries