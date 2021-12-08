import subprocess
import sys
import time

bDebug=False

if __name__ == '__main__':
    snooperCmdString = "sudo python3 snooper.py".split()
    
    if bDebug==False:
        subprocessOut = subprocess.PIPE
    else:
        subprocessOut = sys.stdout

    p =subprocess.Popen(snooperCmdString, stdin=subprocess.PIPE, stdout=subprocessOut, stderr=subprocess.PIPE)
    p.stdin.write(' '.encode('utf-8'))
    p.stdin.flush()

    bScreenCapture = False
    screenCaptureTimer = 0

    screenshotIdx = 0
    if bDebug == False:
        while(True):
            msg = str(p.stdout.readline(), 'utf-8')
            if msg == '' and p.poll() is not None:
                print('Exit')
                break
            if msg:
                print(msg.strip())
            if msg.find('pattern detected') != -1:
                bScreenCapture = True
                screenCaptureTimer = time.time()
            if bScreenCapture == True and msg.find('Left') != -1:
                print('Capture!')
                filename = "screenshot_" + str(screenshotIdx) + ".jpg"
                screenshotIdx += 1
                #you should use your screen capture application here
                subprocess.Popen(["/home/arcs/gnome-screenshot/_build/src/gnome-screenshot", "-p", "-f", filename])
                #subprocess.Popen(["gnome-screenshot", "-p", "-f", filename])
            if bScreenCapture == True:
                elapsed = time.time() - screenCaptureTimer
                if elapsed > 60 * 5:
                    bScreenCapture = False

    p.wait()
