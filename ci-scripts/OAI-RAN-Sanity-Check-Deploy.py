#/*
# * Licensed to the OpenAirInterface (OAI) Software Alliance under one or more
# * contributor license agreements.  See the NOTICE file distributed with
# * this work for additional information regarding copyright ownership.
# * The OpenAirInterface Software Alliance licenses this file to You under
# * the OAI Public License, Version 1.1  (the "License"); you may not use this file
# * except in compliance with the License.
# * You may obtain a copy of the License at
# *
# *       http://www.openairinterface.org/?page_id=698
# *
# * Unless required by applicable law or agreed to in writing, software
# * distributed under the License is distributed on an "AS IS" BASIS,
# * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# * See the License for the specific language governing permissions and
# * limitations under the License.
# *-------------------------------------------------------------------------------
# * For more information about the OpenAirInterface (OAI) Software Alliance:
# *       contact@openairinterface.org
# */
#---------------------------------------------------------------------

import os
import re
import sys
import subprocess
import time


CICD_PUBLIC_NETWORK_RANGE='192.168.61.64/26'

CICD_CASS_IP_ADDR='192.168.61.66'
CICD_HSS_PUBLIC_ADDR='192.168.61.67'
CICD_MME_PUBLIC_ADDR='192.168.61.68'
CICD_REDIS_PUBLIC_ADDR='192.168.61.69'
CICD_SPGWC_PUBLIC_ADDR='192.168.61.70'
CICD_SPGWU_PUBLIC_ADDR='192.168.61.71'
CICD_TRFGEN_PUBLIC_ADDR='192.168.61.72'

CICD_ENB_RF_SIM_PUBLIC_ADDR='192.168.61.80'
CICD_UE0_RF_SIM_PUBLIC_ADDR='192.168.61.90'

