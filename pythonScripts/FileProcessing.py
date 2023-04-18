import pythonScripts.mongodb as mongodb
import numpy
import pythonScripts.product as product
import pythonScripts.Config as Config

def getComponent(row):
        requirementList=[]
        trimmed=str(numpy.char.strip(row))[2:].split(' (')
        component=trimmed.pop(0).split('\\')
        component.pop(0)

        for s in trimmed:        
            m = s[s.find('Requirement'):s.find(')')]
            product.requirementList.append(m) 
        if product.product == "CPES" or product.product == "MWPS":      
            component.pop(0)
            
        if row.find("Web Site") != -1 or row.find("WebSite") != -1:
             product.componentType=component[0]
        else:
            #component.pop(0)
            product.component=component[1].split(' ')[0]
            product.componentType=component[0]      
        return

def getPrerequisites(row):
     product.prerequisites=row.split(' (')[0]
     prerequisitesFLAG="false"
     return

def getScript(row):
        trimmed=numpy.char.strip(row)
        script=str(trimmed).lstrip('- ')
        product.script=script.split('sql')[0]+'sql'
        if row.find("multiple use") != -1:
             product.scriptMultipleUse="true"
        return



def insertDND(wid):
    mongodb.insert(wid)
    return

def generateDict(workItem,workItemTitle,productName,
                 component,componentType,release,database,
                 script,scriptMultipleUse,newService,
                 prerequisites,requirementList,
                 config,keys):
    workItemDict= {
        "work item": workItem,
        "work item title": workItemTitle,
        "product": productName,
        "component": component,
        "component type": componentType,
        "release": release,
        "database": database,
        "script": script,
        "scriptMultipleUse": scriptMultipleUse,
        "newService": newService,
        "prerequisites": prerequisites,
        "requirementList": requirementList,
        "config": config,
        "keys": keys
    }
    return workItemDict

def getConfig(row):
    Config.keys.append(row)
    product.componentType="configuration"
    print("KEYYYSSSSSS\n",Config.keys)

    workItemDict=generateDict(product.workItem,product.workItemTitle,
                                              product.product,product.component,
                                              product.componentType,product.release,
                                              product.database,product.script,
                                              product.scriptMultipleUse,product.newService,
                                              product.prerequisites,product.requirementList,
                                              Config.flag,Config.keys)
    insertDND(workItemDict)
    return

product.workItem = '197560'#212960'
workItemExists=False
prerequisitesFLAG="false"
OpenRelease=0

with open(r'D:\Backyard\Automation\Documentation\CPES_Release notes-Auto.txt', 'r') as releseNotes:
    releaseLines = releseNotes.readlines()

    for releaseRow in releaseLines:     
        if releaseRow.find("Release notes of version Number") != -1:
             OpenRelease+=1
             if OpenRelease > 1:
                  break
             product.release=releaseRow.split(' ')[5].rstrip()

        if releaseRow.find(product.workItem) != -1:
            product.workItemTitle=releaseRow.lstrip()[2:-1]
            workItemExists=True

            updateNotes=open(r'D:\Backyard\Automation\Documentation\CPES_Update-Auto.txt', 'r')
            updateLines=updateNotes.readlines()

            OpenUpdate=0
            for updateRow in updateLines:               
                if updateRow.find("Update from version") != -1:
                    OpenUpdate+=1
                    if OpenUpdate > 1:
                        break
                if updateRow.find('Pre-requisites') != -1:
                     prerequisitesFLAG="true"

                elif updateRow.find(product.workItem) != -1:
                    product.componentPath=updateRow #Clean here
                    product.product="CPES"
                    Config.flag="false"
                    product.newService="false"

                    if updateRow.find("New Service") != -1:
                         product.newService="true"

                    if updateRow.find("Application\\") !=- 1:
                        getComponent(updateRow)
                    elif prerequisitesFLAG=="true":
                        getPrerequisites(updateRow)
                    if updateRow.find("Kindly add") != -1 or updateRow.find("Kindly change") != -1:
                        configHead=numpy.char.strip(updateRow.split(' '))[1:]
                        print('CURRENT:',configHead)
                        if any(product.workItem for x in configHead):
                            Config.flag="true"
                            continue
                        else:
                            Config.flag="false"
                            continue                         
                    else:
                        product.component=""
                        product.componentType=""
                        product.scriptMultipleUse="false"
                        getScript(updateRow)
           
                    workItemDict=generateDict(product.workItem,product.workItemTitle,
                                              product.product,product.component,
                                              product.componentType,product.release,
                                              product.database,product.script,
                                              product.scriptMultipleUse,product.newService,
                                              product.prerequisites,product.requirementList,
                                              Config.flag,Config.keys)
                    insertDND(workItemDict)

                elif updateRow.find("RUN the below Script") != -1:
                        if updateRow.split(' ')[6] == "All":
                            product.database=updateRow.split(' ')[7]
                        else:
                            product.database=updateRow.split(' ')[6]

                elif updateRow.find("add key") != -1 and Config.flag == "true":
                     getConfig(updateRow)
                     print("CONFIG:",updateRow)
                                                      
                prerequisitesFLAG="false"



    if workItemExists==False:
        print("New Work Item")
            #Add work item       