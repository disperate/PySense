import pySenseLogger, random, time

def logDataSets(count):
    messurmentLeft = 2.5
    messurmentRight = 2.5
    for x in range(0, count):

        messurmentLeft += getRandomChange()
        messurmentRight += getRandomChange()

        pySenseLogger.logUltraSonic("SensorLeft", messurmentLeft)
        pySenseLogger.logUltraSonic("SensorRight", messurmentRight)

        if x % 10 == 0:
            pySenseLogger.logNotice("LoggerTest", "Sent 10 logs")

        

def getRandomChange():
    return random.random() - 0.5

logDataSets(100)