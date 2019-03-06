from subprocess import call
import sys
import time

proxies=[('12.164.246.247:35000','hype9049143:pwd994143'),
         ('12.164.246.95:35000', 'hype904926:pwd99426'),
         ('12.164.246.227:35000', 'hype9049123:pwd994123'),
         ('12.164.246.159:35000', 'hype904975:pwd99475'),
         ('12.164.246.235:35000', 'hype9049131:pwd994131'),
         ('12.164.246.85:35000', 'hype904916:pwd99416'),
         ('12.164.246.219:35000', 'hype9049115:pwd994115'),
         ('12.164.246.224:35000', 'hype9049120:pwd994120'),
         ('12.164.246.116:35000', 'hype904947:pwd99447'),
         ('12.164.246.204:35000', 'hype9049100:pwd994100'),
         ('12.164.246.100:35000', 'hype904931:pwd99431'),
         ('12.164.246.246:35000', 'hype9049142:pwd994142'),
         ('12.164.246.140:35000', 'hype904970:pwd99470'),
         ('12.164.246.245:35000', 'hype9049141:pwd994141'),
         ('12.164.246.167:35000', 'hype904983:pwd99483'),
         ('12.164.246.226:35000', 'hype9049122:pwd994122')]

thread_num = 0
for ip_port, auth in proxies:
    region = 3
    # ip_port = '12.164.246.247:35000'
    # auth = 'hype9049143:pwd994143'
    thread_num+=1
    path = 'D:\Codes\Bokx\SNKRSMonitor\logs'
    cmd = 'start cmd /c python snkrs.py %s %s %s ^> %s\log%s.txt' % (region, ip_port, auth, path, thread_num)
    call(cmd, shell=True)
    time.sleep(1)

# path = 'D:\Codes\Bokx\SNKRSMonitor\logs'
# path = sys.argv[1]
# cmd1 = 'start cmd /c python snkrs.py %s %s %s ^> %s\log%s.txt' % (1, '12.164.246.247:35000', 'hype9049143:pwd994143', path, 1)
# cmd2 = 'start cmd /c python snkrs.py %s ^> %s\log%s.txt' % (1,  path, 2)
# call(cmd1, shell=True)
# call(cmd2, shell=True)
# print('all commands ran')