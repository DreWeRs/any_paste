from datetime import datetime

from sqlalchemy import Integer, Column, String, DateTime, ForeignKey, TEXT, Uuid
from sqlalchemy.orm import relationship

from db.session_factory import SqlAlchemyBase


class Fragment(SqlAlchemyBase):
    """ Фрагменты - текст которым пользователь делится с помощью сайта """
    __tablename__ = 'fragments'

    id = Column(String(32), primary_key=True)  # UUID - сгенерированная HEX строка обеспечивающая неповторимость ID
    # и при этом решает проблему когда пользователи могут перебирать ID чтобы найти фрагменты других пользователей
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    filename = Column(String, nullable=False)  # Имя для отображения в списке фрагментов на сайте
    content = Column(TEXT, nullable=False)  # содержимое файла
    created_at = Column(DateTime, default=datetime.now())

    user = relationship("User", back_populates="fragments")
