from HOKAGE import mongodb as db_x

HOKAGE = db_x["CHATBOT"]


def add_chat(chat_id):
    hima = HOKAGE.find_one({"chat_id": chat_id})
    if hima:
        return False
    HOKAGE.insert_one({"chat_id": chat_id})
    return True


def remove_chat(chat_id):
    hima = HOKAGE.find_one({"chat_id": chat_id})
    if not hima:
        return False
    HOKAGE.delete_one({"chat_id": chat_id})
    return True


def get_all_chats():
    r = list(HOKAGE.find())
    if r:
        return r
    return False


def get_session(chat_id):
    hima = HOKAGE.find_one({"chat_id": chat_id})
    if not hima:
        return False
    return hima
