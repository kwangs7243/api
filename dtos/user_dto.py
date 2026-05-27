class SingUpDto:
    def __init__(self, login_id, passwd, name):
        self.login_id = login_id
        self.passwd = passwd
        self.name = name

class SingInDto:
    def __init__(self, login_id, passwd):
        self.login_id = login_id
        self.passwd = passwd


        