from enum import Enum

# Словарь для хранения состояния пользователей
user_states = {}

# Перечисление всех возможных состояний
class State(str, Enum):
    START = "start"
    CLIENT_TYPE = "client_type"

    # Юрлица
    INN = "inn"
    PURPOSE = "purpose"
    GOV_ORG_INN = "gov_org_inn"
    GET_COMMERCIAL_OFFER = "get_commercial_offer"
    TO_SITE = "to_site"

    # Госучреждения
    GOV_INN = "gov_inn"
    PURCHASE_METHOD = "purchase_method"
    ADDITIONAL_SERVICES = "additional_services"
    HELP_WITH_TZ = "help_with_tz"
    EMAIL_APPLICATION = "email_application"

    # Общие
    DEADLINES = "deadlines"
    CONTACTS = "contacts"
    DONE = "done"

# Получить состояние пользователя по chat_id
def get_state(chat_id: str) -> State:
    return user_states.get(chat_id, State.START)

# Установить новое состояние для пользователя
def set_state(chat_id: str, state: State):
    user_states[chat_id] = state
