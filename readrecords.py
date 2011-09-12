# ReadTimeRecords.py
#-*- coding: utf-8 -*-
import os
import logging
import codecs
import sys
import re
from datetime import datetime, date, timedelta 
import ConfigParser

def uStr(str, encoding="utf-8"):
    if isinstance(str, unicode):
        return str
    else:
        return unicode(str, encoding)

class MyLogger:
    def __init__(self, loggerName):
        self.data = []
        logger = logging.getLogger(loggerName)
        logger.setLevel(logging.DEBUG)

        cHandler = logging.StreamHandler()
        cHandler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        cHandler.setFormatter(formatter)

        logger.addHandler(cHandler)

        self.log = logger
    def warn(self, msg):
        self.log.warn(msg)
    def info(self, msg):
        self.log.info(msg)
    def debug(self, msg):
        self.log.debug(msg)
    def error(self, msg):
        self.log.error(msg)

class ReadTimeRecords:
    logger = MyLogger("Read_Time_Records_core")
    def __init__(self):
        self.data = []
        self.files = []
        self._invalidEvent = {"category" : 0}
        self.resultDict = {}
        self.cfg = None
    def setRecordsFolder(self, folderPath):
        """ Set the folder and change the working directory to the assigned folder """
        path = unicode(folderPath, "utf-8")
        #self.logger.debug("the records folder is: "+ path)
        # get the list in diretory
        if os.path.isdir(path):
            self.files = os.listdir(path)
            #for file in self.files[:]:
                #self.logger.debug(file)
            # change the work
            os.chdir(path)
            workingFolder = os.getcwd()
            self.logger.debug("current working directory:"+workingFolder)
            return workingFolder

    def calculteFileEvent(self, fileName):
        """ Calculte a file content """
        self.readRecordFile(fileName, 1)

    def readRecordFile(self, fileName, rule=None):
        """ Read the file line and line """
        self.logger.debug("read the file:"+fileName)
        if os.path.exists(fileName) is False:
            self.logger.error("the file:"+fileName+" is not exists.")
            return
        with open(fileName) as f:
            for line in f:
                lineText = unicode(line, "utf-8")
                #self.logger.debug(lineText)
                if rule is not None and rule == 1:
                    self.calculateCostTimes(self.getRecordEvent(lineText))

    def getRecordEvent(self, lineText=None):
        """ 
        Analysis the line string: 
            filter the comment line and empty line;
            return a event obj or None
        """
        # None argument
        if lineText is None:
            return

        lineText = lineText.strip()
        # empty string
        if len(lineText) == 0:
            return
        # change the encoding
        lineText = uStr(lineText)
        # filter th comment symbol
        if lineText[0] in ['#', '/']:
            return

        event = {"category" : -1}
        items = lineText.split(",")
        length = len(items)
        #patternRegx = r"(?P<category>\d+\-\d+|\d+^\-)"
        patternRegx = r"^(\d+\-\d+|\d+)$"
        categoryPattern = r"(?P<mainCategory>\d+)\-?(?P<subCategory>\d+)?"
        costTimePattern = r"^(\d{1,2}h|\d{1,2}m|\d{1,2}h\d{1,2}m)$"
        timeSymboDict = { u"小时" : "h", u"分" : "m", u"分钟" : "m"}
        for index in range(length):
            items[index] = items[index].strip()
            #self.logger.debug(str(index)+": "+items[index])
            if index == 0:
                category = items[index]
                # category is not set
                if len(category) == 0:
                    return self._invalidEvent
                
                spePos = category.find("(")
                #self.logger.debug("find the end pos:"+str(spePos))
                if spePos != -1:
                    category = category[:spePos]
                    #self.logger.debug("the actural value: "+category)

                m = re.match(patternRegx, category)
                #print "the regx result:", m
                if m is None:
                    self.logger.error("the category: %(category)s is not match regx" % {"category": uStr(category)})
                    return self._invalidEvent

                # set the category value, reset the string to default encoding 
                event['category'] = category.encode()

                m = re.match(categoryPattern, category)
                #print m.groupdict()
                mCategory = m.group('mainCategory') 
                sCategory = m.group('subCategory') 
                #self.logger.debug("mainCategory is:"+str(mCategory)+" subCategory is:"+str(sCategory))
                event['mainCategory'] = int(mCategory)
                event['subCategory'] = int(sCategory) if sCategory is not None else None

            elif index == 1:
                desc = items[index]
                event['desc'] = desc 
            elif index == 2:
                costTime = items[index]
                if len(costTime) == 0:
                    return self._invalidEvent 

                # replace the symbols, get a uniform format as: 10h20m
                for key, value in timeSymboDict.iteritems():
                    costTime = costTime.replace(key, value)

                m = re.match(costTimePattern, costTime)
                
                if m is None:
                    self.logger.error("the costTime is not match regx")
                    return self._invalidEvent

                event['costTime'] = costTime 
            elif index ==3:
                timeScope = items[index]
                event['timeScope'] = timeScope 
            elif index ==4:
                spot = items[index]
                event['spot'] = spot 
            elif index == 5:
                costMoney = items[index]
                event['costMoney'] = costMoney 

        return event
    def calculateCostTimes(self, event=None):
        """ calcute the cost time according events 
            return a dict with a tuple as value,
            e.g., {'1': <300, {'1-1': 20, '1-2': 250}>}
            -'1' as the main category,
            -300 as the total costed time,
            -'1-1' as the sub category1,
            -20 as the costed time of the sub category1
        """

        #self.logger.debug("current event is:"+repr(event))
        if event is None or event['category'] == 0:
            return self.resultDict 

        # operation dict
        calculatorDict = {'h': ' * 60 + ', 'm': ' + '}
        timeValueStr = event['costTime']
        for key, value in calculatorDict.iteritems():
            timeValueStr = timeValueStr.replace(key, value)
        # use eval method
        timeValue = eval(timeValueStr + "0")
        #self.logger.debug("timeValue is: "+str(timeValue))

        mainCategoryKey = str(event['mainCategory'])
        subCategoryKey = event['subCategory']
        categoryKey = event['category']
        #print categoryKey, repr(categoryKey), repr(categoryKey.encode())
        if mainCategoryKey in self.resultDict:
            # get the origin value
            totalCosted, subDict = self.resultDict[mainCategoryKey]
            # set the sub category value
            if subCategoryKey is not None:
                if categoryKey in subDict:
                    subDict[categoryKey] = subDict[categoryKey] + timeValue
                else:
                    subDict[categoryKey] = timeValue
            # set the main category value
            self.resultDict[mainCategoryKey] = totalCosted + timeValue, subDict
            return self.resultDict
        else:
            subDict = {}
            if subCategoryKey is not None:
                subDict[categoryKey] = timeValue
            self.resultDict[mainCategoryKey] = timeValue, subDict 
            return self.resultDict 

        return None

    def writeCalculteFile(self, fileName, lines=None, baseName=None):
        """ write the contents to specific file """
        if lines is None or len(lines) == 0:
            lines = []
            #lines.append(uStr("创建时间(GenerateTime): "))
            lines.append("GenerateTime: ")
            lines.append(datetime.today().isoformat(' '))
            lines.append("\n")
            lines.append("*" * 50 + "\n")
            lines.append("Please set the contents.")
        if baseName is not None:
            fileName = os.path.normpath(os.path.join(baseName, fileName))
        fileName = unicode(fileName, "utf-8")
        #print fileName
        with codecs.open(fileName, "w", "utf-8") as f:
            f.writelines(lines)

    def getCalculateContentByTimes(self, startDate, endDate=None):
        """ 
        read the files according the date scope 
        and return the calculate contents
        """
        self.logger.debug("Calculate time scope is %(startDate) -- %(endDate)" % {"startDate": startDate, "endDate": endDate})
        startDate = self._getStartDate(startDate, endDate)
        if startDate is None:
            return

        if startDate.isdigit():

            startD = self._getDatefromStr(startDate)
            endD = self._getDatefromStr(endDate) if endDate is not None else None
            self.calculteFileEvent(startDate + ".txt")

            nextD = startD + timedelta(days=1)

            if endD is not None and startD < endD:
                while nextD <= endD:
                    nextDate = nextD.strftime("%Y%m%d")
                    if os.path.exists(nextDate + ".txt"):
                        self.calculteFileEvent(nextDate + ".txt")
                    nextD = nextD + timedelta(days=1)

            #print self.resultDict
            return self._getSummuarizeFromCalculteResult(startD, endD)
        else:
            msg = "The file \'{0}.txt\' is not invalid name format."
            self.logger.error(msg)
            return msg

    def _getStartDate(self, startDate, endDate=None):
        """
        get the start date, if not exist the specific start date, 
        get the next date that does not exceed the end date.
        """
        if startDate is None:
            return None

        if os.path.exists(startDate + ".txt") is False:
            msg = "The file \'{0}.txt\' is no exists.".format(startDate)
            self.logger.error(msg)
            if endDate is None:
                return None
            else:
                if startDate.isdigit() and endDate.isdigit():
                    startD = self._getDatefromStr(startDate)
                    endD = self._getDatefromStr(endDate)
                    if startD is None or endD is None:
                        msg = "The files %(startfname) or %(endfname) are invalid format." % {"startfname": startDate, "endfname": endDate}
                        self.logger.error(msg)
                        return None
                    else:
                        nextD = startD + timedelta(days=1)
                        if nextD <= endD:
                            return self._getStartDate(nextD.strftime("%Y%m%d"), endDate)
                        else:
                            msg = "The start date should be before the end date: %(startfname) ~ %(endfname)" % {"startfname": startDate, "endfname": endDate}
                            self.logger.error(msg)
                            return None
                else:
                    msg = "The files %(startfname) or %(endfname) are invalid format." % {"startfname": startDate, "endfname": endDate}
                    self.logger.error(msg)
                    return None
        else:
            return startDate

    def _getDatefromStr(self, dateStr):
        if dateStr.isdigit():
            year = int(dateStr[:4])
            month = int(dateStr[4:6])
            day = int(dateStr[6:])
            return date(year, month, day)
        else:
            return

    def _getSummuarizeFromCalculteResult(self, startD, endD):
        if len(self.resultDict) == 0:
            return
        else:
            lines = []
            sublines = []
            blockline = "*" * 80 + "\n"
            #lines.append(uStr("创建时间(GenerateTime): "))
            lines.append("GenerateTime: %(gentime)s\n" % {"gentime": datetime.today().isoformat(' ')})
            lines.append(blockline)
            lines.append("Calculte Times: ")
            lines.append(startD.isoformat())
            days = 0
            if endD is not None and startD < endD:
                lines.append(" ~ ")
                lines.append(endD.isoformat())
                days = (endD - startD).days
            lines.append("\n")
            thours = (days + 1) * 24
            tminutes = thours * 60
            lines.append("Total Reality Hours: %(hours)dh (%(minutes)dm)\n" % {"hours": thours, "minutes": tminutes})
            lines.append(blockline)
            lines.append("Category Recorded Hours:\n\n")
            for key, value in self.resultDict.iteritems():
                lines.append("\t %(mCategory)s: %(costHours)s (%(costTime)dm), (ratio)%(ratio).2f%%\n\n" % {"mCategory": self._getCategoryDesc("Category", key), "costHours": self._getCostedHoursStr(value[0]), "costTime": value[0], "ratio": value[0] * 100 / tminutes})

                if len(value[1]) != 0:
                    uncategorytimes = value[0]
                    for subkey, subvalue in value[1].iteritems():
                        sublines.append("== Category %(category)s ==\n" % {"category": key})
                        subkey = self._getCategoryDesc("Category" + key, subkey)
                        sublines.append(self._getSubCategoryLine(subkey, subvalue, value[0]))
                        uncategorytimes = uncategorytimes - subvalue

                    if uncategorytimes != 0:
                        subkey = self._getCategoryDesc("Category" + key, key + "-00")
                        sublines.append(self._getSubCategoryLine(subkey, uncategorytimes, value[0]))

                    sublines.append("\n")

            if len(sublines) != 0:
                lines.append("-" * 80 + "\n")
                lines.append("SubCategory Recorded Hours:\n\n")
                lines = lines + sublines

            return lines

    def _getSubCategoryLine(self, subCategory, subCostedTimes, costedTimes):
        subhourstr = self._getCostedHoursStr(subCostedTimes) 
        return "\t %(subCategory)s: %(sHoursstr)s (%(sMinutes)dm), (radio)%(sRatio).2f%%\n" % {"subCategory": subCategory, "sHoursstr": subhourstr, "sMinutes": subCostedTimes, "sRatio": subCostedTimes * 100 / costedTimes}

    def _getCostedHoursStr(self, costedTimes):
        sHour = costedTimes/60
        sMin = costedTimes%60
        hourstr = ("" if sHour == 0 else str(sHour) + "h") + ("" if sMin == 0 else str(sMin) + "m")
        return hourstr

    def setCfgFile(self, filePath):
        if os.path.exists(filePath) is False:
            self.logger.error("the cfg file:"+filePath+" is not exists.")
            return
        self.cfg = ConfigParser.RawConfigParser()
        self.cfg.read(filePath)

    def _getCategoryDesc(self, section, key):
        #self.logger.debug("get category desc: section=" + section + " key=" + key)
        if self.cfg is None:
            self.logger.debug("cfg is None")
            return key
        else :
            return key + uStr("(" + self.cfg.get(section, key) + ")")

if  __name__ == '__main__':
    logger = MyLogger("Read_Time_Records_main")

    logger.debug("current encoding is:"+sys.getdefaultencoding())
    logger.debug("current file sys encoding is:"+sys.getfilesystemencoding())

    #a = u"中文中文"
    #au = u"\u4e2d"
    #print a, repr(a), au, repr(au)
    #b = "测试"
    #print b.__class__
    #print repr(b), unicode(b, "utf-8")
    #print b.__class__


    records = ReadTimeRecords()
    folder = "E:/doc/txt/time_manager/1_diary_日记"
    #logger.debug("representation is:"+repr(b))
    records.setRecordsFolder(folder)
    records.readRecordFile(records.files[0])
