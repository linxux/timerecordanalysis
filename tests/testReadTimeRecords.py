#   testReadTimeRecords.py
#-*- coding: utf-8 -*-
import os
import sys
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


def test_setRecordsFolder():
    records = ReadTimeRecords() 
    
    _method_split_line("setRecordFolder")

    folder = "E:/doc/txt/time_manager/1_diary_日记"
    print "before decode to unicode", folder, repr(folder)
    anotherPath = unicode(os.path.normpath(folder), "utf-8")
    print "after unicode:", anotherPath, repr(anotherPath)

    newFolderPath = records.setRecordsFolder(folder)
    print "get from return gbk value:", newFolderPath, repr(newFolderPath)
    returnFolder = u(newFolderPath, "gbk")
    print returnFolder, repr(returnFolder)
    #print newFolderPath.decode("gbk")

    if not cmp(anotherPath, returnFolder) == 0:
        raise AssertionError
    else:
        _method_split_line("setRecordFolder", True)

def test_getRecordEvent():
    records = ReadTimeRecords()
    
    _method_split_line("getRecordEvent")

    print _block_indent(), "empty argment, pass"
    event = records.getRecordEvent();
    print _block_indent(), "event is", repr(event) 

    _block_split_line()

    print _block_indent(), "empty line:"
    line = " "
    event = records.getRecordEvent(line)
    print _block_indent(), "event is", repr(event) 
    if event is not None:
        raise AssertionError('Error to handle the empty line')
    
    _block_split_line()

    print _block_indent(), "comment line:"
    line = "#|   分类   |    事情    |   所用时间    |   具体时间    |   地点   |   金钱支出"
    uline = u(line, "utf-8")
    print uline
    event = records.getRecordEvent(line)
    print _block_indent(), "event is", repr(event) 
    if event is not None:
        raise AssertionError('Error to handle the comment line')

    test_getRecordEvent_category(records)

    test_getRecordEvent_costTime(records)
    
    _method_split_line("getRecordEvent", True)

def test_getRecordEvent_costTime(records):

    _block_split_line()
    
    print _block_indent(), "invalid line - costTime is None:"
    line = "1(工作), , , N/A, 公司, 0"
    uline = u(line, "utf-8")
    print uline
    event = records.getRecordEvent(line)
    print _block_indent(), "event is", repr(event)
    if event is not None and event['category'] != 0:
        raise AssertionError('Error to handle the invalid line')

    _block_split_line()
    
    print _block_indent(), "invalid line - costTime is not match regx:"
    line = "1(工作), , absccc, N/A, 公司, 0"
    uline = u(line, "utf-8")
    print uline
    event = records.getRecordEvent(line)
    print _block_indent(), "event is", repr(event)
    if event is not None and event['category'] != 0:
        raise AssertionError('Error to handle the invalid line')

    _block_split_line()
    
    print _block_indent(), "valid line - costTime is valid_1:"
    line = "1(工作), , 1h20m, N/A, 公司, 0"
    uline = u(line, "utf-8")
    print uline
    event = records.getRecordEvent(line)
    print _block_indent(), "event is", repr(event)
    if event is not None and event['costTime'] != '1h20m':
        raise AssertionError('Error to handle the invalid line')
   
    _block_split_line()
    
    print _block_indent(), "valid line - costTime is valid_2:"
    line = "1(工作), , 1小时20分, N/A, 公司, 0"
    uline = u(line, "utf-8")
    print uline
    event = records.getRecordEvent(line)
    print _block_indent(), "event is", repr(event)
    if event is not None and event['costTime'] != '1h20m':
        raise AssertionError('Error to handle the invalid line')
    
