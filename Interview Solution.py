
from copy import copy

import enum
import string
from turtle import clone, left, right
from urllib.parse import ParseResultBytes
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
        "LiningThickness" : .5,
        "LiningOffset" : 3,
        "LiningToPanelOffsetX" : 4,
        "LiningToPanelOffsetY" : 5,
        "TransomThickness" : 6,
        "MullionThickness": 6,
       
}

PanelSettings = {
    "Outer_curves": np.array([[0,0,0,0,0],[0,2,2,0,0],[0,0,2,2,0]]),
    "Inner_curves": np.array([[0,0,0,0,0],[.5,1.5,1.5,.5,0.5],[0.5,0.5,1.5,1.5,0.5]]),
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
        elif(kargs["PartitioningType"] == PartitionType.TriplePanelVertical):
            return self.create_tripple_panel_vertical(**kargs)
            
        return
    
    def create_single_panel(self,**kargs):
        return np.array([kargs["Outer_curves"]
                        ,kargs["Inner_curves"]
                        , np.vstack([ np.array([kargs["Y_offset"],kargs["Y_offset"],kargs["Y_offset"],kargs["Y_offset"],kargs["Y_offset"]])
                          ,kargs["Outer_curves"][1],kargs["Outer_curves"][2]])
                        ,np.vstack([np.array([kargs["Y_offset"],kargs["Y_offset"],kargs["Y_offset"],kargs["Y_offset"],kargs["Y_offset"]])
                          ,kargs["Inner_curves"][1],kargs["Inner_curves"][2]])
                        ])
    def create_double_panel_vertical(self,**kargs):
             
        change = kargs["MullionThickness"]/2
        tempkargs = kargs
        topPannel= self.create_single_panel(**tempkargs)
        bottomPannel = np.copy(topPannel)
        ch = np.max([np.array([topPannel[0][2]])])
        transom = self.create_panel_withoutInnercurves(kargs["Outer_curves"][0][0],kargs["Outer_curves"][1][0],-change,kargs["Outer_curves"][1][1],change*2,kargs["Y_offset"])
        for i in range(4):
            topPannel[i][2] += change
            bottomPannel[i][2] -= change +ch
    
        
        
       
        
        return np.array([topPannel,transom,bottomPannel])
        
    def create_double_panel_horizontal(self,**kargs):
        change = kargs["TransomThickness"]/2
        tempkargs = kargs
        leftPanel = self.create_single_panel(**tempkargs)
        rightPanel = self.create_single_panel(**tempkargs)
        # print(change)
        transom = self.create_panel_withoutInnercurves(kargs["Outer_curves"][0][0],-change,kargs["Outer_curves"][2][0],change*2,kargs["Outer_curves"][2][2],kargs["Y_offset"])
        for i in range(4):
            rightPanel[i][1] += change
            leftPanel[i][1] -= change
    

       
        
        return np.array([leftPanel,transom,rightPanel])
    
    def create_tripple_panel_horizontal(self,**kargs):
        change = kargs["TransomThickness"]/2
        leftMostPanel = self.create_single_panel(**kargs)
        rightMostPanel = self.create_single_panel(**kargs)
        middlePanel = self.create_single_panel(**kargs)
        


        ch = np.max(np.array(middlePanel[0][1]))/2
        
        for i in range(4):
            temp = np.copy(middlePanel[i][1])
            temp -= ch
            middlePanel[i][1] = np.copy(temp)

        for i in range(4):

            
            temp = np.copy(middlePanel[i][1])

            temp -= (change*2)
            temp -= ch*2
            leftMostPanel[i][1] = np.copy(temp)

            
            
           
            
        
            
            temp = np.copy(rightMostPanel[i][1])
            temp += (change*2)
            temp += np.max(np.array([middlePanel[0][1]]))
            rightMostPanel[i][1] = np.copy(temp)        
           
        righttransom = self.create_panel_withoutInnercurves(kargs["Outer_curves"][0][0],np.max(np.array([middlePanel[0][1]],dtype=np.float16).argmax()),
                                                            kargs["Outer_curves"][2][0],change*2,kargs["Outer_curves"][2][2],kargs["Y_offset"])
        
       
        lefttransom = np.copy(righttransom)
        
        lefttransom[0][1] -= np.max(np.array(middlePanel)) + (change*2)
        lefttransom[1][1] -= np.max(np.array(middlePanel)) + (change*2)
    

        
        
        
       
        
        return np.array([leftMostPanel,lefttransom,middlePanel,righttransom,rightMostPanel],dtype=object)
    def create_tripple_panel_vertical(self,**kargs):
        change = kargs["MullionThickness"]/2
        
        middlePanel = self.create_single_panel(**kargs)
        bottompanel = self.create_single_panel(**kargs)
        toppanel = self.create_single_panel(**kargs)


        ch = np.max(np.array(middlePanel[0][2]))/2
        
            

        for i in range(4):
            temp = np.copy(middlePanel[i][2])
            temp -= ch
            middlePanel[i][2] = np.copy(temp)
            
            
            temp -= (change*2)
            temp -= ch*2
            bottompanel[i][2] = np.copy(temp)
            
            
            temp = np.copy(middlePanel[i][2])
            temp += (change*2)
            temp += ch*2
            toppanel[i][2] = np.copy(temp)

            

        toptransom = self.create_panel_withoutInnercurves(kargs["Outer_curves"][0][0],kargs["Outer_curves"][1][0],np.max(np.array([middlePanel[0][2]])),
                                                            np.max(np.array([middlePanel[0][1]])),change*2,kargs["Y_offset"])

        downtransom = np.copy(toptransom)        
        downtransom[0][2] += -(ch*2 )-(change*2)
        downtransom[1][2] += -(ch*2)-(change*2)
        return np.array([toppanel,toptransom,middlePanel,downtransom,bottompanel],dtype=object)
    

        
        
        
       
        


    
        
        
        
       
        

        
        
        
       
        
        return np.array([leftMostPanel,lefttransom,middlePanel,righttransom,rightMostPanel])
    def create_rectangle(self,x,y,z):
        return np.array([[x,x,x,x,x]
                         ,[x,y,y,x,x]
                         ,[x,x,z,z,x]])
       
    
    def create_panel_withoutInnercurves(self,orignalPostionx,orignalPositiony,orignalPositionz,width,height,depth):
        return np.array([np.array([[orignalPostionx,orignalPostionx,orignalPostionx,orignalPostionx,orignalPostionx]
                         ,[orignalPositiony,orignalPositiony+width,orignalPositiony+width,orignalPositiony,orignalPositiony]
                         ,[orignalPositionz,orignalPositionz,orignalPositionz+height,orignalPositionz+height,orignalPositionz]]),
                         np.array([[depth,depth,depth,depth,depth]
                         ,[orignalPositiony,orignalPositiony+width,orignalPositiony+width,orignalPositiony,orignalPositiony]
                         ,[orignalPositionz,orignalPositionz,orignalPositionz+height,orignalPositionz+height,orignalPositionz]])])
        
    pass












wc = WindowCreator()

print(wc.create_3d(**PanelSettings,**IfcWindowLiningProperties))