class component:

    def __init__(self, handle, framing, orientation):
        self.handle = handle
        self.framing = framing
        self.orientation = orientation

    def getHandle(self):
        return self.handle

    def getFraming(self):
        return self.framing
    
    def getOrientation(self):
        return self.orientation

    def changeFraming(self, f):
        framing=f
