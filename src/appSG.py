import random
from src.request import request


class appSG():
    req_id = 0
    def __init__(self, t_ackn, sg_id, f_req) -> None:
        self.t_ackn = t_ackn    # time to wait for acknowledgement before sending again
        self.sg_id = sg_id
        self.f_req = f_req
    
    def iterate(self):
        if self.f_req > random.random():
            # this will be the case (f_req*100)% of the time
            return self.Request()
        else:
            return request(imaginary_request=True)
    
    def Request(self):
        # returns a request which is to be forwarded to the HMI input buffer
        self.req_id += 1
        req = request(req_id=self.req_id, sg_id=self.sg_id)
        return req