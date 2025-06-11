
from enum import Enum

class State(Enum):
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
    BLOCKED = "blocked"  # для физлиц

# Временное хранилище
user_states = {}       # chat_id -> State
user_data = {}         # chat_id -> dict
