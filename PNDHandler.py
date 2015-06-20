# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 09:40:07 2015

@author: ppiazi
"""

from TaskEntity import TaskEntity
from PNDDataReader import PNDDataReader

class PNDHandler:
    def __init__(self, file_name):
        self._pnd_data_reader = PNDDataReader(file_name)
        self._pnd_data_dict = {}
        self._root_task_name = ""
        self._end_task_name = ""
        self._critical_paths = []

    def getPNDDataDict(self):
        return self._pnd_data_dict

    def getCriticalTasks(self):
        """ Critial Tasks를 검색하여 결과를 반환한다."""
        critical_path = []

        # TF가 0인 TASK를 검색한다.
        for key in self._pnd_data_dict.keys():
            if self._pnd_data_dict[key].getTf() == 0:
                critical_path.append(self._pnd_data_dict[key])
                
        return critical_path
    
    def getCriticalPaths(self):
        """ Critical Path를 검색하여 결과를 반환한다."""
        path_list = []
        self.findCriticalPaths(self._root_task_name, path_list)
        return self._critical_paths
    
    def findCriticalPaths(self, start_task_name, path_list):
        """ Critical Path를 검색한다. """
        start_task = self._pnd_data_dict[start_task_name]
        
        if start_task.getTf() != 0:
            return False

        path_list.append(start_task)
            
        if start_task.getNextTasks() == None:
            self._critical_paths.append(path_list)
            return True
            
        for next_task_name in start_task.getNextTasks():
            ret = self.findCriticalPaths(next_task_name, path_list)
            if ret == True:
                return True
        
    def analyze(self):
        """ 주어진 Task 정보를 분석하여 ES, EF, LS, LF, TF를 계산한다."""
        self._pnd_data_dict = self._pnd_data_reader.loadFile()
        if self._pnd_data_dict == None:
            return False

        self._root_task_name = self.findTaskNameByType(TaskEntity.ROOT_NODE)
        self._end_task_name = self.findTaskNameByType(TaskEntity.END_NODE)

        self.goForward(self._root_task_name, None, 1)        
        self.goBackward(self._end_task_name, self._pnd_data_dict[self._end_task_name].getEf())
        self.calTf()

        return True
    
    def findTaskNameByType(self, ntype):
        """ Task가 Root인지 End 인지 파악한다."""
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
        """ 순방향 분석을 수행하여 ES, EF를 계산한다."""
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
        """ 분석결과를 전시한다. """
        for key in self._pnd_data_dict.keys():
            task_info = self._pnd_data_dict[key]
            print("%s \t %d \t %d \t %d \t %d \t %d \t %d" % (task_info.getName(), task_info.getDuration(), task_info.getEs(), task_info.getEf(), task_info.getLs(), task_info.getLf(), task_info.getTf()))
            
    def displayList(self, list_data):
        for task_info in list_data:
            print("%s \t %d \t %d \t %d \t %d \t %d \t %d" % (task_info.getName(), task_info.getDuration(), task_info.getEs(), task_info.getEf(), task_info.getLs(), task_info.getLf(), task_info.getTf()))
    
    def goBackward(self, start_task_name, t_lf):
        """ 역방향 분석을 수행하여 LS, LF를 계산한다."""
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
        """ TF를 계산한다. """
        for key in self._pnd_data_dict.keys():
            self._pnd_data_dict[key].calTf()

def displayList(list_data):
    for task_info in list_data:
        print("%s \t %d \t %d \t %d \t %d \t %d \t %d" % (task_info.getName(), task_info.getDuration(), task_info.getEs(), task_info.getEf(), task_info.getLs(), task_info.getLf(), task_info.getTf()))

if __name__ == "__main__":
    a = PNDHandler("data2.csv")
    a.analyze()
    a.displayData()
    a.getCriticalTasks()
    print("Critical Path");
    b = a.getCriticalPaths()
    displayList(b[0])
