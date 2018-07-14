class component:

    def __init__(self, handle, framing=None): #for 1-handles, framing=infinity
        self.handle = handle
        self.framing = framing

    def get_handle(self): #returns type of handle: one or two handle
        return self.handle

    def get_framing(self): #returns framing of 2-handles
        return self.framing

    def change_framing(self, f): #changes framing of 2-handles
        framing=f
