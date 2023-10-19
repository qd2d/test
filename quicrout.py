#####################################################################
#  Copyright 2020 Davie John Mtsuko.                                     #
#  This file is part of quicpy, distributed under the terms of the  #
#  None Software License - Version 1.0.  See the accompanying      #
#  LICENSE file or <http://www.none.org/LICENSE_1_0.txt>           #
#####################################################################
import time
from random import random
import gdspy
import numpy

#Other possible libraries

import collections
from numpy.core._multiarray_umath import ndarray
from gdspy import Cell
#from gdsCAD import *
import csv
import pandas
import numpy as np
from math import pi
import numpy.linalg as linalg
import scipy.interpolate
#import shapely.geometry
#import shapely.affinity
#import shapely.ops
#import shapely.validation


#from gdshelpers.parts import Port
#from gdshelpers.helpers import find_line_intersection, normalize_phase
#from gdshelpers.helpers.bezier import CubicBezierCurve
#from gdshelpers.helpers.positive_resist import convert_to_positive_resist
#from gdshelpers.geometry.chip import Cell
#from gdshelpers.parts.waveguide import Waveguide
#from gdshelpers.parts.coupler import GratingCoupler
#from gdshelpers.parts.interferometer import MachZehnderInterferometer
#from gdshelpers.parts.text import Text

class _device():
    def create_device():

        # Layer/datatype definitions for each step in the fabrication
        ld_liftoff1 = {"layer": 1, "datatype": 0}
        ld_liftoff2 = {"layer": 2, "datatype": 0}
        ld_liftoff3 = {"layer": 3, "datatype": 0}
        ld_gates = {"layer": 4, "datatype": 0}
        ld_majorana_fermions = {"layer": 5, "datatype": 0}  # This is just a label, not physica

        p1 = gdspy.Rectangle((-50, -2.5), (50, 2.5), **ld_liftoff1)
        p2 = gdspy.Rectangle((-52, -3), (-50, 9), **ld_liftoff2)
        p3 = gdspy.Rectangle((54, -2.5), (50, 2.5), **ld_liftoff3)
        p4 = gdspy.Round((-104.5, 0), 2.5, number_of_points=64, **ld_majorana_fermions)
        p5 = gdspy.Round((45, 0), 2.5, number_of_points=64, **ld_majorana_fermions)
        p6 = gdspy.Rectangle((-110, -2.5), (110, 2.5), **ld_liftoff1)
        p7 = gdspy.Round((104.5, 0), 2.5, number_of_points=64, **ld_majorana_fermions)
        p8 = gdspy.Rectangle((114, -2.5), (110, 2.5), **ld_liftoff3)
        p9 = gdspy.Rectangle((-114, -2.5), (-110, 2.5), **ld_liftoff3)
        p10 = gdspy.Rectangle((54, -7), (56, 7), **ld_liftoff3)
        p11 = gdspy.Rectangle((114, -7), (116, 7), **ld_liftoff3)
        p12 = gdspy.Rectangle((-114, -7), (-116, 7), **ld_liftoff3)
        # Label anchored at (1, 3) by its north-west corner
        p13 = gdspy.Label("TSC", (-10, 0), "nw")
        p14 = gdspy.Label("MZM", (40, 0), "nw")

        g10 = gdspy.Rectangle((55, 1), (57, 1.5), **ld_gates)
        g10_2 = gdspy.Rectangle((55, -1), (57, -1.5), **ld_gates)

        g11 = gdspy.Rectangle ((110.5, 1), (112.5, 1.5), **ld_gates)
        g12 = gdspy.Rectangle((-110.5, 1), (-112.5, 1.5), **ld_gates)
        g11_2 = gdspy.Rectangle((110.5, -1), (112.5, -1.5), **ld_gates)
        g12_2 = gdspy.Rectangle((-110.5, -1), (-112.5, -1.5), **ld_gates)

        # Create a cell with a component that is used repeatedly
        nanowire1 = gdspy.Cell("nanowire1")
        nanowire2 = gdspy.Cell("nanowire2")
        nanowire3 = gdspy.Cell("nanowire3")

        nanowire1.add([p1, p2, p3, p5, p10, p13, p14, g10, g10_2])
        nanowire2.add([p1, p3, p5, p10, p13, p14, g10, g10_2])
        nanowire3.add([p6, p4, p7, p8, p9, p11, p12, p13, p14, g11, g12, g11_2, g12_2])

        # Create a cell with the complete device
        device1 = gdspy.Cell("DEVICE1")
        device2 = gdspy.Cell("DEVICE2")

        # Add 2 references to the component changing size and orientation
        ref1 = gdspy.CellReference(nanowire1, (15, 1), magnification=0.25)
        ref2 = gdspy.CellReference(nanowire1, (-15, 1), magnification=0.25, rotation=180)
        ref3 = gdspy.CellReference(nanowire1, (42, 13), magnification=0.25, rotation=180)
        ref4 = gdspy.CellReference(nanowire1, (-42, 13), magnification=0.25, rotation=0)
        ref5 = gdspy.CellReference(nanowire1, (42, -11), magnification=0.25, rotation=180)
        ref6 = gdspy.CellReference(nanowire1, (-42, -11), magnification=0.25, rotation=0)

        device1.add([ref1, ref2, ref3, ref4, ref5, ref6])
        ref1_2 = gdspy.CellReference(nanowire1, (15, 25), magnification=0.25)
        ref2_2 = gdspy.CellReference(nanowire1, (-15, 25), magnification=0.25, rotation=180)
        ref3_2 = gdspy.CellReference(nanowire2, (42, 7), magnification=0.25, rotation=180)
        ref4_2 = gdspy.CellReference(nanowire2, (-42, 7), magnification=0.25, rotation=0)
        ref5_2 = gdspy.CellReference(nanowire1, (15, -11), magnification=0.25, rotation=0)
        ref6_2 = gdspy.CellReference(nanowire1, (-15, -11), magnification=0.25, rotation=180)
        ref7 = gdspy.CellReference(nanowire3, (0, 19), magnification=0.25)
        ref8 = gdspy.CellReference(nanowire3, (0, -5), magnification=0.25)

        device2.add([ref1_2, ref2_2, ref3_2, ref4_2, ref5_2, ref6_2, ref7, ref8])
        # device.add(ref1)

        # The final layout has several repetitions of the complete device
        top = gdspy.Cell("TOP")

        top.add(gdspy.CellArray(device1, 1, 6, (6, 3)))
        top.add(gdspy.CellArray(device2, 1, 2, (6, 3)))

        # Save the library in a file called 'first.gds'.
        gdspy.write_gds("hexon.gds")

        # Optional: Display all cells using the internal viewer.

        return()

