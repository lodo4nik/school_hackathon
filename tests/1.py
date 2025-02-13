from datetime import datetime

nowTimeStr = str(datetime.now())[:-6]
nowTime = datetime.strptime(nowTimeStr, '%Y-%m-%d %H:%M:%S')
print(nowTimeStr)