class deployWithOAIran:

    def __init__(self):

        self.action = 'None'
        self.tag = ''
        self.cli = ''
        res = subprocess.check_output('hostnamectl', shell=True, universal_newlines=True)
        result = re.search('Ubuntu|Red Hat', res)
        if result is not None:
            if result.group(0) == 'Red Hat':
                self.cli = 'sudo podman'
            elif result.group(0) == 'Ubuntu':
                self.cli = 'docker'
        else:
            sys.exit(-1)

    def createNetworks(self):
        # first check if already up?
        try:
            res = subprocess.check_output(self.cli + ' network ls | egrep -c "cicd-oai-public-net"', shell=True, universal_newlines=True)
            if int(str(res.strip())) > 0:
                self.removeNetworks()
        except:
            pass

        subprocess_run_w_echo(self.cli + ' network create --subnet ' + CICD_PUBLIC_NETWORK_RANGE + ' --ip-range ' + CICD_PUBLIC_NETWORK_RANGE + ' cicd-oai-public-net')

    def removeNetworks(self):
        try:
            subprocess_run_w_echo(self.cli + ' network rm cicd-oai-public-net')
        except:
            pass

    def deployCassandra(self):
        # first check if already up? If yes, remove everything.
        try:
            res = subprocess.check_output(self.cli + ' ps -a | grep -c "cicd-cassandra"', shell=True, universal_newlines=True)
            if int(str(res.strip())) > 0:
                self.removeAllContainers()
        except:
            pass

        subprocess_run_w_echo(self.cli + ' run --name cicd-cassandra --network cicd-oai-public-net --ip ' + CICD_CASS_IP_ADDR + ' -d -e CASSANDRA_CLUSTER_NAME="OAI HSS Cluster" -e CASSANDRA_ENDPOINT_SNITCH=GossipingPropertyFileSnitch --health-cmd "nodetool status" cassandra:2.1')
        # waiting for the service to be properly started
        doLoop = True
        while doLoop:
            try:
                res = subprocess.check_output(self.cli + ' exec cicd-cassandra /bin/bash -c "nodetool status"', shell=True, universal_newlines=True)
                rackFound = re.search('UN  ' + CICD_CASS_IP_ADDR, str(res))
                if rackFound is not None:
                    doLoop = False
            except:
                time.sleep(1)
                pass
        subprocess_run_w_echo(self.cli + ' exec cicd-cassandra /bin/bash -c "nodetool status" | tee archives/cassandra_status.log')
        subprocess_run_w_echo(self.cli + ' cp component/oai-hss/src/hss_rel14/db/oai_db.cql cicd-cassandra:/home')
        time.sleep(2)
        doLoop = True
        count = 0
        while doLoop and (count < 10):
            try:
                res = subprocess.check_output(self.cli + ' exec cicd-cassandra /bin/bash -c "cqlsh --file /home/oai_db.cql ' + CICD_CASS_IP_ADDR + '"', shell=True, universal_newlines=True)
                print(self.cli + ' exec cicd-cassandra /bin/bash -c "cqlsh --file /home/oai_db.cql ' + CICD_CASS_IP_ADDR + '"')
                doLoop = False
            except:
                time.sleep(2)
                count += 1
                pass
        if not doLoop:
            print ('Deployment Cassandra --> OK')
        else:
            print ('Problem deploying Cassandra')
            sys.exit(-1)

    def deployHSS(self):
        res = ''
        # first check if tag exists
        try:
            res = subprocess.check_output(self.cli + ' image inspect oai-hss:' + self.tag, shell=True, universal_newlines=True)
        except:
            sys.exit(-1)

        hssEnvFile = ''
        cwd = os.getcwd()
        if os.path.isfile(cwd + '/ci-scripts/oai-ran-sanity-check/hss.env'):
            hssEnvFile = './ci-scripts/oai-ran-sanity-check/hss.env'
        elif os.path.isfile(cwd + '/oai-ran-sanity-check/hss.env'):
            hssEnvFile = './oai-ran-sanity-check/hss.env'
        else:
            sys.exit(-1)

        subprocess_run_w_echo(self.cli + ' run --privileged --name cicd-oai-hss --network cicd-oai-public-net --ip ' + CICD_HSS_PUBLIC_ADDR + ' --env-file ' + hssEnvFile + ' --health-cmd "pgrep --count oai_hss" -d oai-hss:' + self.tag)

        count = 0
        runCount = 0
        status = False
        while (count < 10) and (runCount < 5):
            res = subprocess.check_output(self.cli + ' top cicd-oai-hss', shell=True, universal_newlines=True)
            if re.search('/openair-hss/bin/oai_hss -j /openair-hss/etc/hss_rel14.json --reloadkey true', str(res)):
                runCount += 1
                if runCount == 5:
                    status = True
            count += 1
            time.sleep(2)
        if status:
            print ('Deployment HSS --> OK')
        else:
            print ('Problem deploying HSS')
            sys.exit(-1)

    def deployRedis(self):
        redisConfFile = ''
        cwd = os.getcwd()
        if os.path.isfile(cwd + '/ci-scripts/oai-ran-sanity-check/redis_extern.conf'):
            redisConfFile = './ci-scripts/oai-ran-sanity-check/redis_extern.conf'
        elif os.path.isfile(cwd + '/oai-ran-sanity-check/redis_extern.conf'):
            redisConfFile = './oai-ran-sanity-check/redis_extern.conf'
        else:
            sys.exit(-1)

        subprocess_run_w_echo(self.cli + ' run --privileged --name cicd-redis --network cicd-oai-public-net --ip ' + CICD_REDIS_PUBLIC_ADDR + ' --volume ' + redisConfFile + ':/usr/local/etc/redis/redis.conf --health-cmd "redis-cli -h ' + CICD_REDIS_PUBLIC_ADDR + ' -p 6380 ping" -d redis:6.0.5 "/usr/local/etc/redis/redis.conf"')

        count = 0
        runCount = 0
        status = False
        while (count < 10) and (runCount < 5):
            res = subprocess.check_output(self.cli + ' top cicd-redis', shell=True, universal_newlines=True)
            if re.search('redis-server 192.168.61.69:6380', str(res)):
                runCount += 1
                if runCount == 5:
                    status = True
            count += 1
            time.sleep(2)
        if status:
            print ('Deployment REDIS --> OK')
        else:
            print ('Problem deploying REDIS')
            sys.exit(-1)

    def deployMME(self):
        res = ''
        # first check if tag exists
        try:
            res = subprocess.check_output(self.cli + ' image inspect magma-mme:' + self.tag, shell=True, universal_newlines=True)
        except:
            sys.exit(-1)

        mmeEnvFile = ''
        mmeEntrypoint = ''
        cwd = os.getcwd()
        if os.path.isfile(cwd + '/ci-scripts/oai-ran-sanity-check/mme.env'):
            mmeEnvFile = './ci-scripts/oai-ran-sanity-check/mme.env'
            mmeEntrypoint = './ci-scripts/oai-ran-sanity-check/mme-entrypoint.sh'
        elif os.path.isfile(cwd + '/oai-ran-sanity-check/mme.env'):
            mmeEnvFile = './oai-ran-sanity-check/mme.env'
            mmeEntrypoint = './oai-ran-sanity-check/mme-entrypoint.sh'
        else:
            sys.exit(-1)

        subprocess_run_w_echo(self.cli + ' run --privileged --name cicd-oai-mme --hostname mme --network cicd-oai-public-net --ip ' + CICD_MME_PUBLIC_ADDR + ' --volume ' + mmeEntrypoint + ':/magma-mme/bin/entrypoint.sh --env-file ' + mmeEnvFile + ' --entrypoint "/magma-mme/bin/entrypoint.sh" --health-cmd "pgrep --count oai_mme" -d magma-mme:' + self.tag)

        count = 0
        runCount = 0
        status = False
        while (count < 10) and (runCount < 5):
            res = subprocess.check_output(self.cli + ' top cicd-oai-mme', shell=True, universal_newlines=True)
            if re.search('/magma-mme/bin/oai_mme -c /magma-mme/etc/mme.conf', str(res)):
                runCount += 1
                if runCount == 5:
                    status = True
            count += 1
            time.sleep(2)
        if status:
            print ('Deployment MAGMA-MME --> OK')
        else:
            print ('Problem deploying MAGMA-MME')
            sys.exit(-1)

    def deployOldMME(self):
        res = ''
        # first check if tag exists
        try:
            res = subprocess.check_output(self.cli + ' image inspect oai-mme:' + self.tag, shell=True, universal_newlines=True)
        except:
            sys.exit(-1)

        mmeEnvFile = ''
        mmeEntrypoint = ''
        cwd = os.getcwd()
        if os.path.isfile(cwd + '/ci-scripts/oai-ran-sanity-check/mme-old.env'):
            mmeEnvFile = './ci-scripts/oai-ran-sanity-check/mme-old.env'
        elif os.path.isfile(cwd + '/oai-ran-sanity-check/mme-old.env'):
            mmeEnvFile = './oai-ran-sanity-check/mme-old.env'
        else:
            sys.exit(-1)

        subprocess_run_w_echo(self.cli + ' run --privileged --name cicd-oai-mme --hostname mme --network cicd-oai-public-net --ip ' + CICD_MME_PUBLIC_ADDR + ' --env-file ' + mmeEnvFile + ' -d  oai-mme:' + self.tag)

        time.sleep(1)
        subprocess_run_w_echo(self.cli + ' exec -d cicd-oai-mme /bin/bash -c "nohup tcpdump -i any -w /openair-mme/mme.pcap > /dev/null 2>&1"')

        count = 0
        runCount = 0
        status = False
        while (count < 10) and (runCount < 5):
            res = subprocess.check_output(self.cli + ' top cicd-oai-mme', shell=True, universal_newlines=True)
            if re.search('/openair-mme/bin/oai_mme -c /openair-mme/etc/mme.conf', str(res)):
                runCount += 1
                if runCount == 5:
                    status = True
            count += 1
            time.sleep(2)
        if status:
            print ('Deployment OAI-MME --> OK')
        else:
            print ('Problem deploying OAI-MME')
            sys.exit(-1)

    def deploySPGWC(self):
        res = ''
        # first check if tag exists
        try:
            res = subprocess.check_output(self.cli + ' image inspect oai-spgwc:' + self.tag, shell=True, universal_newlines=True)
        except:
            sys.exit(-1)

        spgwcEnvFile = ''
        cwd = os.getcwd()
        if os.path.isfile(cwd + '/ci-scripts/oai-ran-sanity-check/spgwc.env'):
            spgwcEnvFile = './ci-scripts/oai-ran-sanity-check/spgwc.env'
        elif os.path.isfile(cwd + '/oai-ran-sanity-check/spgwc.env'):
            spgwcEnvFile = './oai-ran-sanity-check/spgwc.env'
        else:
            sys.exit(-1)

        subprocess_run_w_echo(self.cli + ' run --privileged --name cicd-oai-spgwc --network cicd-oai-public-net --ip ' + CICD_SPGWC_PUBLIC_ADDR + ' --env-file ' + spgwcEnvFile + ' --health-cmd "pgrep --count oai_spgwc" -d oai-spgwc:' + self.tag)
        time.sleep(2)
        subprocess_run_w_echo(self.cli + ' exec -d cicd-oai-spgwc /bin/bash -c "nohup tcpdump -i any -w /openair-spgwc/spgwc.pcap > /dev/null 2>&1"')

        count = 0
        runCount = 0
        status = False
        while (count < 10) and (runCount < 5):
            res = subprocess.check_output(self.cli + ' top cicd-oai-spgwc', shell=True, universal_newlines=True)
            if re.search('/openair-spgwc/bin/oai_spgwc -c /openair-spgwc/etc/spgw_c.json -o', str(res)):
                runCount += 1
                if runCount == 5:
                    status = True
            count += 1
            time.sleep(2)
        if status:
            print ('Deployment SPGWC --> OK')
        else:
            print ('Problem deploying SPGWC')
            sys.exit(-1)

    def deploySPGWU(self):
        res = ''
        # first check if tag exists
        try:
            res = subprocess.check_output(self.cli + ' image inspect oai-spgwu-tiny:' + self.tag, shell=True, universal_newlines=True)
        except:
            sys.exit(-1)

        spgwuEnvFile = ''
        cwd = os.getcwd()
        if os.path.isfile(cwd + '/ci-scripts/oai-ran-sanity-check/spgwu.env'):
            spgwuEnvFile = './ci-scripts/oai-ran-sanity-check/spgwu.env'
        elif os.path.isfile(cwd + '/oai-ran-sanity-check/spgwu.env'):
            spgwuEnvFile = './oai-ran-sanity-check/spgwu.env'
        else:
            sys.exit(-1)

        subprocess_run_w_echo(self.cli + ' run --privileged --name cicd-oai-spgwu-tiny --network cicd-oai-public-net --ip ' + CICD_SPGWU_PUBLIC_ADDR + ' --env-file ' + spgwuEnvFile + ' --health-cmd "pgrep --count oai_spgwu" -d oai-spgwu-tiny:' + self.tag)

        count = 0
        runCount = 0
        status = False
        while (count < 10) and (runCount < 5):
            res = subprocess.check_output(self.cli + ' top cicd-oai-spgwu-tiny', shell=True, universal_newlines=True)
            if re.search('/openair-spgwu-tiny/bin/oai_spgwu -c /openair-spgwu-tiny/etc/spgw_u.conf -o', str(res)):
                runCount += 1
                if runCount == 5:
                    status = True
            count += 1
            time.sleep(2)
        if status:
            print ('Deployment SPGWU-TINY --> OK')
        else:
            print ('Problem deploying SPGWU-TINY')
            sys.exit(-1)

    def deployTrfGen(self):
        res = ''
        # first check if tag exists
        try:
            res = subprocess.check_output(self.cli + ' image inspect trf-gen:' + self.tag, shell=True, universal_newlines=True)
        except:
            sys.exit(-1)

        subprocess_run_w_echo(self.cli + ' run --privileged --name cicd-trf-gen --network cicd-oai-public-net --ip ' + CICD_TRFGEN_PUBLIC_ADDR + ' -d trf-gen:' + self.tag)
        time.sleep(2)
        subprocess_run_w_echo(self.cli + ' exec cicd-trf-gen /bin/bash -c "ip route add 12.0.0.0/24 via ' + CICD_SPGWU_PUBLIC_ADDR + ' dev eth0"')
        print ('Deployment TRF-GEN --> OK')

    def deployENB(self):
        res = ''
        # first check if tag exists
        try:
            res = subprocess.check_output(self.cli + ' image inspect oai-enb:' + self.tag, shell=True, universal_newlines=True)
        except:
            sys.exit(-1)

        enbEnvFile = ''
        cwd = os.getcwd()
        if os.path.isfile(cwd + '/ci-scripts/oai-ran-sanity-check/enb.env'):
            enbEnvFile = './ci-scripts/oai-ran-sanity-check/enb.env'
        elif os.path.isfile(cwd + '/oai-ran-sanity-check/enb.env'):
            enbEnvFile = './oai-ran-sanity-check/enb.env'
        else:
            sys.exit(-1)

        subprocess_run_w_echo(self.cli + ' run --privileged --name cicd-oai-enb --network cicd-oai-public-net --ip ' + CICD_ENB_RF_SIM_PUBLIC_ADDR + ' --env-file ' + enbEnvFile + ' -d oai-enb:' + self.tag)

        count = 0
        runCount = 0
        status = False
        while (count < 10) and (runCount < 5):
            res = subprocess.check_output(self.cli + ' top cicd-oai-enb', shell=True, universal_newlines=True)
            if re.search('/opt/oai-enb/bin/lte-softmodem.Rel15 -O /opt/oai-enb/etc/enb.conf', str(res)):
                runCount += 1
                if runCount == 5:
                    status = True
            count += 1
            time.sleep(2)
        if status:
            print ('Deployment RF-SIM-ENB --> OK')
        else:
            print ('Problem deploying RF-SIM-ENB')
            sys.exit(-1)

    def deployUE(self):
        res = ''
        # first check if tag exists
        try:
            res = subprocess.check_output(self.cli + ' image inspect oai-lte-ue:' + self.tag, shell=True, universal_newlines=True)
        except:
            sys.exit(-1)

        ueEnvFile = ''
        cwd = os.getcwd()
        if os.path.isfile(cwd + '/ci-scripts/oai-ran-sanity-check/ue.env'):
            ueEnvFile = './ci-scripts/oai-ran-sanity-check/ue.env'
        elif os.path.isfile(cwd + '/oai-ran-sanity-check/ue.env'):
            ueEnvFile = './oai-ran-sanity-check/ue.env'
        else:
            sys.exit(-1)

        subprocess_run_w_echo(self.cli + ' run --privileged --name cicd-oai-ue --network cicd-oai-public-net --ip ' + CICD_UE0_RF_SIM_PUBLIC_ADDR + ' --env-file ' + ueEnvFile + ' -d oai-lte-ue:' + self.tag)

        count = 0
        runCount = 0
        status = False
        while (count < 10) and (runCount < 5):
            res = subprocess.check_output(self.cli + ' top cicd-oai-ue', shell=True, universal_newlines=True)
            if re.search('/opt/oai-lte-ue/bin/lte-uesoftmodem.Rel15', str(res)):
                runCount += 1
                if runCount == 5:
                    status = True
            count += 1
            time.sleep(2)
        if status:
            print ('Deployment RF-SIM-LTE-UE --> OK')
        else:
            print ('Problem deploying RF-SIM-LTE-UE')
            sys.exit(-1)

    def removeAllContainers(self):
        try:
            subprocess_run_w_echo(self.cli + ' rm -f cicd-cassandra cicd-oai-hss cicd-redis cicd-oai-mme cicd-oai-spgwc cicd-oai-spgwu-tiny cicd-oai-enb cicd-oai-ue cicd-trf-gen')
        except:
            pass

    def retrieveContainerLogs(self):
        subprocess_run_w_echo('mkdir -p archives')
        magmaUsed = True
        prefix = 'magma'
        res = subprocess.check_output(self.cli + ' inspect --format="ImageName = {{.ImageName}}" cicd-oai-mme', shell=True, universal_newlines=True)
        if re.search('oai-mme:', str(res)):
            magmaUsed = False
            prefix = 'openair'

        # First stop tcpdump capture on MME container
        subprocess_run_w_echo(self.cli + ' exec cicd-oai-mme /bin/bash -c "killall tcpdump"')
        subprocess_run_w_echo(self.cli + ' exec cicd-oai-spgwc /bin/bash -c "killall tcpdump"')
        time.sleep(2)
        try:
            res = subprocess.check_output(self.cli + ' exec cicd-oai-mme /bin/bash -c "ls /' + prefix + '-mme/*.pcap"', shell=True, universal_newlines=True)
            subprocess_run_w_echo(self.cli + ' cp cicd-oai-mme:' + res.strip() + ' archives/ || true')
        except:
            pass
        if magmaUsed:
            subprocess_run_w_echo(self.cli + ' cp cicd-oai-mme:/magma-mme/sctpd.log archives/ || true')
            subprocess_run_w_echo(self.cli + ' cp cicd-oai-mme:/magma-mme/mme-stdout.log archives/ || true')
        subprocess_run_w_echo(self.cli + ' logs cicd-oai-mme > archives/mme.log 2>&1 || true')
        subprocess_run_w_echo(self.cli + ' logs cicd-oai-hss > archives/hss.log 2>&1 || true')
        subprocess_run_w_echo(self.cli + ' logs cicd-oai-spgwc > archives/spgwc.log 2>&1 || true')
        subprocess_run_w_echo(self.cli + ' cp cicd-oai-spgwc:/openair-spgwc/spgwc.pcap archives/ || true')
        subprocess_run_w_echo(self.cli + ' logs cicd-oai-spgwu-tiny > archives/spgwu-tiny.log 2>&1 || true')
        subprocess_run_w_echo(self.cli + ' logs cicd-oai-enb > archives/enb.log 2>&1 || true')
        subprocess_run_w_echo(self.cli + ' logs cicd-oai-ue > archives/ue.log 2>&1 || true')
        subprocess_run_w_echo('mkdir -p archives/conf/hss')
        subprocess_run_w_echo(self.cli + ' cp cicd-oai-hss:/openair-hss/etc/hss_rel14.json archives/conf/hss || true')
        subprocess_run_w_echo(self.cli + ' cp cicd-oai-hss:/openair-hss/etc/hss_rel14.conf archives/conf/hss || true')
        subprocess_run_w_echo(self.cli + ' cp cicd-oai-hss:/openair-hss/etc/hss_rel14_fd.conf archives/conf/hss || true')
        subprocess_run_w_echo('mkdir -p archives/conf/mme')
        subprocess_run_w_echo(self.cli + ' cp cicd-oai-mme:/' + prefix + '-mme/etc/mme.conf archives/conf/mme || true')
        subprocess_run_w_echo(self.cli + ' cp cicd-oai-mme:/' + prefix + '-mme/etc/mme_fd.conf archives/conf/mme || true')
        subprocess_run_w_echo('mkdir -p archives/conf/spgwc')
        subprocess_run_w_echo(self.cli + ' cp cicd-oai-spgwc:/openair-spgwc/etc/spgw_c.json archives/conf/spgwc || true')
        subprocess_run_w_echo('mkdir -p archives/conf/spgwu-tiny')
        subprocess_run_w_echo(self.cli + ' cp cicd-oai-spgwu-tiny:/openair-spgwu-tiny/etc/spgw_u.conf archives/conf/spgwu-tiny || true')

    def testTrafficWithPing(self):
        subprocess_run_w_echo('mkdir -p archives')
        # first retrieve IP address allocated to UE by EPC
        res = subprocess.check_output(self.cli + ' exec cicd-oai-ue /bin/bash -c "ifconfig oaitun_ue1 | grep inet"', shell=True, universal_newlines=True)
        res2 = re.search('inet (?P<ip_addr>[0-9\.]+)', str(res.strip()))
        if res2 is not None:
            print('Found IP address: ' + res2.group('ip_addr'))
            UE_EPC_IP_ADDRESS = res2.group('ip_addr')
        else:
            print('Could not foound out UE allocated IP address')
            sys.exit(-1)

        # Then test ping from trf-gen container
        subprocess_run_w_echo(self.cli + ' exec cicd-trf-gen /bin/bash -c "ping -c 10 ' + UE_EPC_IP_ADDRESS + '" > archives/ping_ue_from_trf_gen.log')
        res = subprocess.check_output('cat archives/ping_ue_from_trf_gen.log', shell=True, universal_newlines=True)
        res2 = re.search('10 packets transmitted, 10 received, 0% packet loss', str(res.strip()))
        if res is not None:
            print('TRF-GEN --> UE: OK')
        else:
            print('TRF-GEN --> UE: Missing packets')
            sys.exit(-1)

        # Finally test ping from UE container
        subprocess_run_w_echo(self.cli + ' exec cicd-oai-ue /bin/bash -c "ping -c 10 -I ' + UE_EPC_IP_ADDRESS + ' ' + CICD_TRFGEN_PUBLIC_ADDR + '" > archives/ping_trf_gen_from_ue.log')
        res = subprocess.check_output('cat archives/ping_trf_gen_from_ue.log', shell=True, universal_newlines=True)
        res2 = re.search('10 packets transmitted, 10 received, 0% packet loss', str(res.strip()))
        if res is not None:
            print('UE --> TRF-GEN: OK')
        else:
            print('UE --> TRF-GEN: Missing packets')
            sys.exit(-1)


