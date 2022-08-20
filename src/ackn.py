from random import randrange

class ackn():
    
    type = "ackn"
    
    def __init__(self, stamp=0, req_id=-1, sg_id=-1) -> None:
        self.stamp = stamp
        self.req_id = req_id
        self.sg_id = sg_id