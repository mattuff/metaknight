class component:

    def __init__(self, handle, framing):
        self.handle = handle
        self.framing = framing

    def getHandle(self):
        return self.handle

    def getFraming(self):
        return self.framing

    def changeFraming(self, f):
        framing=f
