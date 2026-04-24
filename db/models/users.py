from flask_login import UserMixin
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash

from db.session_factory import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)

    fragments = relationship("Fragment", back_populates="user")

    def set_hashed_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_hashed_password(self, password):
        return check_password_hash(self.hashed_password, password)
