import PySimpleGUI as sg
from src.hmiSG import hmiSG
from src.appSG import appSG




def getQueueList(_q):
    temp = _q
    list = []
    for el in temp:
        list.append(el[1])
    return list


    

def advanceTimeStep():
    # send first n messages from output buffer
    for i in range(out_buff_send_per_time):
        if len(hmi_sg.out_buff) > 0:
            hmi_sg.out_buff.pop()
    
    # iterate Application SG and update input buffer
    for asg in app_sg:
        req = asg.iterate()
        if req.imaginary_request == False:
            hmi_sg.addToInBuff(req)
    
    # update ui display of current request
    if hmi_sg.curr_req_msg == "input buffer empty":
        window["-UI LISTBOX-"].update(["UI Display","currently active request:",hmi_sg.getCurrReqName()])
    
    # update input buffer display
    window["-IN BUFF LISTBOX-"].update(hmi_sg.getInMsgNames())
    
    # update output buffer display
    window["-OUT BUFF LISTBOX-"].update(hmi_sg.getOutMsgNames())


def uiButtonClicked(event):
    # do nothing, if there is no current message
    if hmi_sg.curr_req_msg == "input buffer empty":
        return
    
    # set answer according to which button was pressed
    if event == "-UI BUTTON 1-":
        hmi_sg.curr_req.user_reaction = "B1"
    elif event == "-UI BUTTON 2-":
        hmi_sg.curr_req.user_reaction = "B2"
    elif event == "-UI BUTTON 3-":
        hmi_sg.curr_req.user_reaction = "B3"
    else:
        hmi_sg.curr_req.user_reaction = "unknown"
    
    # place answer to current message in output buffer
    hmi_sg.addToOutBuff(hmi_sg.curr_req)
    window["-OUT BUFF LISTBOX-"].update(hmi_sg.getOutMsgNames())
    
    # get next message from input buffer and place it in ui display
    window["-UI LISTBOX-"].update(["UI Display","currently active request:",hmi_sg.getCurrReqName()])
    # also update input buffer display
    window["-IN BUFF LISTBOX-"].update(hmi_sg.getInMsgNames())




# create global variables
max_t_ackn = 2
n_appSG = 9 # number of Application-SG
timestep_curr = 0
out_buff_send_per_time = 30
f_req = 0.9/n_appSG # average frequency of request (split up over all appSG)
# create SG objects
hmi_sg = hmiSG(ans_freq=1, max_t_ackn=max_t_ackn)
app_sg = [] #list of all Application-SG
for i in range(n_appSG):
    app_sg.append(appSG(t_ackn=max_t_ackn, sg_id=i, f_req=f_req))



# create basic layout
button_advance = sg.Button("Advance HMI-SG Timestep", key="-ADVANCE TIMESTEP-")
text_timestep = sg.Text("current timestep: "+str(timestep_curr), key="-TIMESTEP CURR-")
listbox_ui = sg.Listbox(
    values=["UI Display","currently active request:",hmi_sg.getCurrReqName()], enable_events=True, size=(35,3), key="-UI LISTBOX-"
)
button_ui_1 = sg.Button("UI Button 1", key="-UI BUTTON 1-")
button_ui_2 = sg.Button("UI Button 2", key="-UI BUTTON 2-")
button_ui_3 = sg.Button("UI Button 3", key="-UI BUTTON 3-")
listbox_in_buff = sg.Listbox(
    values=[], enable_events=True, size=(35,15), key="-IN BUFF LISTBOX-"
)
listbox_out_buff = sg.Listbox(
    values=[], enable_events=True, size=(35,15), key="-OUT BUFF LISTBOX-"
)

lay_SG_col = [
    [sg.Text("HMI-SG")],
    #[sg.Text("Answer Frequency = "+str(hmi_sg.getAnsFreq())+" per timestep", key="-ANSWER FREQ-")],
    [listbox_ui],
    [button_ui_1,button_ui_2,button_ui_3],
    [sg.HSeparator()],
    [sg.Text("Application-SG")],
    [sg.Text("number of SG = "+str(len(app_sg)))],
    [sg.Text("request frequency = "+str(f_req)+" per SG and timesteps")],
    [sg.Text("total request frequency = "+str(f_req*n_appSG)+" per timesteps")],
]

lay_inBuff = [
    [sg.Text("Input Buffer (Priority Queue)")],
    [listbox_in_buff],
]

lay_outBuff = [
    [sg.Text("Output Buffer (FIFO, up to "+str(out_buff_send_per_time)+" per timestep)")],
    [listbox_out_buff],
]

layout_proto = [
    [
        button_advance,
        sg.VSeparator(),
        text_timestep
    ],
    [
        sg.HSeparator()
    ],
    [
        sg.Column(lay_SG_col),
        sg.VSeparator(),
        sg.Column(lay_inBuff),
        sg.VSeparator(),
        sg.Column(lay_outBuff),
    ]
]

# create the window
window = sg.Window("Protokoll Demo",layout_proto)


# event loop
while True:
    event, values = window.read()
    # end if user closes window or presses ok button
    if event == sg.WIN_CLOSED:
        break
    elif event == "-ADVANCE TIMESTEP-":
        timestep_curr += 1
        window["-TIMESTEP CURR-"].update("current timestep: "+str(timestep_curr))
        advanceTimeStep()
    elif event == "-UI BUTTON 1-" or event == "-UI BUTTON 2-" or event == "-UI BUTTON 3-":
        uiButtonClicked(event)

# close window
window.close()
