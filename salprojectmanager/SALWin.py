import maya.cmds as cmds 
import pymel.core as pm
import os

import salCore

reload(salCore)

def __init__():
    print 'fffff'

class mainUI (object):
    ''' description '''
    
    _UiName= ''
    _pjName = ''
    pjPath = ''    
    __version__ = '1.0Alpha'
    
    def __init__(self):
        
        #print ('DEBUG|XML path : '+salCore.ENV_PATH.WORKINGSAPCE_PATH+' , '+salCore.ENV_PATH.XML_FILE_NAME )
        salCore.XML_mod().Check_XML_exists( 
                                           os.path.join(
                                                        salCore.ENV_PATH.WORKINGSAPCE_PATH,
                                                        salCore.ENV_PATH.XML_FILE_NAME 
                                                        )
                                           )
        re_prj = salCore.core().Load_recentProject()
        
        if len(re_prj) < 1:
            re_prj.append (0)
            re_prj.append('Plese select Project')
            re_prj.append('Project path')
            
        
        #print ('DEBUG|__init__|re_prj : '+ re_prj[0]+' , '+re_prj[1]+' , '+re_prj[2])
        
        self._UiName= 'ProjectManMainWindow'
        self._pjName = re_prj[1]
        self.pjPath = re_prj[2]
        self.pjID = re_prj[0]
        
        #print ('DEBUG|__init__|self.pjPath : '+self.pjPath)

    def get_recentProjectData(self):
        
        re_prj = salCore.core().Load_recentProject()
        if len(re_prj) < 1:
            re_prj.append (0)
            re_prj.append('Plese select Project')
            re_prj.append('<Project path>')
        self._pjName = re_prj[1]
        self.pjPath = re_prj[2]
        self.pjID = re_prj[0]
    
    def showUi(self):
        ''' Create SAL peoject manager main window '''
        
        if cmds.window( self._UiName, exists= True ):
            cmds.deleteUI( self._UiName, window = True )
        
        #Check recent project are exists
        if os.path.exists(self.pjPath) is not True:
            self.pjPath = '<Project path>'
                
        cmds.window( self._UiName,title=':: Shape And Light - Project Manager :: V.'+str(self.__version__))
        cmds.columnLayout( adjustableColumn = True)
        cmds.rowLayout( numberOfColumns=2, adjustableColumn=1, columnAlign=(1, 'left') )

        cmds.text('projectNameText',l='Project name : ' + self._pjName,font='boldLabelFont')
        
        #Header
        cmds.button(
                    l='...', 
                    c = loadProjectwin().showUi
                    );
        cmds.setParent('..')
        cmds.text ( 
                   'projectPathText',
                   l='PATH : '+ self.pjPath,
                   align='left'
                   );
        cmds.separator(h=10)
        cmds.setParent('..')
        
        #Text Scollinglist
        cmds.columnLayout(adj=True)
        cmds.textScrollList('scollSceneFiles',numberOfRows=30)
        cmds.setParent('..')
        
        # Confirm button
        cmds.columnLayout(adj=True)
        cmds.button(l="OPEN",
                     c=self.openButton_onclick
                     );
        cmds.button(l="CLOSE",
                     c=self.closeButton_onClick
                     );
        cmds.setParent('..')
        
        self.sceneList_update()
        
        #Show UI
        cmds.showWindow(self._UiName)
        
    def closeButton_onClick(self, *args):
        cmds.deleteUI( self._UiName, window = True )
    
    def openButton_onclick(self, *args):
        selectedfile = cmds.textScrollList('scollSceneFiles', query=True, selectItem=True)
        filepath = cmds.workspace(query=True,rd=True)+'scenes/'+selectedfile[0]
        
        fileCheckState = cmds.file(q=True, modified=True)

        # if there are, save them first ... then we can proceed 
        if fileCheckState:
            print 'Need to save.'
            confAnswer = cmds.confirmDialog( 
                title='Confirm', 
                message='Save this project?', 
                button=['Yes','No'], 
                defaultButton='Yes', 
                cancelButton='No', 
                dismissString='No' )

            if str(confAnswer) == 'Yes' :
                # This is maya's native call to save, with dialogs, etc.
                # No need to write your own.
                cmds.SaveScene()
            else:
                cmds.file( filepath, o=True, f=True )
        else:
            print 'No new changes, proceed.'

        cmds.file( filepath, o=True )
        print ("DEBUG|Open file : "+selectedfile[0])
    
    def sceneList_update(self):
        
        if self.pjPath is not 'Project path' :
            self.get_recentProjectData()
            
        #print ("DEBUG|scene update|Project path :"+self.pjPath)
        #Get scene file
        fileIndex = 0
        
        if os.path.exists(os.path.join(self.pjPath,'scenes')) is True:
            myScenefile = os.listdir(os.path.join(self.pjPath,'scenes'))
            #Filter only scene file.
            for myfile in myScenefile:
                if os.path.isfile(os.path.join(self.pjPath,'scenes',myfile)) is not True :
                    myScenefile.pop(fileIndex)
                fileIndex += 1
                
            if len(myScenefile)<1:
                myScenefile = ['no scene file in <scenes> folder']
        else:
            myScenefile = 'no <scenes> folder'
        
        cmds.textScrollList('scollSceneFiles',edit=True, removeAll=True )
        cmds.textScrollList('scollSceneFiles',edit=True, append = myScenefile )
        
        return myScenefile
        