class Bondpads():
    def bondpadarray(cellname1, cellname2, cellname3, topcell1, number, pitch: object, width: object, length: object, extension1: object, extension2: object) -> object:
        unitCell1 = gdspy.Cell(cellname1)
        rectangle = gdspy.Rectangle((0.0, 0.0), (width, length), layer=1, datatype=0)
        polygon = gdspy.Polygon([(-5,-5),(-55,50),(-5,105),(105,105),(105,-5)],7,0)
        unitCell1.add(rectangle)
        unitCell1.add(polygon)

        unitCell2 = gdspy.Cell(cellname2)
        rectangle = gdspy.Rectangle((0.0 + extension1, 0.0 +extension1), (width - extension1, length - extension1), layer=2, datatype=0)
        unitCell2.add(rectangle)

        unitCell3 = gdspy.Cell(cellname3)
        rectangle = gdspy.Rectangle((0.0 + extension2, 0.0 + extension2), (width - extension2, length - extension2), layer=3, datatype=0)
        unitCell3.add(rectangle)

        top = gdspy.Cell(topcell1)
        top.add(gdspy.CellArray(unitCell1, 1, number, (6, pitch)))
        top.add(gdspy.CellArray(unitCell2, 1, number, (6, pitch)))
        top.add(gdspy.CellArray(unitCell3, 1, number, (6, pitch)))

        return(rectangle)

