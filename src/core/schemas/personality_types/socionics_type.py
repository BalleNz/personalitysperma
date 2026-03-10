from typing import Optional
from uuid import uuid4, UUID

from pydantic import BaseModel, Field, computed_field


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

    records: int | None = Field(
        default=None,
        description="Количество записей"
    )

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

    quadra: Optional[str] = Field(None, description="Квадра типа")
    club: Optional[str] = Field(None, description="Клуб типа")

    # [ Базовые дихотомии ]
    extraversion: Optional[str] = Field(None, description="Экстраверсия/Интроверсия")
    intuition: Optional[str] = Field(None, description="Интуиция/Сенсорика")
    logic: Optional[str] = Field(None, description="Логика/Этика")
    rationality: Optional[str] = Field(None, description="Рациональность/Иррациональность")

    # [ Признаки Рейнина ]
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

    # [ КВАДРАЛЬНЫЕ ]
    aristocratic: Optional[str] = Field(None, description="Аристократия / Демократия")
    merry: Optional[str] = Field(None, description="Весёлость / Серьёзность")
    yielding: Optional[str] = Field(None, description="Уступчивость / Упрямство")

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

    def is_same_quadra(self, other_type: str) -> bool:
        """Проверяет, находится ли другой тип в той же квадре"""
        if not self.primary_type or not other_type:
            return False

        other_type = other_type.strip().upper()

        quadra_map = {
            "ENTP": "Альфа", "ISFJ": "Альфа", "ESFJ": "Альфа", "INTP": "Альфа",
            "ESTP": "Бета", "INFJ": "Бета", "ENFJ": "Бета", "ISTP": "Бета",
            "ESFP": "Гамма", "INTJ": "Гамма", "ENTJ": "Гамма", "ISFP": "Гамма",
            "ESTJ": "Дельта", "INFP": "Дельта", "ENFP": "Дельта", "ISTJ": "Дельта",
        }

        return quadra_map.get(self.primary_type) == quadra_map.get(other_type)

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

        # [ производные дихотомии ]
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
