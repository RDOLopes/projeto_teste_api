from sqlalchemy import Column, Integer


class ModelBase (object):
    id = Column(Integer, primary_key=True, index=True)