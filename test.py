from subprocess import Popen, PIPE, STDOUT
import time
# This file tests client.py and server.property
# found part of this code on https://stackoverflow.com/questions/3781851/run-a-python-script-from-another-python-script-passing-in-arguments

def main():
    print("Starting testing...")
    cmd = 'client.py'
    p = Popen(['grep', 'f'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    grep_stdout = p.communicate(input=b'one\ntwo\nthree\nfour\nfive\nsix\n')[0]
    print(grep_stdout.decode())

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Shutting down")
    except Exception:
        print("Other exception")