class gates():
    def createGateLines():
        gate=gdspy.Cell("GATE")
        g1 = gdspy.FlexPath([(-500.0,450.0), (-275.0, 225.0), (-250.0, 20.0),
                                    (-56, 20.0)], 2.0, ends=["flush"], corners=["round"], bend_radius=5, gdsii_path=False, layer=1, datatype=0)
        g2 = gdspy.FlexPath ([(-500.0, 450.0), (-275.0, 225.0), (-250.0, 20.0), (-100.0, 20.0)], 10.0, ends=["round"], corners=["round"], bend_radius=5,
                                    gdsii_path=True, layer=6, datatype=0)

        g3 = gdspy.FlexPath ([(-500.0, -450.0), (-275.0, -225.0), (-250.0, -20.0),
                              (-56, -20.0)], 2.0, ends=["flush"], corners=["round"], bend_radius=5, gdsii_path=False,
                             layer=1, datatype=0)
        g4 = gdspy.FlexPath ([(-500.0, -450.0), (-275.0, -225.0), (-250.0, -20.0), (-100.0, -20.0)], 10.0, ends=["round"],
                             corners=["round"], bend_radius=5,
                             gdsii_path=False, layer=6, datatype=0)
        gate.add([g1,g2,g3,g4])

        #Righthand side

        g5 = gdspy.FlexPath ([(500.0, 450.0), (275.0, 225.0), (250.0, 20.0),
                              (56, 20.0)], 2.0, ends=["flush"], corners=["round"], bend_radius=5, gdsii_path=True,
                             layer=1, datatype=0)
        g6 = gdspy.FlexPath ([(500.0, 450.0), (275.0, 225.0), (250.0, 20.0), (100.0, 20.0)], 10.0, ends=["round"],
                             corners=["round"], bend_radius=5,
                             gdsii_path=True, layer=6, datatype=0)

        g7 = gdspy.FlexPath ([(500.0, -450.0), (275.0, -225.0), (250.0, -20.0),
                              (56, -20.0)], 2.0, ends=["flush"], corners=["round"], bend_radius=5, gdsii_path=True,
                             layer=1, datatype=0)
        g8 = gdspy.FlexPath ([(500.0, -450.0), (275.0, -225.0), (250.0, -20.0), (100.0, -20.0)], 10.0,
                             ends=["round"],
                             corners=["round"], bend_radius=5,
                             gdsii_path=True, layer=6, datatype=0)
        gate.add ([g1, g2, g3, g4, g5, g6, g7, g8])
        return()

class parameterized():
    def path_from_table(width):
        def nwOrigin(index):
            df = pandas.read_excel('qd2dChip.xls',
                index_col='nanowireName',
                parse_dates=['xCenter', 'yCenter'],
                header=0,
                names=['nanowireName', 'xCenter', 'yCenter'])

            df.to_csv('qchip.csv')
            coordCenterList = df['xCenter'][index], df['yCenter'][index]
            int_coordCenterList = tuple([int (x) for x in coordCenterList])
            print(df)
            print(int_coordCenterList)
            return(int_coordCenterList)
        path1 = gdspy.FlexPath([nwOrigin(0), nwOrigin(2), nwOrigin(3), nwOrigin(1)], width)
        path2 = gdspy.FlexPath([nwOrigin(0), nwOrigin(1), nwOrigin(2)], width+2)
        path3 = gdspy.FlexPath([nwOrigin(4), nwOrigin(5), nwOrigin(6), nwOrigin(7)], width)
        path4 = gdspy.FlexPath([nwOrigin(4), nwOrigin(5), nwOrigin(6)], width+2)

        path5 = gdspy.FlexPath([nwOrigin(8), nwOrigin(9), nwOrigin(10), nwOrigin(11)], width)
        path6 = gdspy.FlexPath([nwOrigin(8), nwOrigin(9), nwOrigin(10)], width+2)
        path7 = gdspy.FlexPath([nwOrigin(12), nwOrigin(13), nwOrigin(14), nwOrigin(15)], width)
        path8 = gdspy.FlexPath([nwOrigin(12), nwOrigin(13), nwOrigin(14)], width+2)


        par = gdspy.Cell("PARAM")
        par.add(path1)
        par.add(path2)
        par.add(path3)
        par.add(path4)
        par.add (path5)
        par.add (path6)
        par.add (path7)
        par.add (path8)
        return()


