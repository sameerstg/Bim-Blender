
import enum
import string
from turtle import left
from matplotlib import transforms
import numpy as np
import matplotlib.pyplot as plt
from enum import Enum
 

class PartitionType(Enum):
    Single = 1
    DoublePanelVertical = 2
    DoublePanelHorizontal = 3
    TriplePanelVertical = 4
    TriplePanelHorizontal = 5
 
settings = {
    "OverallWidth": 1,
    "OverallHeight": 2,
    "Offset":float,
    

}
IfcWindowLiningProperties = {
        "LiningDepth": 1,
        "LiningThickness" : 3,
        "LiningOffset" : 3,
        "LiningToPanelOffsetX" : 4,
        "LiningToPanelOffsetY" : 5,
        "TransomThickness" : 4,
        "MullionThickness": 6,
       
}
PanelSettings = {
    "Outer_curves": np.array([np.array([0,0,0,0,0]),np.array([0,2,2,0,0]),np.array([0,0,2,2,0])]),
    "Inner_curves": np.array([np.array([0,0,0,0,0]),np.array([0,1,1,0,0]),np.array([0,0,1,1,0])]),
    "Y_offset": IfcWindowLiningProperties["LiningThickness"],
    "Y_depth":IfcWindowLiningProperties["LiningDepth"],
    "PartitioningType": PartitionType.TriplePanelHorizontal
}
class WindowCreator:

    def create_2d(self,**kargs):
        return np.array([[0,0,0,0,0], [0,kargs["OverallWidth"],kargs["OverallWidth"],0,0], [0,0,kargs["OverallHeight"],kargs["OverallHeight"],0]])
    
    def create_3d(self,**kargs):
        if(kargs["PartitioningType"] == PartitionType.Single):
            return self.create_single_panel(**kargs)
        elif(kargs["PartitioningType"] == PartitionType.DoublePanelVertical):
            return self.create_double_panel_vertical(**kargs)
        elif(kargs["PartitioningType"] == PartitionType.DoublePanelHorizontal):
            return self.create_double_panel_horizontal(**kargs)
        elif(kargs["PartitioningType"] == PartitionType.TriplePanelHorizontal):
            return self.create_tripple_panel_horizontal(**kargs)
            
        return
    
    def create_single_panel(self,**kargs):
        return np.array([[kargs["Outer_curves"]]
                        ,[kargs["Inner_curves"]]
                        ,[[kargs["Y_offset"],kargs["Y_offset"],kargs["Y_offset"],kargs["Y_offset"]]
                          ,kargs["Outer_curves"][1],kargs["Outer_curves"][2]]
                        ,[[kargs["Y_offset"],kargs["Y_offset"],kargs["Y_offset"],kargs["Y_offset"]]
                          ,kargs["Inner_curves"][1],kargs["Inner_curves"][2]]
                        ])
    def create_double_panel_vertical(self,**kargs):
        change = kargs["MullionThickness"]/2
        tempkargs = kargs
        for i in range(5):
            tempkargs["Outer_curves"][2][i] += change
            tempkargs["Inner_curves"][2][i] += change
        
    
        firstPanel = self.create_single_panel(**tempkargs)
        for i in range(5):
            tempkargs["Outer_curves"][2][i] -= (change*2)
            tempkargs["Inner_curves"][2][i] -= (change*2)
        secondPanel = self.create_single_panel(**tempkargs)
        tempkargs["Outer_curves"][2][2] += change
        tempkargs["Outer_curves"][2][3] += change
        tempkargs["Inner_curves"][2][2] += change
        tempkargs["Inner_curves"][2][3] += change
        
        
        mullionPanel = self.create_single_panel(**tempkargs)
        
        return np.array([firstPanel,mullionPanel,secondPanel])
        
    def create_double_panel_horizontal(self,**kargs):
        change = kargs["TransomThickness"]/2
        tempkargs = kargs
        for i in range(5):
            tempkargs["Outer_curves"][1][i] += change
            tempkargs["Inner_curves"][1][i] += change
        
    
        firstPanel = self.create_single_panel(**tempkargs)
        for i in range(5):
            tempkargs["Outer_curves"][1][i] -= (change*2)
            tempkargs["Inner_curves"][1][i] -= (change*2)
        secondPanel = self.create_single_panel(**tempkargs)
        tempkargs["Outer_curves"][1][1] += change
        tempkargs["Outer_curves"][1][2] += change
        tempkargs["Inner_curves"][1][1] += change
        tempkargs["Inner_curves"][1][2] += change
        transom = self.create_single_panel(**tempkargs)
        return np.array([firstPanel,transom,secondPanel])
    
    def create_tripple_panel_horizontal(self,**kargs):
        change = kargs["TransomThickness"]/2
        leftMostPanel = self.create_single_panel(**kargs)
        rightMostPanel = self.create_single_panel(**kargs)
        middlePanel = self.create_single_panel(**kargs)
        lefttransom = self.create_single_panel(**kargs)
        righttransom = self.create_single_panel(**kargs)
        print(leftMostPanel)
        leftMostPanel[0][0][1] = (leftMostPanel[0][0][1]+leftMostPanel[0][0][1])+(change*1.5)
        
        print("....................................................")
        print(leftMostPanel)
        # print(leftMostPanel)
        
        
        return np.array([leftMostPanel,lefttransom,middlePanel,righttransom,rightMostPanel])
    def create_rectangle(self,x,y,z):
        return np.array([[x,x,x,x,x]
                         ,[x,y,y,x,x]
                         ,[x,x,z,z,x]])
       
    
    def create_panel(self):
        
        return
    pass












wc = WindowCreator()
# print(wc.create_3d(**PanelSettings,**IfcWindowLiningProperties))
wc.create_3d(**PanelSettings,**IfcWindowLiningProperties)
