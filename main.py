import subprocess
import sys

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

    screenshotIdx = 0
    if bDebug == False:
        while(True):
            msg = str(p.stdout.readline(), 'utf-8')
            if msg == '' and p.poll() is not None:
                break
            if msg:
                print(msg.strip())
            if msg.find('Left') != -1:
                filename = "screenshot_" + str(screenshotIdx) + ".jpg"
                screenshotIdx += 1
                subprocess.Popen(["/home/arcs/gnome-screenshot/_build/src/gnome-screenshot", "-p", "-f", filename])
    p.wait()
        