from PyroUbot.core.database import mongo_client

filters_col = mongo_client.pyroubot.filters

def add_filter_db(chat_id: str, keyword: str, response: str):
    filters_col.update_one(
        {"chat_id": chat_id, "keyword": keyword},
        {"$set": {"response": response}},
        upsert=True
    )

def delete_filter_db(chat_id: str, keyword: str):
    return filters_col.delete_one({"chat_id": chat_id, "keyword": keyword})

def get_filters_db(chat_id: str):
    return list(filters_col.find({"chat_id": chat_id}))

def match_filter(chat_id: str, text: str):
    filters = filters_col.find({"chat_id": chat_id})
    for f in filters:
        if f["keyword"] in text:
            return f["response"]
    return None
