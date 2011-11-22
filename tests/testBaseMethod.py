# testBaseMethod.py
#-*- coding: utf-8 -*-
import decimal

def test_float():
    a = 10080
    b = 3360

    print "3/10 = %(value).2f" % {"value": b/a}
    print "3/10 = %(value).2f" % {"value": (b*1.0)/(a*1.0)}
    print "3/10 = %(value).2f%%" % {"value": (b*100*1.0)/(a*1.0)}
    print "3/10 = %(value).2f" % {"value": decimal.Decimal(b)/decimal.Decimal(a)}

if __name__ == '__main__':
    test_float()
