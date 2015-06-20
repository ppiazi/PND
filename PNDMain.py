# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 16:44:25 2015

@author: ppiazi
"""

from PND import PND
from SCurve import SCurve
from PNDDataWriter import PNDDataWriter

if __name__ == "__main__":
    # 정보 파일을 읽어 PND 데이터를 만든다.
    pnd = PND("data2.csv")
    pnd.analyze()
    
    # 만들어진 PND 데이터를 SCurve에 전달하여 분석한다.
    scurve = SCurve(pnd.getPNDDataDict())
    
    scurve.analyzeScurveWithEs()
    scurve.analyzeScurveWithLf()
    
    # PND 데이터와 SCurve 데이터를 기반으로 엑셀을 만든다.
    writer = PNDDataWriter("result.xls", pnd, scurve)
    writer.writeData()