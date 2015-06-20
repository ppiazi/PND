# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 15:53:11 2015

@author: ppiazi
"""

from PNDHandler import PNDHandler
from SCurveHandler import SCurveHandler

import xlwt

class PNDDataWriter:
    def __init__(self, file_name, pnd_data, scurve_data):
        self._wbk = xlwt.Workbook()
        self._file_name = file_name
        self._pnd_data = pnd_data
        self._pnd_data_dict = pnd_data.getPNDDataDict()
        self._scurve_data = scurve_data
        self._scurve_data_es = scurve_data.getScurveDataEs();
        self._scurve_data_lf = scurve_data.getScurveDataLf();
        
        self.initPNDDataHeading()
        self.initSCurveDataHeading()
    
    def initPNDDataHeading(self):        
        self._sheet1 = self._wbk.add_sheet("PND Data", cell_overwrite_ok=True)
        self._sheet1.write(0, 0, "Task Name")
        self._sheet1.write(0, 1, "Duration")
        self._sheet1.write(0, 2, "ES")
        self._sheet1.write(0, 3, "EF")
        self._sheet1.write(0, 4, "LS")
        self._sheet1.write(0, 5, "LF")
        self._sheet1.write(0, 6, "TF")
        self._sheet1.write(0, 7, "Cost")
        self._sheet1.write(0, 8, "Human Resource")
        
    def initSCurveDataHeading(self):
        self._sheet2 = self._wbk.add_sheet("SCurve Data", cell_overwrite_ok=True)
        self._start_day = self._scurve_data.getStartDay()
        self._end_day = self._scurve_data.getEndDay()

        self._sheet2.write(0,0, "Task Name")
        self._sheet2.write(0,1, "Type(ES/LF)")
        
        x = 2
        for i in range(self._start_day, self._end_day + 1):
            self._sheet2.write(0, x, i)
            x = x + 1        
        
    def writePNDData(self):
        row = 1
        for key in self._pnd_data_dict.keys():
            task_info = self._pnd_data_dict[key]
            self._sheet1.write(row, 0, task_info.getName())
            self._sheet1.write(row, 1, task_info.getDuration())
            self._sheet1.write(row, 2, task_info.getEs())
            self._sheet1.write(row, 3, task_info.getEf())
            self._sheet1.write(row, 4, task_info.getLs())
            self._sheet1.write(row, 5, task_info.getLf())
            self._sheet1.write(row, 6, task_info.getTf())
            self._sheet1.write(row, 7, task_info.getCost())
            self._sheet1.write(row, 8, task_info.getHs())
            row = row + 1

    def writeSCurveData(self):
        row = 1
        
        for key in self._scurve_data_es.keys():
            col = 1
            task_scurve_es = self._scurve_data_es[key]
            
            self._sheet2.write(row, 0, key)
            self._sheet2.write(row, col, "es")
            
            for i in range(self._start_day, self._end_day + 1):
                self._sheet2.write(row, col + i, task_scurve_es[i])
            
            row = row + 1
      
        for key in self._scurve_data_lf.keys():
            col = 1
            task_scurve_lf = self._scurve_data_lf[key]
            
            self._sheet2.write(row, 0, key)
            self._sheet2.write(row, col, "lf")
            for i in range(self._start_day, self._end_day + 1):
                self._sheet2.write(row, col + i, task_scurve_lf[i])
            
            row = row + 1
    
    def writeData(self):
        self.writePNDData()
        self.writeSCurveData()
        self._wbk.save(self._file_name)                
    
