# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 16:44:25 2015

@author: ppiazi
"""

import os
import sys
from PNDHandler import PNDHandler
from SCurveHandler import SCurveHandler
from PNDDataWriter import PNDDataWriter
import matplotlib.pyplot as plt
import collections


def drawPlot(pnd, scurve):
    x_axis = range(scurve.getStartDay(), scurve.getEndDay() + 1)
    ori_dict = scurve.getScurveDataEsAccTotal()

    ordered_dict = collections.OrderedDict(sorted(ori_dict.items()))
    y_axis_1 = list(ordered_dict.values())

    ori_dict_2 = scurve.getScurveDataLfAccTotal()

    ordered_dict_2 = collections.OrderedDict(sorted(ori_dict_2.items()))
    y_axis_2 = list(ordered_dict_2.values())

    plt.plot(x_axis, y_axis_1, x_axis, y_axis_2)
    plt.show()

def print_usage():
    print("PNDMain.exe [csv file]")
    print("  ex) PNDMain.exe data2.csv")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print_usage()
        os._exit(1)

    input_csv_file = sys.argv[1]
    input_file_name = input_csv_file[0:input_csv_file.rindex('.')]

    # 정보 파일을 읽어 PND 데이터를 만든다.
    pnd = PNDHandler(input_csv_file)
    ret = pnd.analyze()

    if ret == False:
        os._exit(1)
    
    # 만들어진 PND 데이터를 SCurve에 전달하여 분석한다.
    scurve = SCurveHandler(pnd.getPNDDataDict())
    
    scurve.analyzeScurveWithEs()
    scurve.analyzeScurveWithLf()
    
    # PND 데이터와 SCurve 데이터를 기반으로 엑셀을 만든다.
    writer = PNDDataWriter(input_file_name + ".xls", pnd, scurve)
    writer.writeData()

    drawPlot(pnd, scurve)