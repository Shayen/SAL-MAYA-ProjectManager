import xml.etree.ElementTree as ET
import maya.cmds as cmds
import os
from sets import Set

from salprojectmanager.SALWin import loadProjectwin

class core(object):
    ''' pass '''
    
    def __init__(self):
        pass
    
    def maya_ConfirmDialog(self,title='Confirm Dialog',message='Are you sure?'):
        ''' Create custom confirm dialog template '''
        
        _tempConfDialog = cmds.confirmDialog( 
                               title=title, 
                               message=message, 
                               button=['Yes','No'], 
                               defaultButton='Yes', 
                               cancelButton='No', 
                               dismissString='No' 
                               )
        return _tempConfDialog

    def Load_recentProject(self):
        
        xml_path = os.path.join( ENV_PATH.WORKINGSAPCE_PATH, ENV_PATH.XML_FILE_NAME )
        
        #print ('DEBUG: XAML path = '+xml_path)
        
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        recentProject=[]
        for project in root.findall('project'):
            myid = project.find('recent').text
            path = project.find('path').text
            name = project.get('name')
            if myid == 'yes':
                recentProject.append(myid)
                recentProject.append(name)
                recentProject.append(path)
                
        return (recentProject)
    
    def Load_mayaDir ( self ):
        
        ''' Load only maya folder in requied directory. '''
        
        #Connect XML database
        xml_path = os.path.join(ENV_PATH.WORKINGSAPCE_PATH,ENV_PATH.XML_FILE_NAME)
        root = ET.parse(xml_path)
              
        MAYA_myProject={}
        
        for project in root.iter('project') :
            name = project.get('name')
            pjID = project.find('id').text
            #print ('>>>'+str(name))
            MAYA_myProject.update( {int(pjID):name} )
            
        return (MAYA_myProject)

class ENV_PATH:
    
    WORKINGSAPCE_PATH_tmp = os.path.dirname(os.path.abspath(__file__))
    WORKINGSAPCE_PATH = WORKINGSAPCE_PATH_tmp.replace('\\','/')
    XML_FILE_NAME = 'ProjectDB.xml'
    
    def __init__(self):
        pass;

