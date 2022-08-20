# project imports
from queue import PriorityQueue
from src.appSG import appSG
from src.ackn import ackn
from src.request import request

# external imports


class hmiSG():
    
    in_buff_size = 30
    out_butt_size = 30
    app_sg = []
    out_buff = []
    in_buff_entry_count = 1
    curr_req_msg = "input buffer empty"
    curr_req = request(imaginary_request=True)
    in_buff = PriorityQueue()
    
    
    def __init__(self, ans_freq, max_t_ackn) -> None:
        self.ans_freq = ans_freq    # per second
        self.max_t_ackn = max_t_ackn    
    
    
    def addToInBuff(self, message):
        self.in_buff.put((message.getPrio(), self.in_buff_entry_count, message))
        self.in_buff_entry_count += 1
        
        # create acknowledgement
        acknowledgement = ackn(req_id=message.req_id, sg_id=message.sg_id)
        
        # add acknowledgement to output buffer
        self.addToOutBuff(acknowledgement)
    
    def getInMsgNames(self):
        # return list of strings to represent each incoming message (request)
        msg_list = []
        # copy prio queue
        temp_pq = PriorityQueue()
        for i in self.in_buff.queue: temp_pq.put(i)
        # extract msg strings from prio queue
        while not temp_pq.empty():
            msg = temp_pq.get()
            r_temp = msg[2]
            msg_list.append(("request: sg_id_"+str(r_temp.sg_id)+" - req_id_"+str(r_temp.req_id)+" - prio_"+str(r_temp.prio)))
        return msg_list
    
    def getOutMsgNames(self):
        msg_list = []
        for temp in self.out_buff:
            if temp.type == "ackn":
                msg_list.append(("acknowledgement: sg_id_"+str(temp.sg_id)+" - req_id_"+str(temp.req_id)))
            if temp.type == "request":
                msg_list.append(("answer: sg_id_"+str(temp.sg_id)+" - req_id_"+str(temp.req_id)+" - answ_"+str(temp.user_reaction)))
        
        return msg_list
    
    def getCurrReqName(self):
        # return string that represents first message from input buffer (highest priority)
        # extract current message
        if not self.in_buff.empty():
            curr_req = self.in_buff.get()
            r_temp = curr_req[2]
            self.curr_req = r_temp
            self.curr_req_msg = ("request: sg_id_"+str(r_temp.sg_id)+" - req_id_"+str(r_temp.req_id)+" - prio_"+str(r_temp.prio))
        else:
            self.curr_req_msg = "input buffer empty"
        return self.curr_req_msg
    
    
    
    def addToOutBuff(self, message):
        self.out_buff.append(message)
    
    def getNumApp(self):
        return len(self.app_sg)
    
    def getAnsFreq(self):
        return self.ans_freq
    
    def getTAckn(self):
        return self.max_t_ackn