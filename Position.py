class Position:
    def __init__(self,row,column):
        self.row=row
        self.column=column
    
    @property
    def Row(self):
        return self.row
    
    
    @property
    def Column(self):
        return self.column