#   testCalculateResult.py
#-*- encoding: utf-8 -*-
from timerecordanalysis.readrecords import ReadTimeRecords

def u(str, encoding):
    if isinstance(str, unicode):
        return str
    else:
        return unicode(str, encoding)

def _method_split_line(methodName, flag=False):
    if flag:
        print "-" * 10, methodName, "-" * 10, "success"
    else:
        print "-" * 10, methodName, "-" * 10
def _block_split_line():
    print _block_indent(), "=" * 20
def _block_indent():
    return " " * 4

def test_calculteFileEvent():
    _method_split_line("calculteFileEvent")
    # init args
    records = ReadTimeRecords()
    folder = "E:/doc/txt/time_manager/1_diary_日记"
    records.setRecordsFolder(folder)
    # get the first file in folder
    print "read the first file", ">" * 20, records.files[0]
    records.calculteFileEvent(records.files[0])
    print "the calculate result >>", records.resultDict 

    _block_split_line()

    print "Error file Name: 0000.txt"
    records.calculteFileEvent("0000.txt")
    print "the Error file Name, result >>", records.resultDict

    _block_split_line()
    # get the second file in folder
    print "read the second file", ">" * 20, records.files[1]
    records.calculteFileEvent(records.files[1])
    print "the calculate result >>", records.resultDict

    _method_split_line("calculteFileEvent", True)

def test_writeCalculateFile():
    
    _method_split_line("writeCalculateFile")
    # init args
    records = ReadTimeRecords()
    folder = "E:/doc/txt/time_manager/1_diary_日记"
    records.setRecordsFolder(folder)

    baseDir = "E:/doc/txt/time_manager/2_summarize_总结"
    resultFile = "testResult.txt"
    records.writeCalculteFile(resultFile, None, baseDir)

    _method_split_line("writeCalculateFile", True)

def test_getCalculateContentByTimes():
    _method_split_line("getCalculateContentByTimes")

    # init args
    records = ReadTimeRecords()
    folder = "E:/doc/txt/time_manager/1_diary_日记"
    records.setRecordsFolder(folder)
    cfgFile = "E:/doc/txt/time_manager/category.cfg"
    records.setCfgFile(cfgFile)

    baseDir = "E:/doc/txt/time_manager/2_summarize_总结/tmp"

    startDate = '20110627'
    endDate = '20110702'
    contents = records.getCalculateContentByTimes(startDate, endDate)
    resultFile = startDate + "_" + endDate + ".txt"
    records.writeCalculteFile(resultFile, contents, baseDir)

    _method_split_line("getCalculateContentByTimes", True)

if __name__ == '__main__':
    try:
       test_calculteFileEvent() 
       #test_writeCalculateFile()
       test_getCalculateContentByTimes()
    except AssertionError as e:
        print "*" * 10, e, "*" * 10
        raise
