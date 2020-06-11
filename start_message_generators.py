import subprocess, sys

for age in range(1, 5):
    for sex in range(1, 3):
        subprocess.Popen([sys.executable, '/home/website/virtual-person/messages/gen_scripts/gen_resp_age{}_sex{}.py'.format(age, sex)])

subprocess.Popen([sys.executable, '/home/website/virtual-person/messages/sentiment_recognition.py'])
subprocess.Popen([sys.executable, '/home/website/virtual-person/messages/syntax_characteristics.py'])
while True:
    pass

