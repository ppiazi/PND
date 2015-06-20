# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 12:53:27 2015

@author: ppiazi
"""

from PNDHandler import PNDHandler
import collections

class SCurveHandler:
    def __init__(self, pnd_data_dict):
        self._pnd_data_dict = pnd_data_dict
        self._start_day = -1
        self._end_day = -1
        self._scurve_es = {}
        self._scurve_lf = {}
        self._scurve_es_total = {}
        self._scurve_lf_total = {}

        self.initData()        

    def getScurveDataEs(self):
        return self._scurve_es

    def getScurveDataLf(self):
        return self._scurve_lf

    def getScurveDataEsTotal(self):
        return self._scurve_es_total

    def getScurveDataEsAccTotal(self):
        """
        누적된 Scurve ES 데이터를 반납한다.
        """
        acc_list = {}
        sum = 0

        for i in range(self._start_day, self._end_day + 1):
            sum = sum + self._scurve_es_total[i]
            acc_list[i] = sum

        return acc_list

    def getScurveDataLfTotal(self):
        return self._scurve_lf_total

    def getScurveDataLfAccTotal(self):
        """
        누적된 Scurve LF 데이터를 반납한다.
        """
        acc_list = {}
        sum = 0

        for i in range(self._start_day, self._end_day + 1):
            sum = sum + self._scurve_lf_total[i]
            acc_list[i] = sum

        return acc_list

    def getStartDay(self):
        return self._start_day

    def getEndDay(self):
        return self._end_day        
    
    def initData(self):
        """
        PND 데이터를 기반으로 시작일 및 종료일을 계산한다.
        또한 필요한 자료구조들을 초기화한다.
        """
        for key in self._pnd_data_dict.keys():
            if self._start_day == -1 or self._start_day > self._pnd_data_dict[key].getEs():
                self._start_day = self._pnd_data_dict[key].getEs()
            if self._end_day == -1 or self._end_day < self._pnd_data_dict[key].getEf():
                self._end_day = self._pnd_data_dict[key].getEf()
            self._scurve_es[key] = {}
            self._scurve_lf[key] = {}

        for i in range(self._start_day, self._end_day+1):
            self._scurve_es_total[i] = 0
            self._scurve_lf_total[i] = 0        

    def analyzeScurveWithEs(self):
        """ ES를 기반으로 S-Curve를 작성한다.
        각 Task 별 기간 별 Cost 데이터가 만들어진다."""
        for i in range(self._start_day, self._end_day+1):
            for key in self._pnd_data_dict.keys():
                task_info = self._pnd_data_dict[key]

                # Task에 드는 비용은 기간으로 나누어, 일별로 계산한다.
                cost_per_day = task_info.getCost() / task_info.getDuration()
                
                if task_info.getEs() <= i and task_info.getEf() >= i:
                    self._scurve_es[key][i] = cost_per_day
                    self._scurve_es_total[i] = self._scurve_es_total[i] + self._scurve_es[key][i]
                else:
                    self._scurve_es[key][i] = 0

        # key값으로 정렬한다.
        ordered_scurve_es = collections.OrderedDict(sorted(self._scurve_es.items()))
        self._scurve_es = ordered_scurve_es
    
    def analyzeScurveWithLf(self):
        """ LF를 기반으로 S-Curve를 작성한다.
        각 Task 별 기간 별 Cost 데이터가 만들어진다."""
        for i in range(self._start_day, self._end_day+1):
            for key in self._pnd_data_dict.keys():
                task_info = self._pnd_data_dict[key]
                
                # Task에 드는 비용은 기간으로 나누어, 일별로 계산한다.
                cost_per_day = task_info.getCost() / task_info.getDuration()
                
                if task_info.getLs() <= i and task_info.getLf() >= i:
                    self._scurve_lf[key][i] = cost_per_day
                    self._scurve_lf_total[i] = self._scurve_lf_total[i] + self._scurve_lf[key][i]
                else:
                    self._scurve_lf[key][i] = 0
        # key값으로 정렬한다.
        ordered_scurve_lf = collections.OrderedDict(sorted(self._scurve_lf.items()))
        self._scurve_lf = ordered_scurve_lf

if __name__ == "__main__":    
    a = PNDHandler("data2.csv")
    a.analyze()
    b = SCurveHandler(a.getPNDDataDict())
    b.analyzeScurveWithEs()
    b.analyzeScurveWithLf()           
