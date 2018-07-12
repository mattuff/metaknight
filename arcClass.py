class arc:
    def __init__(self,name,knot,succ):
        self.name=name #is this necessary?
        self.knot=knot
        self.succ=succ #succ needs to be an arc already; doesn't work: one of them has to be the first to be defined.
    def set_succ(self,succ):
        self.succ=succ
    def get_succ(self):
        return(self.succ)
    def get_knot(self):
        return(self.knot)