class XML_mod (object):
    ''' pass '''
    
    def __init__(self, *args):
        pass;
    
    def Check_XML_exists (self,XML_PATH=''):
        '''  check XML database file exists? '''
        
        
        #print ('DEBUG|XML_PATH : '+XML_PATH)    
        if len(XML_PATH)< 1:
            cmds.error("\'XML_PATH\' NOT SET!!")
        
        if os.path.exists(XML_PATH)!= True:
            
            #cmds.error("\'XML_PATH\' ERROR Please check \'XML_PATH\' or your xml file")
            tempConfDialog = core().maya_ConfirmDialog( 
                               title='Cannot find you Project database file', 
                               message='You want to create new XML file in current directory?')
            
            if tempConfDialog == 'Yes':
                self.Create_XMlfile()
               
        else :
            pass;
        
        return XML_PATH;

    def Create_XMlfile(self,*args):
        ''' Create new XML file in Working directory as database '''
        
        filename = ENV_PATH.XML_FILE_NAME
        filename_tmp = ''
        
        if os.path.exists( os.path.join(ENV_PATH.WORKINGSAPCE_PATH, filename) ) is True:
            count = 1
            file_newname = ''
            
            while (os.path.exists(os.path.join(ENV_PATH.WORKINGSAPCE_PATH, filename)) == True ):
                print ('DEBUG|Create_XMlfile : '+os.path.join(ENV_PATH.WORKINGSAPCE_PATH, filename)+ " is exists")
                file_newname = filename+str(count)
                count = count+1
                filename_tmp = file_newname
                
            filename = filename_tmp
        print ('Create_XMlfile|tmp : '+os.path.join(ENV_PATH.WORKINGSAPCE_PATH, filename + '.xml'))
        print ('Create_XMlfile|filename :'+ENV_PATH.XML_FILE_NAME)
        tmp = open(os.path.join(ENV_PATH.WORKINGSAPCE_PATH, filename),'a')
        tmp.write('<data>\n</data>')
        tmp.close()
        
        #add new Project
        #self.add_XML_project(name=raw_input(),path=cmds.fileDialog2(fileMode=3,dialogStyle=2,caption = 'select project'),recentPrj=1)
        #set to recent project
        
    def add_XML_project(self,path,name='default',recentPrj=0):
        ''' Add new project to database '''
        
        if len(path)<1 :
            cmds.error('Path not set')
        else :            
            path= path[0]
            
        if len(name)<1:
            cmds.error('name not set')
               
        xml_path = os.path.join(ENV_PATH.WORKINGSAPCE_PATH,ENV_PATH.XML_FILE_NAME)
        print ('------------------------------------------')
        print ('DEBUG|XML_MOD.add_XML_project.xml_path : ' +xml_path)
        #XML file parsing...
        tree = ET.parse(xml_path)
        root = tree.getroot()
              
        #Prepare variable for loop   
        id_list = []
        
        #Loop for get all id in XML find for finding gap
        for myID in root.iter('id'):
            #print ('DEBUG|add_XML_project|myID.text : '+myID.text)
            id_list.append(myID.text)
            
        if len(id_list) > 1 :
            #Sorting id and fill id gap
            #technique use: Set() compare
            id_list = sorted(id_list)
            id_list = map(int, id_list)
    
            a = range(1, id_list[len(id_list)-1]+1 ) 
            a= Set(a)
            set_id = Set(id_list)
            tmp =list(a-set_id) # find what difference between range and id list gaped.
            
            
            if len(tmp)<1:
                myID = id_list[(len(id_list)-1)]+1
            else :
                myID = tmp[0]
            #print ('DEBUG|add_XML_project : '+a+' , '+set_id+' , '+tmp+' , '+myID)
            #------------------
                
            #print ('DEBUG|add_XML_project : project ID added>> '+ str(myID))
        else :
            myID = '0'
        
        #Adding data to XML file
        project = ET.Element('project')
        project.set('name', name)
        root.append(project)
        prj_id = ET.SubElement(project,'id' )
        prj_id.text = str(myID)
        prj_path = ET.SubElement(project,'path')
        prj_path.text = path
        prj_recent = ET.SubElement(project,'recent')
        if recentPrj == 1 :
            
            for project in tree.findall('project'):
                for myRecentStatus in project.findall('recent') :                    
                    if myRecentStatus.text == 'yes':
                        myRecentStatus.text = 'no'
                        
            prj_recent.text = 'yes'
        else :
            prj_recent.text = 'no'
        tree.write(xml_path)
        
        #print ('DEBUG|XML updated : '+xml_path)
        
        loadwin = loadProjectwin()
        loadwin.update_List()
    
    def xml_delete_project(self,targetID):
        xml_path = os.path.join(ENV_PATH.WORKINGSAPCE_PATH,ENV_PATH.XML_FILE_NAME)
        tree = ET.parse(xml_path)
        root = tree.getroot()

        for project in tree.findall('project'):
            for myID in project.findall('id') :
                myIDvale = int(myID.text)

                if myIDvale == int(targetID):
                    print ('DEBUG|delete : '+project.get('name'))
                    root.remove(project)
        tree.write(xml_path)

        loadwin = loadProjectwin()
        loadwin.update_List()

    def xml_update_project(self,pjID):
        ''' description '''
        
        xml_path = os.path.join(ENV_PATH.WORKINGSAPCE_PATH,ENV_PATH.XML_FILE_NAME)
        #print ('------------------------------------------')
        #XML file parsing...
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        for projectRecentStatus in root.iter('recent'):
            #print str(projectRecentStatus.text)
            if projectRecentStatus.text == 'yes':
                projectRecentStatus.text = 'no'
                #print ('DEBUG : set old recent project to <no>')
        
        for project in tree.findall('project'):
            for myID in project.findall('id') :
                myIDvalue = int(myID.text)
                
                if int(myIDvalue) == int(pjID):
                    #print ('DEBUG : '+str(myID.text)+' was matched !!')
                    for recent in project.findall('recent'):
                        recent.text = 'yes'                     
                    
        
        tree.write(xml_path)
         
if __name__ == '__main__':
    pass