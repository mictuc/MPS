#!/usr/bin/env python

"""Module to define classes and functions used in MPS"""

__author__ = "Michael Tucker"
__copyright__ = "Copyright 2019, Michael Tucker"
__license__ = "GNU v3.0"
__version__ = "1.0.1"
__email__ = "mic.tuc@me.com"

class Part:
    def __init__(self,name,number,cad,drawing,unit):
        self.name = name
        self.number = number
        self.cad = cad
        self.drawing = drawing
        self.unit = unit

    def get_ebom(self, qty=1):
        return [(self,qty)]

class Assy:
    def __init__(self,name,number,cad,drawing,unit,components):#,processes,production_line):
        self.name = name
        self.number = number
        self.cad = cad
        self.drawing = drawing
        self.unit = unit
        self.components = components
        self.processes = []
        # self.production_line = production_line

    def get_ebom(self, qty=1):
        ebom = []
        for component in self.components:
            ebom += component.get_ebom(self.components[component])

        return [(self,qty),[ebom]]

    # def get_work_order(self, level=0):
    #     wo = [self.name]
    #     for process in self.processes:
    #         wo += process
    #
    #     return

    def print_work_order(self):
        print(self.name)
        for process in self.processes:
            print(' ' + process.name)
            for component in process.components:
                print('  ' + component.name + ' ' + component.unit + ' ' + str(process.components[component]))

class Process:
    def __init__(self,name,assy,components):#,work_instructions,cycle_time,cycles_per_unit,fixtures,tools,num_workers,expendables):
        self.name = name
        self.assy = assy
        self.components = components
        # self.work_instructions = work_instructions
        # self.cycle_time = cycle_time
        # self.cycles_per_unit = cycles_per_unit
        # self.time_per_unit = cycle_time * cycles_per_unit
        # self.fixtures = fixtures
        # self.tools = tools
        # self.num_workers = num_workers
        # self.expendables = expendables

        assy.processes.append(self)

class Work_Station:
    def __init__(self,name,number,processes,capital_equipment,space,capex):
        self.name = name
        self.number = number
        self.processes = processes
        self.capital_equipment = capital_equipment
        self.space = space
        self.capex = capex

    def station_cycle_time(self):
        return sum(process.time_per_unit for process in self.processes)

def print_bom(bom,level=0):
    for component in bom:
        if type(component) is tuple:
            print((level * ' ') + component[0].name + ' x' + str(component[1]))
        else:
            print_bom(component, level+1)

def main():
    nose = Part('Nose',10,'Nose.part','Nose.drw','ea')
    body = Part('Body',20,'Body.part','Body.drw','ea')
    spring = Part('Spring',30,'Spring.part','Spring.drw','ea')
    screw = Part('Screw',40,'Screw.part','Screw.drw','ea')
    rod = Part('Rod',50,'Rod.part','Screw.drw','ea')
    piston = Assy('Piston',60,'Piston-ASSY.assy','Piston-ASSY.drw','ea',{screw:2,rod:1})
    pen = Assy('Pen-ASSY',90,'Pen-ASSY.assy','Pen-ASSY.drw','ea',{body:1,spring:3,piston:4,nose:1})

    print_bom(rod.get_ebom())
    print_bom(piston.get_ebom())
    print_bom(pen.get_ebom())

    p1 = Process('Clean rod',piston,{rod:1})
    p1a = Process('Screw1',piston,{screw:1})
    p1b = Process('Screw2',piston,{screw:1})
    p1c = Process('Measure piston',piston,{})
    p2 = Process('Put piston into body',pen,{piston:4,body:1})
    p3 = Process('Put first springs in',pen,{spring:2})
    p4 = Process('Put last spring in',pen,{spring:1})
    p5 = Process('Put nose on',pen,{nose:1})
    p6 = Process('Shine pen',pen,{})
    p7 = Process('Test pen',pen,{})
    p8 = Process('Pack Pen',pen,{})

    pen.print_work_order()

main()
