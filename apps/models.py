# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps import db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, relationship
from apps.exceptions.exception import InvalidUsage

class Product(db.Model):

    __tablename__ = 'products'

    id            = db.Column(db.Integer,      primary_key=True)
    name          = db.Column(db.String(128),  nullable=False)
    info          = db.Column(db.Text,         nullable=True)
    price         = db.Column(db.Integer,      nullable=False)
    
    def __init__(self, **kwargs):
        super(Product, self).__init__(**kwargs)

    def __repr__(self):
        return f"{self.name} / ${self.price}"

    @classmethod
    def find_by_id(cls, _id: int) -> "Product":
        return cls.query.filter_by(id=_id).first() 

    @classmethod
    def get_list(cls):
        return cls.query.all()

    def save(self) -> None:
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)

    def delete(self) -> None:
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)
        return
    
class Group(db.Model):
    """
    Group model for managing user groups
    """
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String, unique=True, nullable=False)
    # 定义与 User 表的关系：一个 Group 可以有多个 User
    # backref='group' 会在 User 模型中自动创建一个 'group' 属性，指向所属的 Group 对象
    users = relationship("DevUser", backref="group", lazy="joined")

    def __repr__(self):
        return f"<Group(id={self.id}, name='{self.name}')>"

class DevUser(db.Model):
    """
    定义 DevUser 表，包含用户基本信息和所属组，以及 IP 地址。
    """
    __tablename__ = 'devusers'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    ip_address = db.Column(db.String(45), nullable=False)
    devidce_id = db.Column(db.Integer, unique=True, nullable=False)

    # 定义外键，关联到 groups 表的 id 字段
    # ondelete="SET NULL" 表示当关联的 Group 被删除时，该组下的 User 的 group_id 将被设置为 NULL
    # nullable=True 必须设置为 True，因为 group_id 现在可以为 NULL
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id', ondelete="SET NULL"), nullable=True)

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', ip_address='{self.ip_address}', group_id={self.group_id})>"
