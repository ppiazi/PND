# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 09:35:56 2015

@author: ppiazi
"""

class TaskEntity:
    ROOT_NODE = 1
    NORMAL_NODE = 2
    END_NODE = 3
       
    def __init__(self, name, duration, next_tasks, entity_type, cost, hs):        
        self._name = name
        self._duration = duration
        self._entity_type = entity_type
        self._es = -1
        self._ef = -1
        self._ls = -1
        self._lf = -1
        self._tf = -1
        self._next_tasks = next_tasks
        self._prev_tasks = []
        self._cost = cost
        self._hs = hs
        
    def setEntityType(self, entity_type):
        self._entity_type = entity_type
        
    def getEntityType(self):
        return self._entity_type

    def setName(self, name):
        self._name = name
        
    def getName(self):
        return self._name
        
    def setEs(self, es):
        self._es = es
        
    def getEs(self):
        return self._es

    def setEf(self, ef):
        self._ef = ef
        
    def getEf(self):
        return self._ef

    def setDuration(self, duration):
        self._duration = duration
        
    def getDuration(self):
        return self._duration

    def setLs(self, ls):
        self._ls = ls
        
    def getLs(self):
        return self._ls
    
    def setLf(self, lf):
        self._lf = lf
        
    def getLf(self):
        return self._lf
    
    def calTf(self):
        if self._ls != -1 and self._es != -1:
            self._tf = self._ls - self._es
        else:
            self._tf = -1
    
    def getTf(self):
        return self._tf
    
    def addNextTask(self, next_task):
        self._next_tasks.append(next_task)
        
    def getNextTasks(self):
        return self._next_tasks
        
    def addPrevTask(self, prev_task):
        self._prev_tasks.append(prev_task)
        
    def getPrevTasks(self):
        return self._prev_tasks

    def setCost(self, cost):
        self._cost = cost        
    
    def getCost(self):
        return self._cost
        
    def setHs(self, hs):
        self._hs = hs
    
    def getHs(self):
        return self._hs
    