from typing import List, Optional
from uuid import uuid4, UUID

from pydantic import BaseModel, Field, field_validator

from src.core.enums.socionics import (
    RelationshipType
)


class UserSocionicsSchema(BaseModel):
    """Схема соционического профиля пользователя"""
    id: Optional[UUID] = Field(default_factory=uuid4)

    # Основное поле - задаётся при создании
    socionics_type: str = Field(
        ...,
        description="Соционический тип (4-буквенный код)"
    )

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

    # Карта базовых дихотомий
    _BASE_DICHOTOMIES = {
        "ILE": (1, 1, 1, -1),  # ИЛЭ - Дон Кихот
        "SEI": (-1, -1, -1, -1),  # СЭИ - Дюма
        "ESE": (1, -1, -1, 1),  # ЭСЭ - Гюго
        "LII": (-1, 1, 1, 1),  # ЛИИ - Робеспьер
        "SLE": (1, -1, 1, -1),  # СЛЭ - Жуков
        "IEI": (-1, 1, -1, -1),  # ИЭИ - Есенин
        "EIE": (1, -1, -1, -1),  # ЭИЭ - Гамлет
        "LSI": (-1, -1, 1, 1),  # ЛСИ - Максим Горький
        "SEE": (1, -1, -1, -1),  # СЭЭ - Цезарь
        "ILI": (-1, 1, 1, -1),  # ИЛИ - Бальзак
        "ESI": (-1, -1, -1, 1),  # ЭСИ - Драйзер
        "LIE": (1, 1, 1, 1),  # ЛИЭ - Джек Лондон
        "IEE": (1, 1, -1, -1),  # ИЭЭ - Гексли
        "SLI": (-1, -1, 1, -1),  # СЛИ - Габен
        "EII": (-1, 1, -1, 1),  # ЭИИ - Достоевский
        "LSE": (-1, -1, 1, 1),  # ЛСЭ - Штирлиц
    }

    class Config:
        arbitrary_types_allowed = True

    @field_validator('socionics_type')
    def validate_socionics_type(cls, v):
        """Валидация типа"""
        v = v.upper()
        if v not in cls._BASE_DICHOTOMIES:
            valid_types = ", ".join(sorted(cls._BASE_DICHOTOMIES.keys()))
            raise ValueError(f"Неизвестный тип: {v}. Допустимые: {valid_types}")
        return v

    def __init__(self, **data):
        """Инициализация с автоматическим вычислением всех полей"""
        super().__init__(**data)
        self._calculate_all_fields()

    def _calculate_all_fields(self):
        """Вычисляет и заполняет все поля на основе типа"""
        # Получаем базовые дихотомии
        E_I, N_S, T_F, J_P = self._BASE_DICHOTOMIES[self.socionics_type]

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

        # ============ КВАДРА И КЛУБ ============
        # Карта квадр
        quadra_map = {
            "ILE": "Альфа", "SEI": "Альфа", "ESE": "Альфа", "LII": "Альфа",
            "SLE": "Бета", "IEI": "Бета", "EIE": "Бета", "LSI": "Бета",
            "SEE": "Гамма", "ILI": "Гамма", "LIE": "Гамма", "ESI": "Гамма",
            "LSE": "Дельта", "EII": "Дельта", "IEE": "Дельта", "SLI": "Дельта",
        }
        self.quadra = quadra_map.get(self.socionics_type, "Неизвестно")

        # Карта клубов
        club_map = {
            "ILE": "Исследователи", "LII": "Исследователи",
            "ILI": "Исследователи", "LIE": "Исследователи",
            "IEE": "Социальные", "EII": "Социальные",
            "IEI": "Социальные", "EIE": "Социальные",
            "SLE": "Практики", "LSI": "Практики",
            "LSE": "Практики", "SLI": "Практики",
            "SEI": "Гуманитарии", "ESE": "Гуманитарии",
            "SEE": "Гуманитарии", "ESI": "Гуманитарии",
        }
        self.club = club_map.get(self.socionics_type, "Неизвестно")

        # ============ МЕЖТИПНЫЕ ОТНОШЕНИЯ ============
        # Карта дуалов
        dual_map = {
            "ILE": "SEI", "SEI": "ILE",
            "ESE": "LII", "LII": "ESE",
            "SLE": "IEI", "IEI": "SLE",
            "EIE": "LSI", "LSI": "EIE",
            "SEE": "ILI", "ILI": "SEE",
            "LIE": "ESI", "ESI": "LIE",
            "LSE": "EII", "EII": "LSE",
            "IEE": "SLI", "SLI": "IEE",
        }
        self.dual = dual_map.get(self.socionics_type, "Неизвестно")

        # Карта конфликторов
        conflict_map = {
            "ILE": "ESI", "SEI": "LIE",
            "ESE": "ILI", "LII": "SEE",
            "SLE": "EII", "IEI": "LSE",
            "EIE": "SLI", "LSI": "IEE",
            "SEE": "LII", "ILI": "ESE",
            "LIE": "SEI", "ESI": "ILE",
            "LSE": "IEI", "EII": "SLE",
            "IEE": "LSI", "SLI": "EIE",
        }
        self.conflictor = conflict_map.get(self.socionics_type, "Неизвестно")

        # Карта активаторов
        activation_map = {
            "ILE": "ESE", "ESE": "ILE",
            "SEI": "LII", "LII": "SEI",
            "SLE": "EIE", "EIE": "SLE",
            "IEI": "LSI", "LSI": "IEI",
            "SEE": "LIE", "LIE": "SEE",
            "ILI": "ESI", "ESI": "ILI",
            "LSE": "IEE", "IEE": "LSE",
            "EII": "SLI", "SLI": "EII",
        }
        self.activation = activation_map.get(self.socionics_type, "Неизвестно")

        # Карта зеркальных типов
        mirror_map = {
            "ILE": "LII", "LII": "ILE",
            "SEI": "ESE", "ESE": "SEI",
            "SLE": "LSI", "LSI": "SLE",
            "IEI": "EIE", "EIE": "IEI",
            "SEE": "ESI", "ESI": "SEE",
            "ILI": "LIE", "LIE": "ILI",
            "LSE": "SLI", "SLI": "LSE",
            "EII": "IEE", "IEE": "EII",
        }
        self.mirror = mirror_map.get(self.socionics_type, "Неизвестно")

        # Родственные
        kindred_map = {
            "ILE": "LIE", "LIE": "ILE",
            "SEI": "SLI", "SLI": "SEI",
            "ESE": "SEE", "SEE": "ESE",
            "LII": "ILI", "ILI": "LII",
            "SLE": "LSE", "LSE": "SLE",
            "IEI": "IEE", "IEE": "IEI",
            "EIE": "LSI", "LSI": "EIE",
            "EII": "ESI", "ESI": "EII",
        }
        self.kindred = kindred_map.get(self.socionics_type)

        # Деловые
        business_map = {
            "ILE": "ESE", "ESE": "ILE",
            "SEI": "LII", "LII": "SEI",
            "SLE": "EIE", "EIE": "SLE",
            "IEI": "LSI", "LSI": "IEI",
            "SEE": "LIE", "LIE": "SEE",
            "ILI": "ESI", "ESI": "ILI",
            "LSE": "IEE", "IEE": "LSE",
            "EII": "SLI", "SLI": "EII",
        }
        self.business = business_map.get(self.socionics_type)

        # Подопечный (кого контролирует)
        supervisee_map = {
            "ILE": "LSI", "ESE": "IEI",
            "SEI": "EIE", "LII": "SLE",
            "SLE": "SEE", "IEI": "ILI",
            "EIE": "LIE", "LSI": "ESI",
            "SEE": "SLE", "ILI": "IEI",
            "LIE": "EIE", "ESI": "LSI",
            "LSE": "SEI", "EII": "ILE",
            "IEE": "LII", "SLI": "ESE",
        }
        self.supervisee = supervisee_map.get(self.socionics_type)

        # Ревизор (кто контролирует)
        supervisor_map = {
            "ILE": "EII", "ESE": "SLI",
            "SEI": "LSE", "LII": "IEE",
            "SLE": "LII", "IEI": "ESE",
            "EIE": "SEI", "LSI": "ILE",
            "SEE": "LSI", "ILI": "EIE",
            "LIE": "IEI", "ESI": "SLE",
            "LSE": "SEE", "EII": "ILI",
            "IEE": "LIE", "SLI": "EII",
        }
        self.supervisor = supervisor_map.get(self.socionics_type)

        # Миражные
        illusory_map = {
            "ILE": "IEE", "SEI": "SLI",
            "ESE": "EII", "LII": "LSE",
            "SLE": "SEE", "IEI": "ESI",
            "EIE": "LSI", "LSI": "EIE",
            "SEE": "SLE", "ILI": "LII",
            "LIE": "ILE", "ESI": "IEI",
            "LSE": "LII", "EII": "ESE",
            "IEE": "ILE", "SLI": "SEI",
        }
        self.illusory = illusory_map.get(self.socionics_type)

        # Полудуальные
        semi_dual_map = {
            "ILE": "EII", "SEI": "LSE",
            "ESE": "SLI", "LII": "IEE",
            "SLE": "ILI", "IEI": "SEE",
            "EIE": "LSI", "LSI": "EIE",
            "SEE": "IEI", "ILI": "SLE",
            "LIE": "ESI", "ESI": "LIE",
            "LSE": "SEI", "EII": "ILE",
            "IEE": "LII", "SLI": "ESE",
        }
        self.semi_dual = semi_dual_map.get(self.socionics_type)

        # Квазитождественные
        quasi_identical_map = {
            "ILE": "ILI", "SEI": "SEE",
            "ESE": "ESI", "LII": "LIE",
            "SLE": "SLI", "IEI": "IEE",
            "EIE": "EII", "LSI": "LSE",
            "SEE": "SEI", "ILI": "ILE",
            "LIE": "LII", "ESI": "ESE",
            "LSE": "LSI", "EII": "EIE",
            "IEE": "IEI", "SLI": "SLE",
        }
        self.quasi_identical = quasi_identical_map.get(self.socionics_type)

        # Суперэго
        super_ego_map = {
            "ILE": "ESI", "SEI": "LIE",
            "ESE": "ILI", "LII": "SEE",
            "SLE": "EII", "IEI": "LSE",
            "EIE": "SLI", "LSI": "IEE",
            "SEE": "LII", "ILI": "ESE",
            "LIE": "SEI", "ESI": "ILE",
            "LSE": "IEI", "EII": "SLE",
            "IEE": "LSI", "SLI": "EIE",
        }
        self.super_ego = super_ego_map.get(self.socionics_type)

    # ============ МЕТОДЫ ДЛЯ СРАВНЕНИЯ ============
    def get_relationship_with(self, other_type: str) -> RelationshipType:
        """Возвращает тип отношения с другим типом"""
        if self.socionics_type == other_type:
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
        valid_types = ["ILE", "SEI", "ESE", "LII", "SLE", "IEI", "EIE", "LSI",
                       "SEE", "ILI", "ESI", "LIE", "IEE", "SLI", "EII", "LSE"]
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
