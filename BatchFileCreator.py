#-*- coding:utf-8 -*-

import maya.cmds as cmds
import os

def getSceneFilePath(fullPath):
	foreign = cmds.file(q = True, sceneName = True)
	native = os.path.normpath(foreign)
	fileName = os.path.basename(native)
	dotPos = fileName.rindex('.')
	baseName = fileName[:dotPos]
	
	if fullPath == 1:
		return native
	else:
		return baseName
		
def getRenderExeFilePath():
	mayaloc = os.getenv('MAYA_LOCATION')
	addpath = '\\bin\\render.exe'
	renderpath = '"%s%s"'%(mayaloc, addpath)

	return renderpath

def getRenderDirectory():
	renderDirectory = cmds.textFieldGrp('directryTBG', query=True, text=True)
	return renderDirectory

def getFrameSE(frame):
    startF = int(cmds.getAttr("defaultRenderGlobals.startFrame"))
    endF = int(cmds.getAttr("defaultRenderGlobals.endFrame"))
    
    if frame == 1:
        return startF
    elif frame == 0:
        return endF
        
def getRenderL():
    return cmds.ls(type = "renderLayer")

def getRenderLayer():
    return  cmds.optionMenu("rendL",q=True,v=True)

def makeContent():
    content=''
    cbRend = cmds.checkBox("checkB",q=True,value=True)
    cbframeSE = cmds.checkBox("checkSE",q=True,value=True)
    cbframeS = cmds.textFieldGrp("startF",q=True,text=True)
    cbframeE = cmds.textFieldGrp("endF",q=True,text=True)
    
    if cbRend == True and cbframeSE == False:
        content = '%s -rl %s -rd %s %s\n' \
        %(getRenderExeFilePath(),getRenderLayer(),getRenderDirectory(), getSceneFilePath(1))
    elif cbframeSE == True and cbRend == False:
        content = '%s -s %s -e %s -rd %s %s\n' \
        %(getRenderExeFilePath(),cbframeS,cbframeE,getRenderDirectory(), getSceneFilePath(1))
    elif cbRend == True and cbframeSE == True:
        content = '%s -s %s -e %s -rl %s -rd %s %s\n' \
        %(getRenderExeFilePath(),cbframeS,cbframeE,getRenderLayer(),getRenderDirectory(), getSceneFilePath(1))
    elif cbRend == False or cbframeSE == False:
        content = '%s -rd %s %s\n' \
        %(getRenderExeFilePath(),getRenderDirectory(), getSceneFilePath(1))
    
    return content
	
def getDefaultPath(extend):
	fullPath = getSceneFilePath(1)
	baseName = getSceneFilePath(0)
	project = fullPath.split('scenes')

	if extend == 1:
		return '%s%s.bat'%(project[0],baseName)
	else:
		return '%simages'%(project[0])
			

def getBatchFilePath():
	batchPathDialog = cmds.fileDialog(mode=1, directoryMask='*.bat')
	batchPathTextBase = os.path.normpath(batchPathDialog)

	if not batchPathTextBase == ".":
		batchPathText = batchPathTextBase
	else:
		batchPathText = getDefaultPath(1)

	cmds.textFieldButtonGrp('batchPathTBG', edit=True, text=batchPathText)
	
def getDirectryPath():
	DirectryDialog = cmds.fileDialog2(fm=3,dir=getDefaultPath(0))
	if DirectryDialog != None:
	    DirectryTextBase = os.path.normpath(DirectryDialog[0])
    
	if not DirectryDialog == None:
		DirectryText = DirectryTextBase
	else:
		DirectryText = getDefaultPath(0)
		
	cmds.textFieldButtonGrp('directryTBG', edit=True, text=DirectryText)
	
def outputBatFile():
	path = cmds.textFieldButtonGrp('batchPathTBG', query=True, text=True)
	content = makeContent()

	f = open(path,'w+')
	f.write(content)
	f.close
	
def commandForCreateButton():
	title = u'BatchFileCreator'
	message = u'batchfile was made in the place that I appointed with a "BatchFile Path".'

	outputBatFile()

	cmds.confirmDialog(title=title, message=message, messageAlign='center', button='OK')

def editFormAttachments():
	cmds.formLayout('formLOT', edit=True,
		attachForm=[('batchPathTBG',     'top',    10),  ('batchPathTBG',   'left',  20),
			    ('directryTBG',    'top',    40),    ('directryTBG',  'left',  20),
			    ('createBTN',        'bottom', 10),  ('createBTN',      'left',  10),
			    ('closeBTN',         'bottom', 10),  ('closeBTN',       'right', 10),
			    ("rendL",            'top', 105 ),   ("checkB",         'top', 80 ),
			    ("checkB",         'left', 10 ),
			    ("rendL",            'left', 10 ),   ("checkSE",        'left', 280 ),
			    ("checkSE",          'top', 80 ),    ('startF',         'top', 103 ),
			    ('startF',           'left', 280 ),  ('endF',           'top', 103 ),
			    ('endF',             'left', 420 )],
		attachPosition=[('createBTN', 'right', 2, 50), ('closeBTN', 'left', 2, 50)])

def BatchFileCreatorUI():
    winName = u"BatchFileCreateWindow"
    
    if cmds.window(winName,exists = True):
        cmds.deleteUI(winName)
    cmds.window(winName,s=False,w=560,h=180)
    
    cmds.formLayout('formLOT')
    cmds.textFieldButtonGrp('batchPathTBG',label=u"BatchFile Path:",text=getDefaultPath(1),buttonLabel='...',buttonCommand='getBatchFilePath()')
    cmds.textFieldButtonGrp('directryTBG', label=u'RenderDirectory Path:', text=getDefaultPath(0),buttonLabel='...',buttonCommand='getDirectryPath()')
    
    rendL = cmds.ls(type="renderLayer")

    cmds.optionMenu("rendL",w=260,en=False)
    for i in range(len(rendL)):
        cmds.menuItem(label="%s"%(rendL[i]))
    
    visOnOption  = 'cmds.optionMenu("rendL",e=True,en=True)'
    visOffOption = 'cmds.optionMenu("rendL",e=True,en=False)'
    cmds.checkBox("checkB",label=u"RenderLayer",value=False,onCommand=visOnOption,offCommand=visOffOption)
    
    visOnFrame  = 'cmds.textFieldGrp("startF",e=True,en=True)+'+'cmds.textFieldGrp("endF",e=True,en=True)'
    visOffFrame = 'cmds.textFieldGrp("startF",e=True,en=False)+'+'cmds.textFieldGrp("endF",e=True,en=False)'
    cmds.checkBox("checkSE",label=u"Frame Range",value=False,onCommand=visOnFrame,offCommand=visOffFrame)
    cmds.textFieldGrp("startF",label=u"Start Frame :", text="%s" %getFrameSE(1),en=False, columnWidth2=(80,50))
    cmds.textFieldGrp("endF", label=u"End Frame :", text="%s" %getFrameSE(0),en=False, columnWidth2=(80,50))
    
    cmds.button('createBTN',label=u"Create",command="commandForCreateButton()")
    cmds.button('closeBTN',label=u'Close', command='cmds.deleteUI("%s")'%winName)
    
    editFormAttachments()
    cmds.showWindow()
BatchFileCreatorUI()
