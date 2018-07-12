class arc:
    def __init__(self,name,knot,succ):
        self.name=name
        self.knot=knot
        self.succ=succ
    def set_succ(self,succ):
        self.succ=succ
    def get_succ(self):
        return(self.succ)
    def get_knot(self):
        return(self.knot)

