from bcc import BPF
import ctypes as ct

keyCodeList = {}

def initKeyCodeList():
    keyCodeList[2] = '1'
    keyCodeList[3] = '2'
    keyCodeList[4] = '3'
    keyCodeList[5] = '4'
    keyCodeList[6] = '5'
    keyCodeList[7] = '6'
    keyCodeList[8] = '7'
    keyCodeList[9] = '8'
    keyCodeList[10] = '9'
    keyCodeList[14] = 'Backspace'
    keyCodeList[16] = 'q'
    keyCodeList[17] = 'w'
    keyCodeList[18] = 'e'
    keyCodeList[19] = 'r'
    keyCodeList[20] = 't'
    keyCodeList[21] = 'y'
    keyCodeList[22] = 'u'
    keyCodeList[23] = 'i'
    keyCodeList[24] = 'o'
    keyCodeList[25] = 'p'
    keyCodeList[26] = '['
    keyCodeList[27] = ']'
    keyCodeList[30] = 'a'
    keyCodeList[31] = 's'
    keyCodeList[32] = 'd'
    keyCodeList[33] = 'f'
    keyCodeList[34] = 'g'
    keyCodeList[35] = 'h'
    keyCodeList[36] = 'j'
    keyCodeList[37] = 'k'
    keyCodeList[38] = 'l'
    keyCodeList[39] = ';'
    keyCodeList[40] = '\''
    keyCodeList[41] = '`'
    keyCodeList[44] = 'z'
    keyCodeList[45] = 'x'
    keyCodeList[46] = 'c'
    keyCodeList[47] = 'v'
    keyCodeList[48] = 'b'
    keyCodeList[49] = 'n'
    keyCodeList[50] = 'm'
    keyCodeList[51] = ','
    keyCodeList[52] = '.'
    keyCodeList[53] = '/'
    keyCodeList[57] = 'Space'

    keyCodeList[29] = 'Ctrl'
    keyCodeList[42] = 'Shift'
    keyCodeList[54] = 'Shift'

    keyCodeList[272] = 'Bluetooth Mouse Left Button'
    keyCodeList[273] = 'Bluetooth Mouse Right Button'

def initBpfArray(keyboardSnooper, mouseClickSnooper):
    keyboardInputLog = keyboardSnooper.get_table("keyboardInputLog")
    for entry in keyboardInputLog:
        entry = ct.c_uint(0)
    mouseClickLog = mouseClickSnooper.get_table("mouseClickLog")
    for entry in mouseClickLog:
        entry = ct.c_uint(0)

    return (keyboardInputLog, mouseClickLog)

def getKeyInput(log):
    if log[0].value == 0:
        # No Input
        return None

    retval = log[1].value
    log[0] = ct.c_uint(0)

    return retval

def processKeyboardInput(keyInput):
    # keyboard input comes twice per one press.
    # So it counts each press and raises only when the count is even.
    if (keyInput in processKeyboardInput.counter) == False:
        processKeyboardInput.counter[keyInput] = 1
    else:
        processKeyboardInput.counter[keyInput] += 1
        if (processKeyboardInput.counter[keyInput] % 2) == 0:
            if keyInput in keyCodeList:
                print(keyCodeList[keyInput], flush=True)
            else:
                print(keyInput, flush=True)

processKeyboardInput.counter = {}

def processMouseClick(mouseClick):
    if mouseClick == 9:
        print("Mouse Left Button", flush=True)
    elif mouseClick == 10:
        print("Mouse Right Button", flush=True)

if __name__ == '__main__':
    initKeyCodeList()

    keyboardSnooper = BPF(src_file="keyboardSnooper.c")
    keyboardSnooper.attach_kprobe(
        event="kbd_keycode", fn_name="on_keyboardInput")

    mouseClickSnooper = BPF(src_file="mouseClickSnooper.c")
    mouseClickSnooper.attach_kprobe(
        event="psmouse_process_byte", fn_name="on_mouseClick")

    (keyboardInputLog, mouseClickLog) = initBpfArray(
        keyboardSnooper, mouseClickSnooper)

    print("Start snooping", flush=True)

    while 1:
        keyInput = getKeyInput(keyboardInputLog)
        if keyInput != None:
            processKeyboardInput(keyInput)
        mouseClick = getKeyInput(mouseClickLog)
        if mouseClick != None:
            processMouseClick(mouseClick)