def subprocess_run_w_echo(cmd):
    print(cmd)
    subprocess.run(cmd, shell=True)

def Usage():
    print('----------------------------------------------------------------------------------------------------------------------')
    print('OAI-RAN-Sanity-Check-Deploy.py')
    print('   Deploy for DsTester in the pipeline.')
    print('----------------------------------------------------------------------------------------------------------------------')
    print('Usage: python3 OAI-RAN-Sanity-Check-Deploy.py [options]')
    print('  --help  Show this help.')
    print('---------------------------------------------------------------------------------------------- Mandatory Options -----')
    print('  --action={CreateNetworks,RemoveNetworks,...}')
    print('-------------------------------------------------------------------------------------------------------- Options -----')
    print('  --tag=[Image Tag in registry]')
    print('------------------------------------------------------------------------------------------------- Actions Syntax -----')
    print('python3 OAI-RAN-Sanity-Check-Deploy.py --action=CreateNetworks')
    print('python3 OAI-RAN-Sanity-Check-Deploy.py --action=RemoveNetworks')
    print('python3 OAI-RAN-Sanity-Check-Deploy.py --action=DeployCassandra')
    print('python3 OAI-RAN-Sanity-Check-Deploy.py --action=DeployHSS --tag=[tag]')
    print('python3 OAI-RAN-Sanity-Check-Deploy.py --action=DeployRedis')
    print('python3 OAI-RAN-Sanity-Check-Deploy.py --action=DeployMME --tag=[tag]')
    print('python3 OAI-RAN-Sanity-Check-Deploy.py --action=DeploySPGWC --tag=[tag]')
    print('python3 OAI-RAN-Sanity-Check-Deploy.py --action=DeploySPGWU --tag=[tag]')
    print('python3 OAI-RAN-Sanity-Check-Deploy.py --action=DeployTrfGen --tag=[tag]')
    print('python3 OAI-RAN-Sanity-Check-Deploy.py --action=DeployRfSimENB --tag=[tag]')
    print('python3 OAI-RAN-Sanity-Check-Deploy.py --action=DeployRfSimUE --tag=[tag]')
    print('python3 OAI-RAN-Sanity-Check-Deploy.py --action=TestTrafficPing')
    print('python3 OAI-RAN-Sanity-Check-Deploy.py --action=RetrieveLogs')
    print('python3 OAI-RAN-Sanity-Check-Deploy.py --action=RemoveAllContainers')

