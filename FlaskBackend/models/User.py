#creating the user class
class User:
    def __init__(self, userid:str, fullname:str, username:str, password:str, usertype: str):
        self.userid = userid
        self.fullname = fullname
        self.username = username
        self.password = password
        self.usertype = usertype
        