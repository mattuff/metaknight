class component:

    def __init__(self, handle, framing): #for 1-handles, framing=infinity
        self.handle = handle
        self.framing = framing

    def getHandle(self): #returns type of handle: one or two handle
        return self.handle

    def getFraming(self): #returns framing of 2-handles
        return self.framing

    def changeFraming(self, f): #changes framing of 2-handles
        framing=f
