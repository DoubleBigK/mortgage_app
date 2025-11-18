from . import settings, details
from typing import TypedDict

class Settings(TypedDict):
    basic: settings.Basic
    additional: settings.Additional

class Details(TypedDict):
    general: details.General
    monthly: details.Monthly
    upfront: details.Upfront