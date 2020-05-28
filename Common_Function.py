import datetime as dt
import os
import re

import Configuration as conf

'''
 fetches player state and time from the input string Line.
'''
def get_State_And_Date(Line):
    reg = re.compile('.*Player Status = "(.+?)".*')
    state = reg.findall(Line)[0]
    reg = re.compile('\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d\.\d*')
    date = reg.findall(Line)[0]
    return(state, date)

'''
    Parses the input log file. 
    Print the following as summary: 
        1. No. of video start/stop/pause/buffering events. 
        2. Min/Max/Average stop/pause/buffering duration.
'''
def Parse_Log(File_Name):
    if not os.path.isfile(File_Name):
        print('File ' + File_Name + ' is not found')
        return
    Count = {}
    prestate = None
    predate = None
    duration = {'Ended' : [], 'Paused' : [], 'Buffering' : []}
    Timedict = {'Ended' : [], 'Paused' : [], 'Buffering' : []}
    with open(File_Name, 'r') as File:
        for Line in File:
            x = re.search('.*Player Status.*', Line)
            if(x):
                state, date = get_State_And_Date(Line)
                if(state in Count.keys()):
                    Count[state] += 1
                else:
                    Count[state] = 1
                if(prestate == None and predate == None):
                    prestate = state
                    predate = dt.datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
                else:
                    currentdate = dt.datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
                    if prestate == 'Ended':                        
                        differnce  = currentdate - predate
                        duration['Ended'].append(differnce)
                        Timedict['Ended'].append(predate)
                    if prestate == 'Paused':
                        differnce  = currentdate - predate
                        duration['Paused'].append(differnce)
                        Timedict['Paused'].append(predate)
                    if prestate == 'Buffering':
                        differnce  = currentdate - predate
                        duration['Buffering'].append(differnce)
                        Timedict['Buffering'].append(predate)
                    prestate = state
                    predate = currentdate
    for i in Count.keys():
        print('Number of ' + i + ' states are ' + str(Count[i]))
    for i in duration.keys():
        if(len(duration[i]) != 0):
            minmum = min(duration[i])
            min_index = duration[i].index(minmum)
            maximum = max(duration[i])
            max_index = duration[i].index(maximum)
            print('Minimum duration of ' + i + ' state is ' + str(minmum) + ' occured at ' + str(Timedict[i][min_index]))
            print('Maximum duration of ' + i + ' state is ' + str(maximum) + ' occured at ' + str(Timedict[i][max_index]))
            average_timedelta = sum(duration[i], dt.timedelta(0)) / len(duration[i])
            print('Average duration of ' + i + ' state is ' + str(average_timedelta))
        else:
            print("There is no record of " + i + " state")