def test_getRecordEvent_category(records):

    _block_split_line()

    print _block_indent(), "invalid line - category is invalid_1:"
    line = "工作, , 1小时, N/A, 公司, 0"
    uline = u(line, "utf-8")
    print uline
    event = records.getRecordEvent(line)
    print _block_indent(), "event is", repr(event)
    if event is not None and event['category'] != 0:
        raise AssertionError('Error to handle the invalid line')

    _block_split_line()
    
    print _block_indent(), "invalid line - category is invalid_2:"
    line = "12-, , 1小时, N/A, 公司, 0"
    uline = u(line, "utf-8")
    print uline
    event = records.getRecordEvent(line)
    print _block_indent(), "event is", repr(event)
    if event is not None and event['category'] != 0:
        raise AssertionError('Error to handle the invalid line')

    _block_split_line()
    
    print _block_indent(), "valid line - category is valid_1:"
    line = "1, , 1小时, N/A, 公司, 0"
    uline = u(line, "utf-8")
    print uline
    event = records.getRecordEvent(line)
    print _block_indent(), "event is", repr(event)
    if event is not None and event['category'] == 0:
        raise AssertionError('Error to handle the valid line')
    
    _block_split_line()
    
    print _block_indent(), "valid line - category is valid_2:"
    line = "1-2, , 1小时, N/A, 公司, 0"
    uline = u(line, "utf-8")
    print uline
    event = records.getRecordEvent(line)
    print _block_indent(), "event is", repr(event)
    if event is not None and event['category'] == 0:
        raise AssertionError('Error to handle the valid line')

    _block_split_line()
    
    print _block_indent(), "valid line - category is valid_3:"
    line = "2-1(计算机类), , 1小时, N/A, 公司, 0"
    uline = u(line, "utf-8")
    print uline
    event = records.getRecordEvent(line)
    print _block_indent(), "event is", repr(event)
    if event is not None and event['category'] == 0:
        raise AssertionError('Error to handle the valid line')

    _block_split_line()
    
    print _block_indent(), "valid line - category mainCategory value:"
    line = "2(计算机类), , 1小时, N/A, 公司, 0"
    uline = u(line, "utf-8")
    print uline
    event = records.getRecordEvent(line)
    print _block_indent(), "event is", repr(event), type(event['mainCategory'])
    if event is not None and event['mainCategory'] != 2:
        raise AssertionError('Error to handle the valid line')

    _block_split_line()
    
    print _block_indent(), "valid line - category main/subCategory value:"
    line = "2-1(计算机类), , 1小时, N/A, 公司, 0"
    uline = u(line, "utf-8")
    print uline
    event = records.getRecordEvent(line)
    print _block_indent(), "event is", repr(event), type(event['mainCategory'])
    if event is not None and event['mainCategory'] != 2 and event['subCategory'] !=1:
        raise AssertionError('Error to handle the valid line')

def test_calculateCostTimes():
    records = ReadTimeRecords()

    _method_split_line("calculateCostTimes")

    print _block_indent(), "Empty pass"
    result = records.calculateCostTimes()
    print _block_indent(), "the result is:", result
    if result is None:
        raise AssertionError('Error to calcute the costed times')

    _block_split_line()

    print _block_indent(), "Event is None - invalid obj"
    result = records.calculateCostTimes(None)
    print _block_indent(), "the result is:", result
    if result is None:
        raise AssertionError('Error to calculate the costed times')

    _block_split_line()

    evetTxt = "1(工作), , 1小时45分, N/A, 公司, 0"
    print _block_indent(), "Valid event 1 :",
    print u(evetTxt, "utf-8")
    result = records.calculateCostTimes(records.getRecordEvent(evetTxt))
    print _block_indent(), "the result is:", result, result['1'][0]
    if result is None or len(result) == 0 or result['1'][0] != 105:
        raise AssertionError('Error to calculate the costed times')

    _block_split_line()

    evetTxt = "1(工作), 开会, 40分, N/A, 公司, 0"
    print _block_indent(), "Valid event 2 :",
    print u(evetTxt, "utf-8")
    result = records.calculateCostTimes(records.getRecordEvent(evetTxt))
    print _block_indent(), "the result is:", result, result['1'][0]
    if result is None or len(result) == 0 or result['1'][0] != 145:
        raise AssertionError('Error to calculate the costed times')

    _block_split_line()

    evetTxt = "2(学习), , 1小时, N/A, 公司, 0"
    print _block_indent(), "Valid event 3 :",
    print u(evetTxt, "utf-8")
    result = records.calculateCostTimes(records.getRecordEvent(evetTxt))
    print _block_indent(), "the result is:", result, result['2'][0]
    if result is None or len(result) == 0 or result['2'][0] != 60:
        raise AssertionError('Error to calculate the costed times')

    _block_split_line()

    evetTxt = "2-1(计算机类), , 1小时, N/A, 公司, 0"
    print _block_indent(), "Valid event 4 :",
    print u(evetTxt, "utf-8")
    result = records.calculateCostTimes(records.getRecordEvent(evetTxt))
    print _block_indent(), "the result is:", result, result['2'][0]
    if result is None or len(result) == 0 or result['2'][0] != 120 or result['2'][1]['2-1'] != 60:
        raise AssertionError('Error to calculate the costed times')

    _block_split_line()

    evetTxt = "3-1(项目), , 1小时50分, N/A, 公司, 0"
    print _block_indent(), "Valid event 5 :",
    print u(evetTxt, "utf-8")
    result = records.calculateCostTimes(records.getRecordEvent(evetTxt))
    print _block_indent(), "the result is:", result, result['3'][0]
    if result is None or len(result) == 0 or result['3'][0] != 110 or result['3'][1]['3-1'] != 110:
        raise AssertionError('Error to calculate the costed times')

    _method_split_line("calculateCostTimes", True)

if __name__ == '__main__':
    #print sys.path
    try:
        test_setRecordsFolder()
        test_getRecordEvent()
        test_calculateCostTimes()
    except AssertionError as e:
        print "*" * 10, e, "*" * 10
        raise
