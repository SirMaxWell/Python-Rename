#ComplexRename.py

import maya.cmds as cmds
from functools import partial

def addPrefixOrSuffix(type, text):
    # get the selection
    selectionList=cmds.ls(selection=True)
    
    if len(selectionList)>0:
        
        #user inputa
        #checks the type if neither do nothing
        if text != "":#if left blank
            
            if type == "prefix":
                for obj in selectionList:
                    cmds.rename(obj, text + "_" + obj)
            if type == "suffix":
                for obj in selectionList:
                    cmds.rename(obj, obj + "_" + text)



    
def checkBoxChanged(type, *args):
    #gets the value of the checkboxs
    value = cmds.checkBox(type + "CB", q=True, v=True)
    
    if value ==True:
        if type == "searchReplace":
            cmds.textField("searchTF", edit=True, enable=True)
            cmds.textField("replaceTF", edit=True, enable=True)
        else:
            cmds.textField(type + "TF", edit=True, enable=True)
    if value ==False:
        if type == "searchReplace":
            cmds.textField("searchTF", edit=True, enable=False)
            cmds.textField("replaceTF", edit=True, enable=False)
        else:
            cmds.textField(type + "TF", edit=True, enable=False)
            
        
    
def applyCallback( *pArgs ):
    print ("Apply button pressed")
    
    #gets the values of checkboxes 
    prefixCB=cmds.checkBox("prefixCB", q=True,v=True)
    suffixCB=cmds.checkBox("suffixCB", q=True,v=True)
    searchReplaceCB=cmds.checkBox("searchReplaceCB", q=True,v=True)
    
    if prefixCB:
        text=cmds.textField("prefixTF", q=True, text=True)
        addPrefixOrSuffix("prefix", text)
    if suffixCB:
        text=cmds.textField("suffixTF", q=True, text=True)
        addPrefixOrSuffix("suffix", text)
    if searchReplaceCB:
        searchText=cmds.textField("searchTF", q=True, text=True)
        replaceText=cmds.textField("replaceTF", q=True, text=True)
        #print("works")
        searchAndReplace(searchText, replaceText)
        
def searchAndReplace(searchText, replaceText):
    selection = cmds.ls(sl = True)
    if len(selection) > 0:
        for object in selection:
            if object.find(searchText) != -1: # 0 = the first letter of a string, so -1 means it didnt find anything with that string
                newName = object.replace(searchText, replaceText)
                cmds.rename(object, newName)
            if object.find(searchText) == -1:
                cmds.warning("No Object with that name found")
                 
                 
    
    
    
        
def cancelCallBack( *pArgs ):
    cmds.deleteUI("myWindowID")
    
def createUi():
    windowID = "myWindowID"
    
    if cmds.window(windowID, exists=True):
        cmds.deleteUI(windowID) 
        
    cmds.window(windowID, title="Renamer", sizeable=False, resizeToFitChildren=True)

    layout = cmds.rowColumnLayout( numberOfColumns=4, columnWidth=[(1,80), (2,80), (3,100),(4,10)], columnOffset=[(10,'right',3)])
 
    
    #create the ui for the checkboxes 
    prefixCB = cmds.checkBox("prefixCB",label = "Add Prefix", v = False, cc = partial(checkBoxChanged, "prefix"))
    suffixCB = cmds.checkBox("suffixCB",label = "Add Suffix", value = False, cc = partial(checkBoxChanged, "suffix"))
    searchReplaceCB = cmds.checkBox("searchReplaceCB",label = "Search/Replace", v = False,cc = partial(checkBoxChanged, "searchReplace"))
    cmds.separator(h=10,style="none")
    #creates the text labels 
    textA = cmds.text(label = "Prefix")
    prefixTF = cmds.textField("prefixTF", w = 200, enable = False)
    cmds.separator(h=10,style="none")
    cmds.separator(h=10,style="none")
    textB = cmds.text(label = "Suffix")
    
    suffixTF = cmds.textField("suffixTF", w = 200, enable = False)
    
    
    
    
    cmds.separator(h=10,style="none")
    cmds.separator(h=10,style="none")
    
    textC = cmds.text(label = "Search For:")
    searchTF = cmds.textField("searchTF", w = 200, enable = False)
    cmds.separator(h=10,style="none")
    cmds.separator(h=10,style="none")
    textD = cmds.text(label = "Replace With:")
    replaceTF = cmds.textField("replaceTF", w = 200, enable = False)
    cmds.separator(h=10,style="none")
    cmds.separator(h=10,style="none")
    cmds.separator(h=10,style="none")

    
    
    cmds.button(label="Apply", command=applyCallback)
    cmds.button(label="Cancel", command=cancelCallBack) 
    

    
    
    cmds.showWindow()

createUi()


