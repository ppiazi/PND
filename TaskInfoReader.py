# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 09:55:09 2015

@author: ppiazi
"""

import csv
import TaskEntity
import collections

class PNDDataReader:
    def __init__(self, file_name):
        self._file_name = file_name
        
    def loadFile(self):
        """
        read a csv file containing task information and return a dict.
        """
        try:
            csv_file = open(self._file_name)
        except:
            print("Error : file not found %s" % self._file_name)
            return None

        csv_reader = csv.reader(csv_file, delimiter=',')
        
        task_dict = {}        
        
        for row in csv_reader:
            if row[2] != '':
                next_list = row[2].split(',')
            else:
                next_list = None
            # 0 : Name, 1 : Duration, 2 : Next Tasks, 3 : Node Type
            t = TaskEntity.TaskEntity(row[0], int(row[1]), next_list, int(row[3]), int(row[4]), int(row[5]))
            task_dict[row[0]] = t
        
        ordered_task_dict = collections.OrderedDict(sorted(task_dict.items()))        
        
        return ordered_task_dict

if __name__ == "__main__":
    a = PNDDataReader("data1.csv")
    d = a.loadFile()