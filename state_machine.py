from enum import Enum

class State(str, Enum):
    START = "start"
    CLIENT_TYPE = "client_type"
    INN = "inn"
    PURCHASE_GOAL = "purchase_goal"
    GOV_INN = "gov_inn"
    PURCHASE_METHOD = "purchase_method"
    NEED_TZ = "need_tz"
    NEED_INSTALL = "need_install"
    NEED_TRAINING = "need_training"
    DEADLINE = "deadline"
    CONTACTS = "contacts"
    END = "end"
    BLOCKED = "blocked"

# Память бота
user_states = {}         # chat_id -> State
user_data = {}           # chat_id -> dict
last_messages = {}       # chat_id -> str

def get_state(chat_id: str) -> State:
    return user_states.get(chat_id, State.START)

def set_state(chat_id: str, state: State):
    user_states[chat_id] = state

def get_last_message(chat_id: str) -> str:
    return last_messages.get(chat_id, "")

def set_last_message(chat_id: str, text: str):
    last_messages[chat_id] = text
