#   cmdtmanalysis.py
#-*- encoding: utf-8 -*-

import sys
from timerecordanalysis.readrecords import ReadTimeRecords

def usage():
    print """
    [1] configure the analysis
    [2] analysis time records
    [0] exit
    """
    return raw_input('please select the operation: ')

def analysTimeRecords():
    startDate = ""
    while(len(startDate) == 0):
        startDate = raw_input('input the start date: ').strip()

    endDate = raw_input('input the end date: ').strip()
    print 'caluting the records from [%(start)s] to [%(end)s]' % {'start': startDate, 'end': endDate} 

    workDayStr = raw_input('input working day in a weeek (default is 5): ').strip()
    workDay = 5
    if workDayStr.isdigit():
        workDay = int(workDayStr)

    records = ReadTimeRecords()
    folder = "E:/doc/txt/time_manager/1_diary_日记"
    records.setRecordsFolder(folder)
    cfgFile = "E:/doc/txt/time_manager/category.cfg"
    records.setCfgFile(cfgFile)
    baseDir = "E:/doc/txt/time_manager/2_summarize_总结/tmp"
    
    records.setWorkDays(workDay)
    contents = records.getCalculateContentByTimes(startDate, endDate)
    outputFileName = startDate + "_" + (endDate if len(endDate)>0 else "now") + ".txt"

    records.writeCalculteFile(outputFileName, contents, baseDir) 

if __name__ == '__main__':
    while(True) :
        value = int(usage())
        print 'choose opertion [%(option)s]' % {'option': value}
        if value == 0:
            sys.exit(0)
        elif value == 1:
            pass
        elif value == 2:
            analysTimeRecords()
        else:
            pass


