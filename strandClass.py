class strand:
    
    def __init__(self,component,succ=None,pred=None):
        self.component=component
        self.succ=succ
        self.pred=pred
        
    def set_succ(self,succ):
        self.succ=succ
        
    def get_succ(self):
        return(self.succ)
        
    def set_pred(self,pred):
        self.pred=pred
        
    def get_pred(self):
        return(self.pred)
    
    def get_component(self):
        return(self.component)
    
    def set_component(self):
        return(self.component)