class loadProjectwin(object) :
    ''' description '''
    
    _UiName =''
    _myMayaPath =''
    _myMayaProjectID = {}
    
    def __init__(self,*args):
        self._myMayaPath = ''#salCore.ProjectManager_core().Load_mayaDir()
        self._UiName = 'myProjectLoaderWin'
    
    def showUi(self, *args):
        ''' pass '''
        
        if cmds.window( "myProjectLoaderWin", exists= True ):
            cmds.deleteUI( "myProjectLoaderWin", window = True ) 
            
        cmds.window(self._UiName, title='Load Project Window')
        cmds.columnLayout(adjustableColumn=True)
        
        _myMayaPath = []
        _myMayaDict = salCore.core().Load_mayaDir()
        _mymayaID = {}
        
        i=0
        for key,value in _myMayaDict.items():
            #print ('key = '+str(key))
            #print ('Value = '+value)
            _myMayaPath.append(value)
            _mymayaID.update( {i:key} )
            i += 1
        
        self._myMayaProjectID = _mymayaID
        
        #Header
        cmds.textScrollList('ProjectName_TextScrollList',numberOfRows=30, append = _myMayaPath )
        
        #Project control Buttons
        cmds.rowLayout(numberOfColumns=5, adjustableColumn=1)
        cmds.button(
                    l="add new project",
                    c = self.add_newProject_on_click 
                    )
        cmds.button(l="remove project",
                    c=self.removeButton_onClick
                    )
        cmds.setParent('..')
        cmds.separator()
        cmds.setParent('..')
        
        #Confirm Buttons
        cmds.rowLayout(numberOfColumns=2, adjustableColumn=1)
        cmds.button(
                    l="Load project",
                     c=self.LoadprojectButton_onClick
                     );
        cmds.button(
                    l="CLOSE", 
                    c= self.closeButton_onClick
                    );
        cmds.setParent('..')
        
        #ShowUI
        cmds.showWindow(self._UiName)
    
    def add_newProject_on_click(self,*args):
        #show maya file browser
        print ("DEBUG|add_newProject_on_click : CLICK!!")
        Prj_Path = cmds.fileDialog2(fileMode=3,dialogStyle=2)
        
        #add project to XML database
        salCore.XML_mod().add_XML_project(name=raw_input(), path=Prj_Path,recentPrj=1)
        
    def LoadprojectButton_onClick(self, *args):
        
        _prjName = cmds.textScrollList('ProjectName_TextScrollList', query=True, selectItem=True)
        _prjSelectedIndex = cmds.textScrollList('ProjectName_TextScrollList', query=True, selectIndexedItem=True)
        
        _myMayaSceneID = str(self._myMayaProjectID[int( _prjSelectedIndex[0] )-1])
        
        #Set selected project to recent project
        salCore.XML_mod().xml_update_project( pjID = _myMayaSceneID )
        
        _myMayaDict = salCore.core().Load_recentProject()
        
        print ('DEBUG|LoadprojectButton_onClick| _myMayaDict : >> '+str(_myMayaDict))
        #print ('DEBUG|LoadprojectButton_onClick : Project ' + _prjName[0] + ' ID is ' + _myMayaSceneID + ' was load!!')
        
        
        confAnswer = cmds.confirmDialog( title='Confirm', message='Set selected project to working project?', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )

        if str(confAnswer) == 'Yes' :
            newpjPath = _myMayaDict[2]
            setPrjCmd = 'setProject "'+newpjPath+'"'
            print ('DEBUG|LoadprojectButton_onClick |setPrjCmd : '+setPrjCmd)
            pm.mel.eval(setPrjCmd)
            print ('DEBUG|LoadprojectButton_onClick | current work space  : '+cmds.workspace(query=True,rd=True))
            scenelist = mainUI().sceneList_update()s
        else :
            pass

        cmds.text('projectNameText', edit=True, l='Project name : ' +_prjName[0])
        cmds.text('projectPathText', edit=True, l='PATH : '+_myMayaDict[2] )
        cmds.textScrollList('scollSceneFiles',edit=True, removeAll=True )
        cmds.textScrollList('scollSceneFiles', edit=True, append = scenelist)
        cmds.deleteUI( self._UiName, window = True )
    
    def removeButton_onClick(self,*args):
        _prjName = cmds.textScrollList('ProjectName_TextScrollList', query=True, selectItem=True)
        _prjSelectedIndex = cmds.textScrollList('ProjectName_TextScrollList', query=True, selectIndexedItem=True)
        
        selectedID = str(self._myMayaProjectID[int( _prjSelectedIndex[0]-1 )])
        #print selectedID
        salCore.XML_mod().xml_delete_project(targetID=selectedID)

    def update_List ( *args):
        if cmds.window('myProjectLoaderWin',exists=True):
            myDir = salCore.core().Load_mayaDir()
            Prjname =[]
            for i ,j in myDir.items() : 
                Prjname.append(j)
            cmds.textScrollList('ProjectName_TextScrollList',edit=True, removeAll=True )
            cmds.textScrollList('ProjectName_TextScrollList',edit=True, append = Prjname )
    
    def closeButton_onClick(self, *args):
        cmds.deleteUI( self._UiName, window = True )
        

def main(*args) :
    appmainUI = mainUI()
    appmainUI.showUi()
#print (__file__)

