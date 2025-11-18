from . import settings

def standard(mortgage_name: str):
    settings.Basic(mortgage_name).render()
    settings.Additional(mortgage_name).render()
