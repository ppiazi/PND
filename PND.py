# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 09:40:07 2015

@author: ppiazi
"""

from TaskEntity import TaskEntity
from PNDDataReader import PNDDataReader

class PND:
    def __init__(self, file_name):
        self._pnd_data_reader = PNDDataReader(file_name)
        self._pnd_data_dict = self._pnd_data_reader.loadFile()
        self._root_task_name = self.findTaskNameByType(TaskEntity.ROOT_NODE)
        self._end_task_name = self.findTaskNameByType(TaskEntity.END_NODE)
        self.goForward(self._root_task_name, None, 1)        
        self.goBackward(self._end_task_name, self._pnd_data_dict[self._end_task_name].getEs())
        self.calTf()
    
    def findTaskNameByType(self, ntype):
        found = False
        task_name = None
        for key in self._pnd_data_dict.keys():
            entity_type = self._pnd_data_dict[key].getEntityType()
            
            if  entity_type == ntype:
                task_name = key
                found = True
                break

        return task_name
   
    def goForward(self, start_task_name, prev_task_name, t_es):
        start_task = self._pnd_data_dict[start_task_name]

        # 기존에 설정된 값이 입력된 값보다 크다면, 기존 값을 유지한다.
        if t_es <= start_task.getEs():
            t_es = start_task.getEs()
       
        if prev_task_name != None:
            start_task.addPrevTask(prev_task_name)
        
        t_ef = start_task.getDuration() + t_es - 1

        start_task.setEs(t_es)
        start_task.setEf(t_ef)
                
        if start_task.getNextTasks() == None:
            return
            
        for next_node_name in start_task.getNextTasks():
            self.goForward(next_node_name, start_task_name, t_ef + 1)
    
    def displayData(self):
        for key in self._pnd_data_dict.keys():
            task_info = self._pnd_data_dict[key]
            print("%s \t %d \t %d \t %d \t %d \t %d \t %d" % (task_info.getName(), task_info.getDuration(), task_info.getEs(), task_info.getEf(), task_info.getLs(), task_info.getLf(), task_info.getTf()))
    
    def goBackward(self, start_task_name, t_lf):
        start_task = self._pnd_data_dict[start_task_name]

        # 기존에 설정된 값이 입력된 값보다 크다면, 기존 값을 유지한다.
        if start_task.getLf() != -1 and t_lf > start_task.getLf():
            t_lf = start_task.getLf()
       
        t_ls = t_lf - start_task.getDuration() + 1

        start_task.setLf(t_lf)
        start_task.setLs(t_ls)
                
        if start_task.getPrevTasks() == None:
            return
            
        for prev_task_name in start_task.getPrevTasks():
            self.goBackward(prev_task_name, t_ls - 1)
            
    def calTf(self):
        for key in self._pnd_data_dict.keys():
            self._pnd_data_dict[key].calTf()

if __name__ == "__main__":
    a = PND("data1.csv")

    a.displayData()
