import os
import pandas as pd
import numpy as np
os.chdir('/Users/aneeshks/Documents/BAO/Analysis/InfectedDevices') 

#colnames=['Site', 'Devices', 'Requests'] 
#sourceDataDF = pd.read_csv('part-00000-286f9ccd-2a22-4dff-ae22-dde414e74649-c000.csv', sep='\t', names=colnames, header=None)

sourceDataDF = pd.read_csv('part-00000-22d3fd2e-0506-4bfe-9552-144ddefada49-c000.csv', sep='\t')
print(sourceDataDF.shape)
sourceDataDF.head(2)



OutPutdata = pd.DataFrame([])
Index = 0
#sourceDataDF.Site.unique()
Sites = ['abc.com','xyz.com']

for featSites in Sites:
    Index = Index + 1
    ListExclude = []
    
    ListExclude.append(featSites)     
    TotalUniSits = len(sourceDataDF.Site.unique())
    VarSourceDataSiteDF = []
    VarSourceDataSiteDF = sourceDataDF[sourceDataDF['Site'] == featSites]
    
    SummaryVarSourceDataSiteDF = []
    SummaryVarSourceDataSiteDF = pd.DataFrame(VarSourceDataSiteDF
                                          .groupby('Site')
                                          .agg({'Devices':'count'})
                                          .reset_index()    
                                          .rename(columns={'Devices':'TotalDevices'})
                                        )
 
    SummaryVarSourceDataSiteDF['NewDeviceAddition'] = 0
    SummaryVarSourceDataSiteDF['ParentSite'] = featSites
    SummaryVarSourceDataSiteDF['Score'] = 0
    SummaryVarSourceDataSiteDF['TotalDeviceSet'] = len(VarSourceDataSiteDF.Devices.unique())
    SummaryVarSourceDataSiteDF['CommonDevices'] = len(VarSourceDataSiteDF.Devices.unique())
   
    VarSiteUniqDev = []
    VarSiteUniqDev = VarSourceDataSiteDF.Devices.unique() 
    OutPutdata = OutPutdata.append(SummaryVarSourceDataSiteDF) 

    if len(sourceDataDF[sourceDataDF['Devices'].isin(VarSiteUniqDev)].Site.unique()) > 100:
        numRelatedSites = len(sourceDataDF[sourceDataDF['Devices'].isin(VarSiteUniqDev)].Site.unique())
    else: numRelatedSites = len(sourceDataDF[sourceDataDF['Devices'].isin(VarSiteUniqDev)].Site.unique())  
    
    SaveStore = 100
    DevStaticStart = SummaryVarSourceDataSiteDF["TotalDevices"]     

    for k in range(1, numRelatedSites):         
        print("Loop1-", Index, TotalUniSits, "Loop2-", k, numRelatedSites)
        
        VarAllSitesKnowDev =  sourceDataDF[sourceDataDF['Devices'].isin(VarSiteUniqDev)]
        VarAllSitesUnKnowDev =  sourceDataDF[~sourceDataDF['Devices'].isin(VarSiteUniqDev)]
        VarSummaryAllSitesKnowDev = pd.DataFrame(VarAllSitesKnowDev
                                              .groupby('Site')
                                              .agg({'Devices':'count'})
                                               .reset_index()
                                              .rename(columns={'Devices':'TotalDevices'})
                                            )
        VarSummaryAllSitesUnKnowDev = pd.DataFrame(VarAllSitesUnKnowDev
                                              .groupby('Site')
                                              .agg({'Devices':'count'})
                                              .reset_index()
                                              .rename(columns={'Devices':'TotalDevices'})
                                            )
        VarSummaryJoined = VarSummaryAllSitesKnowDev.merge(VarSummaryAllSitesUnKnowDev, left_on='Site', right_on='Site', how='left')
        VarSummaryJoined = VarSummaryJoined.rename(index=str, columns={"TotalDevices_x": "CommonDevices", "TotalDevices_y": "NewDeviceAddition"})
        VarSummaryJoined = VarSummaryJoined.fillna(0)
        VarSummaryJoined = VarSummaryJoined[~VarSummaryJoined['Site'].isin(ListExclude)]
        Tempdata = pd.DataFrame([])
        OutTemp = pd.DataFrame([])
        VarClosestSite = []

        if len(VarSummaryJoined) > 1000:
            VarnumRelatedSites = len(VarSummaryJoined) 
        else: VarnumRelatedSites = len(VarSummaryJoined)  
    
        for i in range(0, VarnumRelatedSites):
            Num = DevStaticStart + VarSummaryJoined["NewDeviceAddition"][i] 
            Den = DevStaticStart  + VarSummaryJoined["CommonDevices"][i] + VarSummaryJoined["NewDeviceAddition"][i]
            score = Num*100.00/Den
            perc = 100*VarSummaryJoined["CommonDevices"][i]/(VarSummaryJoined["NewDeviceAddition"][i] + VarSummaryJoined["CommonDevices"][i])
            Tempdata = Tempdata.append(pd.DataFrame({
                'Site': VarSummaryJoined["Site"][i],
                'Score': score,
                'perc': perc,
                'NewDeviceAddition':VarSummaryJoined["NewDeviceAddition"][i],
                'CommonDevices':VarSummaryJoined["CommonDevices"][i],
                'DevStaticStart': DevStaticStart
            }))
            
        VarClosestSite = Tempdata[Tempdata['perc'] == Tempdata["perc"].max()]["Site"]
        
        if len(VarClosestSite) == 1: VarClosestSiteFirst = VarClosestSite[0]
        else: VarClosestSiteFirst = list(VarClosestSite[0])[1]
    
        if len(VarClosestSite) > 0:  
            ListExclude.append(VarClosestSiteFirst)
            OutTemp = VarSummaryJoined[VarSummaryJoined['Site'] == VarClosestSiteFirst]  
            OutTemp['Score'] = Tempdata[Tempdata['Site'] == VarClosestSiteFirst]["perc"][0]
            OutTemp['ParentSite'] = featSites
            OutTemp['NewDeviceAddition'] = Tempdata[Tempdata['Site'] == VarClosestSiteFirst]["NewDeviceAddition"][0]
            OutTemp['CommonDevices'] = Tempdata[Tempdata['Site'] == VarClosestSiteFirst]["CommonDevices"][0]
            OutTemp['TotalDeviceSet'] = len(VarSiteUniqDev)
            OutPutdata = OutPutdata.append(pd.DataFrame(OutTemp)) 
            OutPutdata.fillna(0)
            SaveStore = Tempdata[Tempdata['Site'] == VarClosestSiteFirst]["perc"][0]
            VarSourceDataSiteDF_next = sourceDataDF[sourceDataDF['Site'].isin(ListExclude)]
            VarSiteUniqDev = VarSourceDataSiteDF_next.Devices.unique()
            DevStaticStart = DevStaticStart + Tempdata[Tempdata['Site'] == VarClosestSiteFirst]["NewDeviceAddition"]

        else: print("end")

    OutPutdata.to_csv("FileOut6Sites.csv", sep='\t',header=True, line_terminator='\n')
