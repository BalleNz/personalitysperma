from typing import List, Optional
from uuid import uuid4, UUID

from pydantic import BaseModel, Field, field_validator, computed_field

from src.core.enums.socionics import (
    RelationshipType
)


class UserSocionicsSchema(BaseModel):
    """Схема соционического профиля пользователя"""
    id: Optional[UUID] = Field(default_factory=uuid4)
    GROUP: str = "personality"

    ENTP: Optional[float] = Field(None, ge=0.0, le=1.0, description="ENTP / ILE (Дон Кихот)")
    ISFJ: Optional[float] = Field(None, ge=0.0, le=1.0, description="ISFJ / SEI (Дюма)")
    ESFJ: Optional[float] = Field(None, ge=0.0, le=1.0, description="ESFJ / ESE (Гюго)")
    INTP: Optional[float] = Field(None, ge=0.0, le=1.0, description="INTP / LII (Робеспьер)")

    ENFJ: Optional[float] = Field(None, ge=0.0, le=1.0, description="ENFJ / EIE (Гамлет)")
    ISTP: Optional[float] = Field(None, ge=0.0, le=1.0, description="ISTP / LSI (Максим Горький)")
    ESTP: Optional[float] = Field(None, ge=0.0, le=1.0, description="ESTP / SLE (Жуков)")
    INFJ: Optional[float] = Field(None, ge=0.0, le=1.0, description="INFJ / IEI (Есенин)")

    ESFP: Optional[float] = Field(None, ge=0.0, le=1.0, description="ESFP / SEE (Наполеон)")
    INTJ: Optional[float] = Field(None, ge=0.0, le=1.0, description="INTJ / ILI (Бальзак)")
    ENTJ: Optional[float] = Field(None, ge=0.0, le=1.0, description="ENTJ / LIE (Джек Лондон)")
    ISFP: Optional[float] = Field(None, ge=0.0, le=1.0, description="ISFP / ESI (Драйзер)")

    ENFP: Optional[float] = Field(None, ge=0.0, le=1.0, description="ENFP / IEE (Гексли)")
    INFP: Optional[float] = Field(None, ge=0.0, le=1.0, description="INFP / EII (Достоевский)")
    ESTJ: Optional[float] = Field(None, ge=0.0, le=1.0, description="ESTJ / LSE (Штирлиц)")
    ISTJ: Optional[float] = Field(None, ge=0.0, le=1.0, description="ISTJ / SLI (Габен)")

    records: int = Field(..., description="Количество записей")

    def model_dump(self, **kwargs):
        """Переопределяем дамп"""
        include = {
            "id",
            "ENTP", "ISFJ", "ESFJ", "INTP",
            "ENFJ", "ISTP", "ESTP", "INFJ",
            "ESFP", "INTJ", "ENTJ", "ISFP",
            "ENFP", "INFP", "ESTJ", "ISTJ",
        }
        kwargs["include"] = include
        kwargs.setdefault("exclude_none", True)
        return super().model_dump(**kwargs)

    primary_type: Optional[str] = Field(None, description="Основной тип (например 'ENTP', 'INFJ')")

    # Вычисляемые поля - заполняются автоматически после инициализации
    quadra: Optional[str] = Field(None, description="Квадра типа")
    club: Optional[str] = Field(None, description="Клуб типа")

    # Базовые дихотомии
    extraversion: Optional[str] = Field(None, description="Экстраверсия/Интроверсия")
    intuition: Optional[str] = Field(None, description="Интуиция/Сенсорика")
    logic: Optional[str] = Field(None, description="Логика/Этика")
    rationality: Optional[str] = Field(None, description="Рациональность/Иррациональность")

    # Признаки Рейнина 5-15
    static: Optional[str] = Field(None, description="Статика/Динамика")
    positivist: Optional[str] = Field(None, description="Позитивизм/Негативизм")
    process: Optional[str] = Field(None, description="Процесс/Результат")
    declaring: Optional[str] = Field(None, description="Деклатимность/Демонстративность")
    constructivist: Optional[str] = Field(None, description="Конструктивизм/Эмотивизм")
    careful: Optional[str] = Field(None, description="Рассудительность/Решительность")
    farsighted: Optional[str] = Field(None, description="Дальновидность/Беспечность")
    judicious: Optional[str] = Field(None, description="Рассудительность/Решительность (вторая)")
    tactical: Optional[str] = Field(None, description="Тактика/Стратегия")
    questioning: Optional[str] = Field(None, description="Вопрошание/Утверждение")
    merging: Optional[str] = Field(None, description="Объединяющий/Разделяющий")

    # [ КВАДРАЛЬНЫЕ (одинаковы у всей КВАДРЫ) ]
    aristocratic: Optional[str] = Field(None, description="Аристократия / Демократия")
    merry: Optional[str] = Field(None, description="Весёлость / Серьёзность")
    yielding: Optional[str] = Field(None, description="Уступчивость / Упрямство")

    # Межтипные отношения (14 типов)
    dual: Optional[str] = Field(None, description="Дуал (идеальный партнёр)")
    conflict: Optional[str] = Field(None, description="Конфликтор (наихудшая совместимость)")
    activation: Optional[str] = Field(None, description="Активатор (бодрящие отношения)")
    mirror: Optional[str] = Field(None, description="Зеркальный (похожий, но видит недостатки)")
    kindred: Optional[str] = Field(None, description="Родственный (похожие ценности)")
    business: Optional[str] = Field(None, description="Деловой (хорошие коллеги)")
    supervisee: Optional[str] = Field(None, description="Подопечный (кого контролирует)")
    supervisor: Optional[str] = Field(None, description="Ревизор (кто контролирует)")
    illusory: Optional[str] = Field(None, description="Миражный (иллюзия понимания)")
    semi_dual: Optional[str] = Field(None, description="Полудуальный (частичное дополнение)")
    quasi_identical: Optional[str] = Field(None, description="Квазитождественный (похожий, но разный подход)")
    super_ego: Optional[str] = Field(None, description="Суперэго (моральные требования)")

    # Карта базовых дихотомий (ключи заменены на MBTI)
    _BASE_DICHOTOMIES = {
        "ENTP": (1, 1, 1, -1),  # ИЛЭ - Дон Кихот
        "ISFJ": (-1, -1, -1, -1),  # СЭИ - Дюма
        "ESFJ": (1, -1, -1, 1),  # ЭСЭ - Гюго
        "INTP": (-1, 1, 1, 1),  # ЛИИ - Робеспьер
        "ESTP": (1, -1, 1, -1),  # СЛЭ - Жуков
        "INFJ": (-1, 1, -1, -1),  # ИЭИ - Есенин
        "ENFJ": (1, -1, -1, -1),  # ЭИЭ - Гамлет
        "ISTP": (-1, -1, 1, 1),  # ЛСИ - Максим Горький
        "ESFP": (1, -1, -1, -1),  # СЭЭ - Цезарь
        "INTJ": (-1, 1, 1, -1),  # ИЛИ - Бальзак
        "ISFP": (-1, -1, -1, 1),  # ЭСИ - Драйзер
        "ENTJ": (1, 1, 1, 1),  # ЛИЭ - Джек Лондон
        "ENFP": (1, 1, -1, -1),  # ИЭЭ - Гексли
        "ISTJ": (-1, -1, 1, -1),  # СЛИ - Габен
        "INFP": (-1, 1, -1, 1),  # ЭИИ - Достоевский
        "ESTJ": (-1, -1, 1, 1),  # ЛСЭ - Штирлиц
    }

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

    @computed_field
    @property
    def accuracy_percent(self) -> float:
        """Процент точности"""
        records_count: int | None = self.records
        if records_count is None or records_count <= 0:
            return 0.0
        elif records_count == 1:
            return 0.04
        elif records_count == 2:
            return 0.09
        else:
            # при 7 записях: 42%
            # при 17 записях: 63%
            # при 27 записях: 71%
            # при 50 записях: 78%
            margin = 1.5081 / (records_count ** 0.5)
            return 1 - margin

    def __init__(self, **data):
        """Инициализация с автоматическим вычислением всех полей"""
        super().__init__(**data)
        self.set_primary_type()
        self._calculate_all_fields()

    def get_top_3_types(self) -> list:
        """отдает 3 самых вероятных типа"""
        type_probs = {
            "ENTP": self.ENTP, "ISFJ": self.ISFJ, "ESFJ": self.ESFJ, "INTP": self.INTP,
            "ENFJ": self.ENFJ, "ISTP": self.ISTP, "ESTP": self.ESTP, "INFJ": self.INFJ,
            "ESFP": self.ESFP, "INTJ": self.INTJ, "ENTJ": self.ENTJ, "ISFP": self.ISFP,
            "ENFP": self.ENFP, "INFP": self.INFP, "ESTJ": self.ESTJ, "ISTJ": self.ISTJ,
        }

        sorted_types = sorted(
            [[k, v] for k, v in type_probs.items() if v is not None],
            key=lambda x: x[1],
            reverse=True
        )

        return sorted_types[:3]

    def set_primary_type(self):
        """
        1. Определяем primary_type по максимальной вероятности, если не задан
        2. Нормализуем вероятности (опционально, но рекомендуется)
        3. Запускаем вычисления всех зависимых полей
        """
        type_probs = {
            "ENTP": self.ENTP, "ISFJ": self.ISFJ, "ESFJ": self.ESFJ, "INTP": self.INTP,
            "ENFJ": self.ENFJ, "ISTP": self.ISTP, "ESTP": self.ESTP, "INFJ": self.INFJ,
            "ESFP": self.ESFP, "INTJ": self.INTJ, "ENTJ": self.ENTJ, "ISFP": self.ISFP,
            "ENFP": self.ENFP, "INFP": self.INFP, "ESTJ": self.ESTJ, "ISTJ": self.ISTJ,
        }

        # Нормализация (если сумма ≠ 0 и не ≈ 1)
        total = sum(v for v in type_probs.values() if v is not None)
        if total > 0 and abs(total - 1.0) > 1e-6:
            for typ in type_probs:
                if type_probs[typ] is not None:
                    setattr(self, typ, type_probs[typ] / total)

        if not self.primary_type:
            max_prob = -1.0
            max_type = None
            for typ, prob in type_probs.items():
                if prob is not None and prob > max_prob:
                    max_prob = prob
                    max_type = typ
            if max_type:
                self.primary_type = max_type

        if not self.primary_type:
            raise ValueError("Не удалось определить primary_type — все вероятности равны None")

        return self

    def _calculate_all_fields(self):
        """Вычисляет и заполняет все поля на основе типа"""
        # Получаем базовые дихотомии
        E_I, N_S, T_F, J_P = self._BASE_DICHOTOMIES[self.primary_type]

        # Вычисляем производные дихотомии
        S_D = E_I * N_S  # Статика/Динамика
        P_N = E_I * T_F  # Позитивизм/Негативизм
        Proc_Res = E_I * J_P  # Процесс/Результат
        Decl_Dem = N_S * T_F  # Деклатимность/Демонстративность
        Constr_Emot = N_S * J_P  # Конструктивизм/Эмотивизм
        Care_Dar = T_F * J_P  # Рассудительность/Решительность
        Far_Obs = S_D * T_F  # Дальновидность/Беспечность
        Jud_Dec = S_D * J_P  # Рассудительность/Решительность (вторая)
        Tact_Strat = P_N * J_P  # Тактика/Стратегия
        Quest_Assert = S_D * Care_Dar  # Вопрошание/Утверждение
        Merg_Div = Decl_Dem * J_P  # Объединяющий/Разделяющий

        Arist_Dem = N_S * T_F * J_P  # Аристократия / Демократия
        Merry_Ser = E_I * N_S * T_F  # Весёлость / Серьёзность (Merry/Serious)
        Yield_Obst = E_I * T_F * J_P  # Уступчивость / Упрямство (Yielding/Obstinate)

        # ============ БАЗОВЫЕ ДИХОТОМИИ ============
        self.extraversion = "Экстраверт" if E_I == 1 else "Интроверт"
        self.intuition = "Интуит" if N_S == 1 else "Сенсорик"
        self.logic = "Логик" if T_F == 1 else "Этик"
        self.rationality = "Рационал" if J_P == 1 else "Иррационал"

        # ============ ПРИЗНАКИ РЕЙНИНА ============
        self.static = "Статик" if S_D == 1 else "Динамик"
        self.positivist = "Позитивист" if P_N == 1 else "Негативист"
        self.process = "Процесс" if Proc_Res == 1 else "Результат"
        self.declaring = "Деклатим" if Decl_Dem == 1 else "Демонстратив"
        self.constructivist = "Конструктивист" if Constr_Emot == 1 else "Эмотивист"
        self.careful = "Рассудительный" if Care_Dar == 1 else "Решительный"
        self.farsighted = "Дальновидный" if Far_Obs == 1 else "Беспечный"
        self.judicious = "Рассудительный" if Jud_Dec == 1 else "Решительный"
        self.tactical = "Тактик" if Tact_Strat == 1 else "Стратег"
        self.questioning = "Вопрошающий" if Quest_Assert == 1 else "Утверждающий"
        self.merging = "Объединяющий" if Merg_Div == 1 else "Разделяющий"

        self.aristocratic = "Аристократ" if Arist_Dem == 1 else "Демократ"
        self.merry = "Весёлый" if Merry_Ser == 1 else "Серьёзный"
        self.yielding = "Уступчивый" if Yield_Obst == 1 else "Упрямый"

        # ============ КВАДРА И КЛУБ ============
        # Карта квадр (ключи заменены на MBTI)
        quadra_map = {
            "ENTP": "Альфа", "ISFJ": "Альфа", "ESFJ": "Альфа", "INTP": "Альфа",
            "ESTP": "Бета", "INFJ": "Бета", "ENFJ": "Бета", "ISTP": "Бета",
            "ESFP": "Гамма", "INTJ": "Гамма", "ENTJ": "Гамма", "ISFP": "Гамма",
            "ESTJ": "Дельта", "INFP": "Дельта", "ENFP": "Дельта", "ISTJ": "Дельта",
        }
        self.quadra = quadra_map.get(self.primary_type, "Неизвестно")

        # Карта клубов (ключи заменены на MBTI)
        club_map = {
            "ENTP": "Исследователи", "INTP": "Исследователи",
            "INTJ": "Исследователи", "ENTJ": "Исследователи",
            "ENFP": "Социальные", "INFP": "Социальные",
            "INFJ": "Социальные", "ENFJ": "Социальные",
            "ESTP": "Практики", "ISTP": "Практики",
            "ESTJ": "Практики", "ISTJ": "Практики",
            "ISFJ": "Гуманитарии", "ESFJ": "Гуманитарии",
            "ESFP": "Гуманитарии", "ISFP": "Гуманитарии",
        }
        self.club = club_map.get(self.primary_type, "Неизвестно")

        # ============ МЕЖТИПНЫЕ ОТНОШЕНИЯ ============
        # Карта дуалов (ключи и значения заменены на MBTI)
        dual_map = {
            "ENTP": "ISFJ", "ISFJ": "ENTP",
            "ESFJ": "INTP", "INTP": "ESFJ",
            "ESTP": "INFJ", "INFJ": "ESTP",
            "ENFJ": "ISTP", "ISTP": "ENFJ",
            "ESFP": "INTJ", "INTJ": "ESFP",
            "ENTJ": "ISFP", "ISFP": "ENTJ",
            "ESTJ": "INFP", "INFP": "ESTJ",
            "ENFP": "ISTJ", "ISTJ": "ENFP",
        }
        self.dual = dual_map.get(self.primary_type, "Неизвестно")

        # Карта конфликторов
        conflict_map = {
            "ENTP": "ISFP", "ISFJ": "ENTJ",
            "ESFJ": "INTJ", "INTP": "ESFP",
            "ESTP": "INFP", "INFJ": "ESTJ",
            "ENFJ": "ISTJ", "ISTP": "ENFP",
            "ESFP": "INTP", "INTJ": "ESFJ",
            "ENTJ": "ISFJ", "ISFP": "ENTP",
            "ESTJ": "INFJ", "INFP": "ESTP",
            "ENFP": "ISTP", "ISTJ": "ENFJ",
        }
        self.conflict = conflict_map.get(self.primary_type, "Неизвестно")

        # Карта активаторов
        activation_map = {
            "ENTP": "ESFJ", "ESFJ": "ENTP",
            "ISFJ": "INTP", "INTP": "ISFJ",
            "ESTP": "ENFJ", "ENFJ": "ESTP",
            "INFJ": "ISTP", "ISTP": "INFJ",
            "ESFP": "ENTJ", "ENTJ": "ESFP",
            "INTJ": "ISFP", "ISFP": "INTJ",
            "ESTJ": "ENFP", "ENFP": "ESTJ",
            "INFP": "ISTJ", "ISTJ": "INFP",
        }
        self.activation = activation_map.get(self.primary_type, "Неизвестно")

        # Карта зеркальных типов
        mirror_map = {
            "ENTP": "INTP", "INTP": "ENTP",
            "ISFJ": "ESFJ", "ESFJ": "ISFJ",
            "ESTP": "ISTP", "ISTP": "ESTP",
            "INFJ": "ENFJ", "ENFJ": "INFJ",
            "ESFP": "ISFP", "ISFP": "ESFP",
            "INTJ": "ENTJ", "ENTJ": "INTJ",
            "ESTJ": "ISTJ", "ISTJ": "ESTJ",
            "INFP": "ENFP", "ENFP": "INFP",
        }
        self.mirror = mirror_map.get(self.primary_type, "Неизвестно")

        # Родственные
        kindred_map = {
            "ENTP": "ENTJ", "ENTJ": "ENTP",
            "ISFJ": "ISTJ", "ISTJ": "ISFJ",
            "ESFJ": "ESFP", "ESFP": "ESFJ",
            "INTP": "INTJ", "INTJ": "INTP",
            "ESTP": "ESTJ", "ESTJ": "ESTP",
            "INFJ": "ENFP", "ENFP": "INFJ",
            "ENFJ": "ISTP", "ISTP": "ENFJ",
            "INFP": "ISFP", "ISFP": "INFP",
        }
        self.kindred = kindred_map.get(self.primary_type)

        # Деловые
        business_map = {
            "ENTP": "ESFJ", "ESFJ": "ENTP",
            "ISFJ": "INTP", "INTP": "ISFJ",
            "ESTP": "ENFJ", "ENFJ": "ESTP",
            "INFJ": "ISTP", "ISTP": "INFJ",
            "ESFP": "ENTJ", "ENTJ": "ESFP",
            "INTJ": "ISFP", "ISFP": "INTJ",
            "ESTJ": "ENFP", "ENFP": "ESTJ",
            "INFP": "ISTJ", "ISTJ": "INFP",
        }
        self.business = business_map.get(self.primary_type)

        # Подопечный (кого контролирует)
        supervisee_map = {
            "ENTP": "ISTP", "ESFJ": "INFJ",
            "ISFJ": "ENFJ", "INTP": "ESTP",
            "ESTP": "ESFP", "INFJ": "INTJ",
            "ENFJ": "ENTJ", "ISTP": "ISFP",
            "ESFP": "ESTP", "INTJ": "INFJ",
            "ENTJ": "ENFJ", "ISFP": "ISTP",
            "ESTJ": "ISFJ", "INFP": "ENTP",
            "ENFP": "INTP", "ISTJ": "ESFJ",
        }
        self.supervisee = supervisee_map.get(self.primary_type)

        # Ревизор (кто контролирует)
        supervisor_map = {
            "ENTP": "INFP", "ESFJ": "ISTJ",
            "ISFJ": "ESTJ", "INTP": "ENFP",
            "ESTP": "INTP", "INFJ": "ESFJ",
            "ENFJ": "ISFJ", "ISTP": "ENTP",
            "ESFP": "ISTP", "INTJ": "ENFJ",
            "ENTJ": "INFJ", "ISFP": "ESTP",
            "ESTJ": "ESFP", "INFP": "INTJ",
            "ENFP": "ENTJ", "ISTJ": "INFP",
        }
        self.supervisor = supervisor_map.get(self.primary_type)

        # Миражные
        illusory_map = {
            "ENTP": "ENFP", "ISFJ": "ISTJ",
            "ESFJ": "INFP", "INTP": "ESTJ",
            "ESTP": "ESFP", "INFJ": "ISFP",
            "ENFJ": "ISTP", "ISTP": "ENFJ",
            "ESFP": "ESTP", "INTJ": "INTP",
            "ENTJ": "ENTP", "ISFP": "INFJ",
            "ESTJ": "INTP", "INFP": "ESFJ",
            "ENFP": "ENTP", "ISTJ": "ISFJ",
        }
        self.illusory = illusory_map.get(self.primary_type)

        # Полудуальные
        semi_dual_map = {
            "ENTP": "INFP", "ISFJ": "ESTJ",
            "ESFJ": "ISTJ", "INTP": "ENFP",
            "ESTP": "INTJ", "INFJ": "ESFP",
            "ENFJ": "ISTP", "ISTP": "ENFJ",
            "ESFP": "INFJ", "INTJ": "ESTP",
            "ENTJ": "ISFP", "ISFP": "ENTJ",
            "ESTJ": "ISFJ", "INFP": "ENTP",
            "ENFP": "INTP", "ISTJ": "ESFJ",
        }
        self.semi_dual = semi_dual_map.get(self.primary_type)

        # Квазитождественные
        quasi_identical_map = {
            "ENTP": "INTJ", "ISFJ": "ESFP",
            "ESFJ": "ISFP", "INTP": "ENTJ",
            "ESTP": "ISTJ", "INFJ": "ENFP",
            "ENFJ": "INFP", "ISTP": "ESTJ",
            "ESFP": "ISFJ", "INTJ": "ENTP",
            "ENTJ": "INTP", "ISFP": "ESFJ",
            "ESTJ": "ISTP", "INFP": "ENFJ",
            "ENFP": "INFJ", "ISTJ": "ESTP",
        }
        self.quasi_identical = quasi_identical_map.get(self.primary_type)

        # Суперэго
        super_ego_map = {
            "ENTP": "ISFP", "ISFJ": "ENTJ",
            "ESFJ": "INTJ", "INTP": "ESFP",
            "ESTP": "INFP", "INFJ": "ESTJ",
            "ENFJ": "ISTJ", "ISTP": "ENFP",
            "ESFP": "INTP", "INTJ": "ESFJ",
            "ENTJ": "ISFJ", "ISFP": "ENTP",
            "ESTJ": "INFJ", "INFP": "ESTP",
            "ENFP": "ISTP", "ISTJ": "ENFJ",
        }
        self.super_ego = super_ego_map.get(self.primary_type)

    # ============ МЕТОДЫ ДЛЯ СРАВНЕНИЯ ============
    def get_relationship_with(self, other_type: str) -> RelationshipType:
        """Возвращает тип отношения с другим типом"""
        if self.primary_type == other_type:
            return RelationshipType.IDENTICAL

        # Карта соответствия полей схемы типам отношений
        relation_map = {
            RelationshipType.DUAL: self.dual,
            RelationshipType.CONFLICT: self.conflict,
            RelationshipType.ACTIVATION: self.activation,
            RelationshipType.MIRROR: self.mirror,
            RelationshipType.KIND_RED: self.kindred,
            RelationshipType.BUSINESS: self.business,
            RelationshipType.SUPERVISEE: self.supervisee,
            RelationshipType.SUPERVISOR: self.supervisor,
            RelationshipType.ILLUSORY: self.illusory,
            RelationshipType.SEMI_DUAL: self.semi_dual,
            RelationshipType.QUASI_IDENTICAL: self.quasi_identical,
            RelationshipType.SUPER_EGO: self.super_ego,
        }

        for relation_type, relation_field in relation_map.items():
            if relation_field == other_type:
                return relation_type

        return RelationshipType.OTHER


