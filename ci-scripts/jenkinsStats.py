import sys      # arg
import re       # reg
import time     # sleep
import os
import subprocess
import time

class JenkinsStats:
    def __init__(self):
        self.url = ''
        self.jobName = ''
        self.nbDays = 1

    def doStatsOnJob(self):
        lastBuildId = subprocess.check_output('curl --silent ' + self.url + '/job/' + self.jobName + '/api/json | jq .lastBuild.number', shell=True, universal_newlines=True)
        lastBuildId = int(lastBuildId.strip())
        print('Last job ID was ' + str(lastBuildId))

        doLoop = True
        jobId = lastBuildId
        foundTodayMasterRun = False
        foundYesterdayMasterRun = False
        nbPullRequestJobs = 0
        nbSuccessFull = 0
        nbFailed = 0
        nbBypassJobs = 0
        duration = 0
        bypassDuration = 0
        fullDuration = 0
        waitLockDuration = 0
        todayMasterStatus = False
        todayMasterDuration = 0
        masterCount = 0
        masterDuration = 0

        while doLoop:
            print('Stats on job #' + str(jobId))
            subprocess.run('curl --silent ' + self.url + '/job/' + self.jobName + '/' + str(jobId) + '/api/json | jq . > jobsStats.json', shell=True)
            buildCause = subprocess.check_output('cat jobsStats.json | jq .actions[0].causes', shell=True, universal_newlines=True)
            if re.search('UpstreamCause', str(buildCause)) is not None:
                if not foundTodayMasterRun:
                    foundTodayMasterRun = True
                    status = subprocess.check_output('cat jobsStats.json | jq .result', shell=True, universal_newlines=True)
                    if re.search('SUCCESS', str(status)) is not None:
                        todayMasterStatus = True
                    jobDuration = subprocess.check_output('cat jobsStats.json | jq .duration', shell=True, universal_newlines=True)
                    jobDuration = int(jobDuration.strip())
                    todayMasterDuration = jobDuration / 1000
                    masterDuration = jobDuration / 1000
                elif not foundYesterdayMasterRun:
                    masterCount += 1
                    if masterCount == self.nbDays:
                        foundYesterdayMasterRun =  True
                        doLoop = False
                    else:
                        jobDuration = subprocess.check_output('cat jobsStats.json | jq .duration', shell=True, universal_newlines=True)
                        jobDuration = int(jobDuration.strip())
                        masterDuration += jobDuration / 1000
            elif (re.search('GhprbCause', str(buildCause)) is not None) and foundTodayMasterRun:
                nbPullRequestJobs +=1
                status = subprocess.check_output('cat jobsStats.json | jq .result', shell=True, universal_newlines=True)
                if re.search('SUCCESS', str(status)) is not None:
                    nbSuccessFull += 1
                else:
                    nbFailed += 1
                jobDuration = subprocess.check_output('cat jobsStats.json | jq .duration', shell=True, universal_newlines=True)
                jobDuration = int(jobDuration.strip())
                duration += (jobDuration / 1000)
                lockTime = subprocess.check_output('curl --silent ' + self.url + '/job/' + self.jobName + '/' + str(jobId) + '/console | grep CI-Orion-Build-Sanity-Check-Deploy-Test', shell=True, universal_newlines=True)
                for lockLine in str(lockTime).split('\n'):
                    if re.search('Trying to acquire lock on', lockLine) is not None:
                        ret = re.search('<b>(?P<timestamp>[0-9:]+)</b>', lockLine)
                        if ret is not None:
                            timestamp = ret.group('timestamp')
                            lockStart = time.strptime(timestamp, "%H:%M:%S")
                    if re.search('Lock acquired on', lockLine) is not None:
                        ret = re.search('<b>(?P<timestamp>[0-9:]+)</b>', lockLine)
                        if ret is not None:
                            timestamp = ret.group('timestamp')
                            lockEnd = time.strptime(timestamp, "%H:%M:%S")
                            lockDuration = time.mktime(lockEnd) - time.mktime(lockStart)
                            waitLockDuration += lockDuration
                            jobDuration -= (lockDuration * 1000)
                # if job ran for less than 90 seconds, it is certainly a bypass
                if jobDuration < 90000:
                    nbBypassJobs += 1
                    bypassDuration += (jobDuration / 1000)
                else:
                    fullDuration += (jobDuration / 1000)
            jobId = subprocess.check_output('cat jobsStats.json | jq .previousBuild.number', shell=True, universal_newlines=True)
            jobId = int(jobId.strip())

        print ('---------------------------------------------------------')
        print ('Statistics on       = ' + str(self.nbDays) + ' last day(s)')
        print ('---------------------------------------------------------')
        print ('nbPullRequestJobs   = ' + str(nbPullRequestJobs))
        print ('nbSuccessFul        = ' + str(nbSuccessFull))
        print ('nbFailed            = ' + str(nbFailed))
        print ('nbBypassJobs        = ' + str(nbBypassJobs))
        print ('---------------------------------------------------------')
        duration = duration + masterDuration
        print ('Full Usage          = ' + ('%.1f' % duration) + ' seconds (' + ('%.1f' % (duration/3600)) + ' hours)')
        print ('Wait Usage          = ' + ('%.1f' % waitLockDuration) + ' seconds (' + ('%.1f' % (waitLockDuration/3600)) + ' hours)')
        waitLockDuration = int(waitLockDuration)
        print ('Real Usage          = ' + ('%.1f' % ((duration-waitLockDuration)/(3600))) + ' hours (Rate = ' + ('%.1f' % ((100*(duration-waitLockDuration))/(3600*24*self.nbDays))) + '%)')
        print ('---------------------------------------------------------')
        print ('Bypass Avg Duration = ' + ('%.1f' % (bypassDuration/nbBypassJobs)) + ' seconds')
        print ('Full   Avg Duration = ' + ('%.1f' % (fullDuration/(nbPullRequestJobs-nbBypassJobs))) + ' seconds')
        print ('                    = ' + ('%.1f' % (fullDuration/((nbPullRequestJobs-nbBypassJobs)*60))) + ' minutes')
        print ('---------------------------------------------------------')
        if todayMasterStatus:
            print ('Today Master Check  = SUCCESS')
        else:
            print ('Today Master Check  = FAILURE')
        print ('Today Master Time   = ' + ('%.1f' % (todayMasterDuration/60)) + ' minutes')

#--------------------------------------------------------------------------------------------------------
#
# Start of main
#
#--------------------------------------------------------------------------------------------------------

STATS = JenkinsStats()
STATS.url = 'https://jenkins-oai.eurecom.fr'
STATS.jobName = 'MAGMA-MME-production'

STATS.doStatsOnJob()
