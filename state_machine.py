from enum import Enum

# FSM состояния
class State(str, Enum):
    START = "start"
    CLIENT_TYPE = "client_type"
    INN = "inn"
    PURPOSE = "purpose"
    GOV_PURCHASE_METHOD = "gov_purchase_method"
    GOV_PARTNER_INN = "gov_partner_inn"
    EXTRA_SERVICES = "extra_services"
    DEADLINE = "deadline"
    CONTACTS = "contacts"

# Хранилища состояний и контекста
_states = {}
_contexts = {}

def get_state(user_id):
    return _states.get(user_id, State.START)

def set_state(user_id, state):
    _states[user_id] = state

def get_context(user_id):
    return _contexts.get(user_id, {})

def update_context(user_id, data):
    if user_id not in _contexts:
        _contexts[user_id] = {}
    _contexts[user_id].update(data)  # добавляем или обновляем значения
