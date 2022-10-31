class Entry:
    def __init__(self, _name):
        self._name = _name

    def setter(self, id,title,body):
        self.id = id
        self.title = title
        self.body = body
        self.blenth = len(body)  # attribute meant to take the initial legnth of the body which is in VIEW when entry is read

    def check_if_update(self, _id, _body):
        self._body = _body
        if _id == self.id:
            if len(_body) > len(self.body):
                return True
        else:
            return False
    def send_update(self):
        return (self.id,self.title,self._body)