'''
------------------------------------------------------------------------------------------------------------------
Calls the classes
------------------------------------------------------------------------------------------------------------------
'''
action1 = _device
action2 = Bondpads
action3 = gates
action4 = parameterized

'''
------------------------------------------------------------------------------------------------------------------
Action1: Create the hexon device
------------------------------------------------------------------------------------------------------------------
'''''

mastercell5 = action1.create_device()
master_library = gdspy.library.GdsLibrary(infile=r'C:\Users\User\quicpy\hexon.gds')
mastercell2 = master_library.top_level()[-1]
ref5= gdspy.CellReference(mastercell2, (0,-8.5), magnification=1)
print("The device was successfully created")

'''
------------------------------------------------------------------------------------------------------------------
Action2: Create the bonding pads
------------------------------------------------------------------------------------------------------------------
'''''
##Create gds file
mastercell1 = action2.bondpadarray("CELL1", "CELL2", "CELL3", "BONDPADS", 7, 150, 100, 100, 5, 10)
gdspy.write_gds("bondpads.gds")
##stream in gds to get instances for high level main cell
master_library2 = gdspy.library.GdsLibrary(infile=r'C:\Users\User\quicpy\bondpads.gds')
mastercell3 = master_library2.top_level()[0]


'''
------------------------------------------------------------------------------------------------------------------
Action3: Create the horizontally oriented electrodes
------------------------------------------------------------------------------------------------------------------
'''''
mastercell6=action3.createGateLines()
gdspy.write_gds("gates.gds")
master_library3 = gdspy.library.GdsLibrary(infile=r'C:\Users\User\quicpy\gates.gds')
mastercell7 = master_library3.top_level()[0]
ref6= gdspy.CellReference(mastercell7, (0,0), magnification=1)
ref7= gdspy.CellReference(mastercell7, (0,0), rotation=90, magnification=1)


''''
-------------------------------------------------------------------------------------------------------------------
Action4: Create the vertically oriented electrodes from Excel sheet
-------------------------------------------------------------------------------------------------------------------
'''
mastercell8 = action4.path_from_table(1)
gdspy.write_gds("parameterized.gds")
time.sleep(random() * 0.1 * 60)

master_library4 = gdspy.library.GdsLibrary(infile=r'C:\Users\User\quicpy\parameterized.gds')
mastercell9 = master_library4.top_level()[0]


''''
-------------------------------------------------------------------------------------------------------------------
Action 5: Create a high level cell and place instances generated in actions 1 to 4 and save a gds file.
-------------------------------------------------------------------------------------------------------------------
'''
subCell2 = gdspy.Cell("SUB2")
ref1=gdspy.CellReference(mastercell3, (550,-500), magnification=1)
ref2=gdspy.CellReference(mastercell3, (-550,500), magnification=1, rotation=180)
ref3=gdspy.CellReference(mastercell3, (500,550), rotation=90, magnification=1)
ref4=gdspy.CellReference(mastercell3, (-500,-550), rotation=-90, magnification=1)
ref8= gdspy.CellReference(mastercell9, (0,0), magnification=1)
ref9= gdspy.CellReference(mastercell9, (0,0), rotation=180, magnification=1)
subCell2.add([ref1, ref2, ref3, ref4, ref5, ref6, ref7, ref8, ref9]) #ref8, ref9#
gdspy.write_gds("quantum_chip_01.gds")
gdspy.LayoutViewer(pattern={'default': 8}, depth=4, background='#FFFFFF')
subCell2.write_svg("quantum_chip_01.svg")
print("The microdevice was successfully created")
print("Please open the following gds files:\n")
print("(1)hexon.gds")
print("(2)bondpads.gds")
print("(3)gates.gds")
print("(4)parameterized.gds")
print("(and)\n")
print("(5)quantum_chip_01.gds\n")
print("Instruction: Run the program again several times before updating the first 4 gds files.")

