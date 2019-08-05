# SolidFire volume moving simuration
# v0.1 Kensuke Maeda 2019/06/10
# v0.2 Kensuke Maeda 2019/06/17
#
# Usage
# 1.) Access to Active IQ(SolidFire)
#   https://activeiq.solidfire.com/
# 2.) Download csv file.
#     [Select a Cluster]tab -> Click my cluster name -> [Drives] -> Click [Excel Export] Icon
# 3.) Download json files.
#     [Reporting] -> [API Collection] -> Download json of [ListISCSISessions] and [ListVolumeStatsByVolume]
# 4.) Execute this script
#   Usage : 
#     python <Script name>.py <Drives.csv> <ListISCSISessions.json> <ListVolumeStatsByVolume.json>

import json
import pandas as pd
import sys

args = sys.argv

file_drivelist = args[1]
file_listiscsisessions = args[2]
file_listvolstats = args[3]

df = pd.read_csv(file_drivelist,usecols=['Node ID','Service ID'])
f = open(file_listvolstats,'r')
json_dict = json.load(f)
psvlist = []

for json_key in json_dict['volumeStats']:
        primarydfloc = df.loc[df['Service ID'] == json_key['metadataHosts']['primary'],'Node ID']
        secondarydfloc = df.loc[df['Service ID'] == json_key['metadataHosts']['liveSecondaries'][0],'Node ID']
        psvjson = {'primaryNodeID':int(primarydfloc.values),'secondaryNodeID':int(secondarydfloc.values),'volumeID':json_key['volumeID']}
        psvlist.append(psvjson)

psvdf = pd.io.json.json_normalize(psvlist)
pscountdf = psvdf.groupby(['primaryNodeID','secondaryNodeID']).size().reset_index(name='counts')
pcountdf = psvdf.groupby(['primaryNodeID']).size().reset_index(name='VolCountBeforeUpgrade')
movevoldict = {}
for index1, row1 in pcountdf.iterrows():
    rowname = str(row1['primaryNodeID'])
    movevoldict.update({rowname:{}})
    for index2, row2 in pcountdf.iterrows():
        if row1['primaryNodeID'] == row2['primaryNodeID']:
            volcount = 0
        else:
            movecountdf = pscountdf.loc[(pscountdf['primaryNodeID'] == row2['primaryNodeID']) & (pscountdf['secondaryNodeID'] == row1['primaryNodeID'])]
            if len(movecountdf.index) == 0:
                    volcount = row1['VolCountBeforeUpgrade']
            else:
                    volcount = row1['VolCountBeforeUpgrade'] + movecountdf['counts']
        nodename = str(row2['primaryNodeID'])
        movevoljson = {nodename:int(volcount)}
        movevoldict[rowname].update(movevoljson)

movevoldictdf = pd.read_json(json.dumps(movevoldict))
movevoldictdf2 = movevoldictdf.sort_index(ascending=True)
movevoldictdf3 = movevoldictdf2.sort_index(axis=1,ascending=True)

print '------VolumeCountBeforeUpgrade------'
print pcountdf
print '------All Volumes------'
print movevoldictdf3.T
print '-----------------------'


##############

f2 = open(file_listiscsisessions,'r')
iscsidict = json.load(f2)
actvolid = []

for json_key in iscsidict['sessions']:
        actvolid.append(json_key['volumeID'])

actvolid_uq = list(set(actvolid))
actvoldf = pd.DataFrame(actvolid_uq,columns=['volumeID'])

actpsvoldf = psvdf[psvdf['volumeID'].isin(actvoldf['volumeID'])]


pscountdf = actpsvoldf.groupby(['primaryNodeID','secondaryNodeID']).size().reset_index(name='counts')
pcountdf = actpsvoldf.groupby(['primaryNodeID']).size().reset_index(name='VolCountBeforeUpgrade')
movevoldict = {}
for index1, row1 in pcountdf.iterrows():
    rowname = str(row1['primaryNodeID'])
    movevoldict.update({rowname:{}})
    for index2, row2 in pcountdf.iterrows():
        if row1['primaryNodeID'] == row2['primaryNodeID']:
            volcount = 0
        else:
            movecountdf = pscountdf.loc[(pscountdf['primaryNodeID'] == row2['primaryNodeID']) & (pscountdf['secondaryNodeID'] == row1['primaryNodeID'])]
            if len(movecountdf.index) == 0:
                    volcount = row1['VolCountBeforeUpgrade']
            else:
                    volcount = row1['VolCountBeforeUpgrade'] + movecountdf['counts']
        nodename = str(row2['primaryNodeID'])
        movevoljson = {nodename:int(volcount)}
        movevoldict[rowname].update(movevoljson)

movevoldictdf = pd.read_json(json.dumps(movevoldict))
movevoldictdf2 = movevoldictdf.sort_index(ascending=True)
movevoldictdf3 = movevoldictdf2.sort_index(axis=1,ascending=True)

print '------ActiveIOVolumeCountBeforeUpgrade------'
print pcountdf
print '------ActiveIOVolumes------'
print movevoldictdf3.T
print '-----------------------'