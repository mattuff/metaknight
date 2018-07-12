class component:

    def __init__(self, handle, framing):
        self.handle = handle
        self.framing = framing

    def gethandle(self):
        return self.handle

    def getframing(self):
        return self.framing

    def changeframing(self, f):
        framing=f
