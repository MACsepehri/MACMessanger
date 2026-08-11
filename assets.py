def check_session(session):

    if not session:
        session["login"] = False
        session["profile"] = {}
        session["chat_data"] = []

        return False

    if not session.get("login", False):
        return False

    return True