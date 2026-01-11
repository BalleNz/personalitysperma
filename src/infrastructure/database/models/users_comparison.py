from sqlalchemy import Column, Text, Float, Integer, ForeignKey

from infrastructure.database.models.base import IDMixin, TimestampsMixin


class UsersComparison(IDMixin, TimestampsMixin):
    """
    Таблица для хранения сравнения совместимости пользователей по разным характеристикам.
    Каждая запись описывает совместимость по одной характеристике между двумя пользователями.
    """

    __tablename__ = 'users_comparison'

    # Основной первичный ключ
    id = Column(Integer, primary_key=True, autoincrement=True, comment='Уникальный идентификатор сравнения')

    # Ссылки на сравниваемых пользователей
    user_a_id = Column(
        Integer,
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
        comment='ID первого пользователя'
    )

    user_b_id = Column(
        Integer,
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
        comment='ID второго пользователя'
    )

    # Характеристики совместимости
    holland_code = Column(
        Text,
        nullable=True,
        comment='Совместимость по кодам Голланда'
    )

    hecaxo = Column(
        Text,
        nullable=True,
        comment='Совместимость по HECAxo'
    )

    socionics = Column(
        Text,
        nullable=True,
        comment='Совместимость по соционике'
    )

    basic_traits = Column(
        Text,
        nullable=True,
        comment='Совместимость по базовым чертам'
    )

    clinic_traits = Column(
        Text,
        nullable=True,
        comment='Совместимость по клиническим чертам'
    )

    summary = Column(
        Text,
        nullable=True,
        comment='сводка совместимости'
    )

    # Метаданные и оценки
    compatibility_score = Column(
        Float,
        nullable=True,
        comment='Общая оценка совместимости (0-100)'
    )