# [ СХЕМА СРАВНЕНИЯ ]
class SocionicsComparisonSchema(BaseModel):
    """Схема для сравнения двух соционических типов"""
    id: Optional[UUID] = Field(default_factory=uuid4)

    type_a: str = Field(..., description="Первый тип")
    type_b: str = Field(..., description="Второй тип")

    # Вычисляемые поля
    schema_a: Optional['UserSocionicsSchema'] = Field(None, description="Схема первого типа")
    schema_b: Optional['UserSocionicsSchema'] = Field(None, description="Схема второго типа")

    relationship: Optional[RelationshipType] = Field(None, description="Тип отношения между типами")
    shared_dichotomies: Optional[List[str]] = Field(None, description="Совпадающие дихотомии")
    different_dichotomies: Optional[List[str]] = Field(None, description="Различающиеся дихотомии")
    compatibility_score: Optional[float] = Field(None, description="Оценка совместимости (0-100)")

    class Config:
        arbitrary_types_allowed = True

    @field_validator('type_a', 'type_b')
    def validate_socionics_type(cls, v):
        """Валидация типа"""
        v = v.upper()
        valid_types = ["ENTP", "ISFJ", "ESFJ", "INTP", "ESTP", "INFJ", "ENFJ", "ISTP",
                       "ESFP", "INTJ", "ENTJ", "ISFP", "ENFP", "INFP", "ESTJ", "ISTJ"]
        if v not in valid_types:
            raise ValueError(f"Неизвестный тип: {v}")
        return v

    def __init__(self, **data):
        """Инициализация с автоматическим вычислением сравнения"""
        super().__init__(**data)
        self._calculate_comparison()

    def _calculate_comparison(self):
        """Вычисляет все поля сравнения"""
        # Создаем схемы пользователей
        self.schema_a = UserSocionicsSchema(socionics_type=self.type_a)
        self.schema_b = UserSocionicsSchema(socionics_type=self.type_b)

        # Определяем тип отношения
        self.relationship = self.schema_a.get_relationship_with(self.type_b)

        # Получаем все дихотомии
        dich_a = self.schema_a.get_all_dichotomies()
        dich_b = self.schema_b.get_all_dichotomies()

        # Определяем совпадающие и различающиеся дихотомии
        shared = []
        different = []

        for name, value_a in dich_a.items():
            value_b = dich_b.get(name)
            if value_a == value_b:
                shared.append(name)
            else:
                different.append(name)

        self.shared_dichotomies = shared
        self.different_dichotomies = different

        # Вычисляем оценку совместимости
        self.compatibility_score = self._calculate_compatibility_score()

    def _calculate_compatibility_score(self) -> float:
        """Вычисляет оценку совместимости (0-100)"""
        # Базовая оценка по совпадающим признакам (15 признаков Рейнина)
        total_dichotomies = 15
        shared_count = len(self.shared_dichotomies)
        base_score = (shared_count / total_dichotomies) * 60  # Максимум 60% за признаки

        # Бонусы/штрафы за тип отношений
        relation_bonuses = {
            RelationshipType.DUAL: 30,
            RelationshipType.ACTIVATION: 15,
            RelationshipType.MIRROR: 10,
            RelationshipType.KIND_RED: 5,
            RelationshipType.BUSINESS: 10,
            RelationshipType.SEMI_DUAL: 8,
            RelationshipType.QUASI_IDENTICAL: 3,
            RelationshipType.OTHER: 0,
            RelationshipType.IDENTICAL: 5,
            RelationshipType.SUPERVISEE: -10,
            RelationshipType.SUPERVISOR: -10,
            RelationshipType.ILLUSORY: -15,
            RelationshipType.SUPER_EGO: -20,
            RelationshipType.CONFLICT: -40,
        }

        # Добавляем бонус за отношение
        bonus = relation_bonuses.get(self.relationship, 0)

        # Бонус за одну квадру (если не учтен в отношениях выше)
        if self.schema_a.is_same_quadra(self.type_b) and self.relationship not in [
            RelationshipType.DUAL, RelationshipType.ACTIVATION, RelationshipType.MIRROR
        ]:
            bonus += 5

        # Бонус за один клуб
        if self.schema_a.club == self.schema_b.club:
            bonus += 3

        score = base_score + bonus
        return max(0, min(100, round(score, 1)))

    @property
    def compatibility_level(self) -> str:
        """Уровень совместимости по оценке"""
        score = self.compatibility_score or 0
        if score >= 80:
            return "Отличная"
        elif score >= 60:
            return "Хорошая"
        elif score >= 40:
            return "Умеренная"
        elif score >= 20:
            return "Низкая"
        else:
            return "Очень низкая"

    def _get_relationship_description(self) -> str:
        """Получить описание типа отношений"""
        descriptions = {
            RelationshipType.DUAL: "Идеальная совместимость, взаимное дополнение",
            RelationshipType.CONFLICT: "Наихудшая совместимость, постоянные конфликты",
            RelationshipType.ACTIVATION: "Бодрящие отношения, взаимная активация",
            RelationshipType.MIRROR: "Похожи, но видят недостатки друг друга",
            RelationshipType.IDENTICAL: "Одинаковый тип, полное понимание",
            RelationshipType.KIND_RED: "Похожие ценности и мировоззрение",
            RelationshipType.BUSINESS: "Хорошие деловые партнеры",
            RelationshipType.SUPERVISEE: "Контролирует",
            RelationshipType.SUPERVISOR: "Контролируется",
            RelationshipType.ILLUSORY: "Иллюзия понимания, часто недопонимание",
            RelationshipType.SEMI_DUAL: "Частичное дополнение, неплохая совместимость",
            RelationshipType.QUASI_IDENTICAL: "Похожи, но разный подход к задачам",
            RelationshipType.SUPER_EGO: "Высокие моральные требования друг к другу",
            RelationshipType.OTHER: "Нейтральные отношения",
        }
        return descriptions.get(self.relationship or RelationshipType.OTHER, "Нейтральные отношения")
