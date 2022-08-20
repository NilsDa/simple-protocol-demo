from random import randrange

class request():
    prio: int
    type = "request"
    user_reaction = ""
    def __init__(self, req_id=-1, sg_id=-1, stamp=0, imaginary_request=False) -> None:
        self.prio = randrange(10)
        self.stamp = stamp
        self.req_id = req_id
        self.sg_id = sg_id
        self.imaginary_request = imaginary_request
    
    def getPrio(self):
        return self.prio