class Extension:
    def __init__(self, session):
        self.session = session

    def checkSession(self):
        result = None
        if not self.session:
            self.session["profile"] = {}
            self.session["login"] = False
            self.session["chat"] = {}
            result = False
        elif not self.session["login"]:
            result = False
        else:
            result = True
        return (self.session, result)

    def createAccount(self, new_profile_data):
        self.session["login"] = True
        self.session["profile"] = new_profile_data
        return self.session

    