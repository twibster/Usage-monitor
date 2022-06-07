import time, psutil, monotonic, datetime

mtime=monotonic.time.time
monitorTime = datetime.datetime.now().date()

def getSessionTime():
	upTime =mtime()
	return datetime.timedelta(seconds = upTime-windowsUpTime)

def getNetworkUsage(firstRun=0):
	network = psutil.net_io_counters(pernic=True)
	networkUsage = (network["Wi-Fi"].bytes_recv + network["Wi-Fi"].bytes_sent)//1048576
	return networkUsage-windowsNetwork if not firstRun else networkUsage

windowsUpTime = mtime()
windowsNetwork= getNetworkUsage(1)

def readFile(file):
	try:
		file.seek(0)
		fileSession = file.readline().split(" ")[2].split(":")
		fileSession = datetime.timedelta(hours=int(fileSession[0]),
								minutes=int(fileSession[1]),seconds=int(fileSession[2][1]))
		fileNetwork = int(file.readline().split(":")[1].split(" ")[1].strip())
	except IndexError:
		fileSession = datetime.timedelta()
		fileNetwork=0
		
	return fileSession,fileNetwork

def registerData(date):
	with open(f"{date}.txt",'a+') as file:
		fileSession,fileNetwork = readFile(file)
		lastWrite = datetime.datetime.now()
		while datetime.datetime.now().date() == date:
			time.sleep(1)
			sessionTime=getSessionTime() + fileSession
			try:
				network_usage = getNetworkUsage() + fileNetwork
			except RuntimeError:
				continue

			if (datetime.datetime.now() - lastWrite).total_seconds() >62:
				windowsUpTime = mtime()
				fileSession,_ = readFile(file)
			else:
				file.truncate(0)
				file.seek(0)	
				file.write("Session Time: %s \nNetwork Usage: %s Mb\n" % (sessionTime,network_usage))
				file.flush()
			lastWrite = datetime.datetime.now()
		else:
			monitorTime=datetime.datetime.now().date()
			registerData(monitorTime)

registerData(monitorTime)