#--------------------------------------------------------------------------------------------------------
#
# Start of main
#
#--------------------------------------------------------------------------------------------------------

SNRAN = deployWithOAIran()

argvs = sys.argv
argc = len(argvs)

while len(argvs) > 1:
    myArgv = argvs.pop(1)
    if re.match('^\-\-help$', myArgv, re.IGNORECASE):
        Usage()
        sys.exit(0)
    elif re.match('^\-\-action=(.+)$', myArgv, re.IGNORECASE):
        matchReg = re.match('^\-\-action=(.+)$', myArgv, re.IGNORECASE)
        action = matchReg.group(1)
        if action != 'CreateNetworks' and \
           action != 'RemoveNetworks' and \
           action != 'DeployCassandra' and \
           action != 'DeployHSS' and \
           action != 'DeployRedis' and \
           action != 'DeployMME' and \
           action != 'DeployOldMME' and \
           action != 'DeploySPGWC' and \
           action != 'DeploySPGWU' and \
           action != 'DeployTrfGen' and \
           action != 'DeployRfSimENB' and \
           action != 'DeployRfSimUE' and \
           action != 'RetrieveLogs' and \
           action != 'TestTrafficPing' and \
           action != 'RemoveAllContainers':
            print('Unsupported Action => ' + action)
            Usage()
            sys.exit(-1)
        SNRAN.action = action
    elif re.match('^\-\-tag=(.+)$', myArgv, re.IGNORECASE):
        matchReg = re.match('^\-\-tag=(.+)$', myArgv, re.IGNORECASE)
        SNRAN.tag = matchReg.group(1)

