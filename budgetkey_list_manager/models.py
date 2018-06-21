import logging
import json

from contextlib import contextmanager

from sqlalchemy import DateTime
from sqlalchemy import inspect
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Unicode, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker

# ## SQL DB
Base = declarative_base()

_sql_engine = None
_sql_session = None


def setup_engine(connection_string):
    global _sql_engine
    assert connection_string, "No database defined, please set your DATABASE_URL environment variable"
    _sql_engine = create_engine(connection_string)
    Base.metadata.create_all(_sql_engine)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    global _sql_session
    if _sql_session is None:
        assert _sql_engine is not None, "No database defined, please set your DATABASE_URL environment variable"
        _sql_session = sessionmaker(bind=_sql_engine)
    session = _sql_session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.expunge_all()


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


def parse_properties(item):
    item['properties'] = json.loads(item['properties'])
    return item


class List(Base):
    __tablename__ = 'lists'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    user_id = Column(String(128))


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    list_id = Column(Integer)
    url = Column(String(512))
    title = Column(Unicode)
    properties = Column(Unicode)


def get_list(list_name, user_id):
    with session_scope() as session:
        ret = session.query(List).filter_by(name=list_name, user_id=user_id).first()
        return object_as_dict(ret) if ret else None


def get_list_by_item(item_id):
    with session_scope() as session:
        item = session.query(Item).get(item_id)
        ret = None
        if item:
            ret = session.query(List).get(item.list_id)
        return object_as_dict(ret) if ret else None


def create_list(list_name, user_id):
    with session_scope() as session:
        to_add = List(name=list_name, user_id=user_id)
        session.add(to_add)
        session.flush()
        return object_as_dict(to_add)


def add_item(list_name, user_id, item):
    with session_scope() as session:
        list_id = session.query(List).filter_by(name=list_name, user_id=user_id).first().id
        existing_item = session.query(Item)\
                               .filter_by(list_id=list_id,
                                          title=item["title"],
                                          url=item["url"])\
                               .first()
        if existing_item is None:
            to_add = Item(list_id=list_id, **item)
            session.add(to_add)
            ret = to_add
        else:
            existing_item.properties = item.get('properties')
            session.add(existing_item)
            ret = existing_item
        session.flush()
        return object_as_dict(ret)


def get_items(list_name, user_id):
    with session_scope() as session:
        list_id = session.query(List).filter_by(name=list_name, user_id=user_id).first().id
        return list(map(parse_properties,
                        map(object_as_dict, 
                            session.query(Item).filter_by(list_id=list_id))))


def delete_item(item_id):
    with session_scope() as session:
        session.delete(session.query(Item).get(item_id))