if SNRAN.action == 'CreateNetworks':
    SNRAN.createNetworks()
elif SNRAN.action == 'RemoveNetworks':
    SNRAN.removeNetworks()
elif SNRAN.action == 'DeployCassandra':
    SNRAN.deployCassandra()
elif SNRAN.action == 'DeployHSS':
    if SNRAN.tag == '':
        print('Missing OAI-HSS image tag')
        Usage()
        sys.exit(-1)
    SNRAN.deployHSS()
elif SNRAN.action == 'DeployRedis':
    SNRAN.deployRedis()
elif SNRAN.action == 'DeployMME':
    if SNRAN.tag == '':
        print('Missing MAGMA-MME image tag')
        Usage()
        sys.exit(-1)
    SNRAN.deployMME()
elif SNRAN.action == 'DeployOldMME':
    if SNRAN.tag == '':
        print('Missing OAI-MME image tag')
        Usage()
        sys.exit(-1)
    SNRAN.deployOldMME()
elif SNRAN.action == 'DeploySPGWC':
    if SNRAN.tag == '':
        print('Missing OAI-SPGWC image tag')
        Usage()
        sys.exit(-1)
    SNRAN.deploySPGWC()
elif SNRAN.action == 'DeploySPGWU':
    if SNRAN.tag == '':
        print('Missing OAI-SPGWU image tag')
        Usage()
        sys.exit(-1)
    SNRAN.deploySPGWU()
elif SNRAN.action == 'DeployTrfGen':
    if SNRAN.tag == '':
        print('Missing TRF-GEN image tag')
        Usage()
        sys.exit(-1)
    SNRAN.deployTrfGen()
elif SNRAN.action == 'DeployRfSimENB':
    if SNRAN.tag == '':
        print('Missing OAI-ENB image tag')
        Usage()
        sys.exit(-1)
    SNRAN.deployENB()
elif SNRAN.action == 'DeployRfSimUE':
    if SNRAN.tag == '':
        print('Missing OAI-LTE-UE image tag')
        Usage()
        sys.exit(-1)
    SNRAN.deployUE()
elif SNRAN.action == 'TestTrafficPing':
    SNRAN.testTrafficWithPing()
elif SNRAN.action == 'RetrieveLogs':
    SNRAN.retrieveContainerLogs()
elif SNRAN.action == 'RemoveAllContainers':
    SNRAN.removeAllContainers()

sys.exit(0)
