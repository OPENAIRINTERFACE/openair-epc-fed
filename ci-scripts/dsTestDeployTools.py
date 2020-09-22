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

CICD_PRIVATE_NETWORK_RANGE='192.168.68.0/26'
CICD_PUBLIC_NETWORK_RANGE='192.168.61.192/26'

CICD_CASS_IP_ADDR='192.168.68.2'
CICD_HSS_DBN_ADDR='192.168.68.3'

CICD_HSS_PUBLIC_ADDR='192.168.61.194'
CICD_MME_PUBLIC_ADDR='192.168.61.195'
CICD_SPGWC_PUBLIC_ADDR='192.168.61.196'
CICD_SPGWU_PUBLIC_ADDR='192.168.61.197'

class deployForDsTester():
    def __init__(self):
        self.action = 'None'
        self.tag = ''

    def createNetworks(self):
        # first check if already up?
        try:
            res = subprocess.check_output('docker network ls | egrep -c "cicd-oai-public-net|cicd-oai-private-net"', shell=True, universal_newlines=True)
            if int(str(res.strip())) > 0:
                self.removeNetworks()
        except:
            pass

        subprocess_run_w_echo('docker network create --attachable --subnet ' + CICD_PUBLIC_NETWORK_RANGE + ' --ip-range ' + CICD_PUBLIC_NETWORK_RANGE + ' cicd-oai-public-net')
        subprocess_run_w_echo('docker network create --attachable --subnet ' + CICD_PRIVATE_NETWORK_RANGE + ' --ip-range ' + CICD_PRIVATE_NETWORK_RANGE + ' cicd-oai-private-net')

    def removeNetworks(self):
        try:
            subprocess_run_w_echo('docker network rm cicd-oai-public-net cicd-oai-private-net')
        except:
            pass

    def deployCassandra(self):
        # first check if already up? If yes, remove everything.
        try:
            res = subprocess.check_output('docker ps -a | grep -c "cicd-cassandra"', shell=True, universal_newlines=True)
            if int(str(res.strip())) > 0:
                self.removeAllContainers()
        except:
            pass

        subprocess_run_w_echo('docker run --name cicd-cassandra --network cicd-oai-private-net --ip ' + CICD_CASS_IP_ADDR + ' -d -e CASSANDRA_CLUSTER_NAME="OAI HSS Cluster" -e CASSANDRA_ENDPOINT_SNITCH=GossipingPropertyFileSnitch cassandra:2.1')
        # waiting for the service to be properly started
        doLoop = True
        while doLoop:
            try:
                res = subprocess.check_output('docker exec -it cicd-cassandra /bin/bash -c "nodetool status"', shell=True, universal_newlines=True)
                rackFound = re.search('UN  ' + CICD_CASS_IP_ADDR, str(res))
                if rackFound is not None:
                    doLoop = False
            except:
                time.sleep(1)
                pass
        subprocess_run_w_echo('docker exec -it cicd-cassandra /bin/bash -c "nodetool status" | tee archives/cassandra_status.log')
        subprocess_run_w_echo('docker cp component/oai-hss/src/hss_rel14/db/oai_db.cql cicd-cassandra:/home')
        time.sleep(2)
        doLoop = True
        while doLoop:
            try:
                res = subprocess.check_output('docker exec -it cicd-cassandra /bin/bash -c "cqlsh --file /home/oai_db.cql ' + CICD_CASS_IP_ADDR + '"', shell=True, universal_newlines=True)
                print('docker exec -it cicd-cassandra /bin/bash -c "cqlsh --file /home/oai_db.cql ' + CICD_CASS_IP_ADDR + '"')
                doLoop = False
            except:
                time.sleep(2)
                pass

    def deployHSS(self):
        res = ''
        # first check if tag exists
        try:
            res = subprocess.check_output('docker image inspect oai-hss:' + self.tag, shell=True, universal_newlines=True)
        except:
            sys.exit(-1)

        # check if there is an entrypoint
        entrypoint = re.search('entrypoint', str(res))
        if entrypoint is not None:
            # SDB to Cassandra will be on `eth0`
            subprocess_run_w_echo('docker run --privileged --name cicd-oai-hss --network cicd-oai-private-net --ip ' + CICD_HSS_DBN_ADDR + ' -d --entrypoint "/bin/bash" oai-hss:' + self.tag + ' -c "sleep infinity"')
            # S6A to MME will be on `eth1`
            subprocess_run_w_echo('docker network connect --ip ' + CICD_HSS_PUBLIC_ADDR + ' cicd-oai-public-net cicd-oai-hss')
        else:
            # SDB to Cassandra will be on `eth0`
            subprocess_run_w_echo('docker run --privileged --name cicd-oai-hss --network cicd-oai-private-net --ip ' + CICD_HSS_DBN_ADDR + ' -d oai-hss:' + self.tag + ' /bin/bash -c "sleep infinity"')
            # S6A to MME will be on `eth1`
            subprocess_run_w_echo('docker network connect --ip ' + CICD_HSS_PUBLIC_ADDR + ' cicd-oai-public-net cicd-oai-hss')
        subprocess_run_w_echo('python3 component/oai-hss/ci-scripts/generateConfigFiles.py --kind=HSS --cassandra=' + CICD_CASS_IP_ADDR + ' --hss_s6a=' + CICD_HSS_PUBLIC_ADDR + ' --apn1=apn1.carrier.com --apn2=apn2.carrier.com --users=200 --imsi=100000000000001 --ltek=0c0a34601d4f07677303652c0462535b --op=63bfa50ee6523365ff14c1f45f88737d --nb_mmes=4 --from_docker_file')
        subprocess_run_w_echo('docker cp ./hss-cfg.sh cicd-oai-hss:/openair-hss/scripts')
        subprocess_run_w_echo('docker exec -it cicd-oai-hss /bin/bash -c "cd /openair-hss/scripts && chmod 777 hss-cfg.sh && ./hss-cfg.sh" > archives/hss_config.log')

    def deployMME(self):
        res = ''
        # first check if tag exists
        try:
            res = subprocess.check_output('docker image inspect oai-mme:' + self.tag, shell=True, universal_newlines=True)
        except:
            sys.exit(-1)

        # check if there is an entrypoint
        entrypoint = re.search('entrypoint', str(res))
        if entrypoint is not None:
            subprocess_run_w_echo('docker run --privileged --name cicd-oai-mme --network cicd-oai-public-net --ip ' + CICD_MME_PUBLIC_ADDR + ' -d --entrypoint "/bin/bash" oai-mme:' + self.tag + ' -c "sleep infinity"')
        else:
            subprocess_run_w_echo('docker run --privileged --name cicd-oai-mme --network cicd-oai-public-net --ip ' + CICD_MME_PUBLIC_ADDR + ' -d oai-mme:' + self.tag + ' /bin/bash -c "sleep infinity"')
        subprocess_run_w_echo('python3 ./ci-scripts/generate_mme_config_script.py --kind=MME --hss_s6a=' + CICD_HSS_PUBLIC_ADDR + ' --mme_s6a=' + CICD_MME_PUBLIC_ADDR + ' --mme_s1c_IP=' + CICD_MME_PUBLIC_ADDR + ' --mme_s1c_name=eth0 --mme_s10_IP=' + CICD_MME_PUBLIC_ADDR + ' --mme_s10_name=eth0 --mme_s11_IP=' + CICD_MME_PUBLIC_ADDR + ' --mme_s11_name=eth0 --spgwc0_s11_IP=' + CICD_SPGWC_PUBLIC_ADDR + ' --mme_gid=455 --mme_code=5 --mcc=320 --mnc=230 --tai_list="5556 506 301,5556 505 300,1235 203 101,1235 202 100,5557 506 301,5557 505 300,1236 203 101,1236 202 100" --realm=openairinterface.org --prefix=/openair-mme/etc --from_docker_file')
        subprocess_run_w_echo('docker cp ./mme-cfg.sh cicd-oai-mme:/openair-mme/scripts')
        subprocess_run_w_echo('docker exec -it cicd-oai-mme /bin/bash -c "cd /openair-mme/scripts && chmod 777 mme-cfg.sh && ./mme-cfg.sh" > archives/mme_config.log')
        subprocess_run_w_echo('docker cp mme.conf cicd-oai-mme:/openair-mme/etc')

    def deploySPGWC(self):
        res = ''
        # first check if tag exists
        try:
            res = subprocess.check_output('docker image inspect oai-spgwc:' + self.tag, shell=True, universal_newlines=True)
        except:
            sys.exit(-1)

        # check if there is an entrypoint
        entrypoint = re.search('entrypoint', str(res))
        if entrypoint is not None:
            subprocess_run_w_echo('docker run --privileged --name cicd-oai-spgwc --network cicd-oai-public-net --ip ' + CICD_SPGWC_PUBLIC_ADDR + ' -d --entrypoint "/bin/bash" oai-spgwc:' + self.tag + ' -c "sleep infinity"')
        else:
            subprocess_run_w_echo('docker run --privileged --name cicd-oai-spgwc --network cicd-oai-public-net --ip ' + CICD_SPGWC_PUBLIC_ADDR + ' -d oai-spgwc:' + self.tag + ' /bin/bash -c "sleep infinity"')
        subprocess_run_w_echo('python3 ci-scripts/generate_spgwc_config_script.py --kind=SPGW-C --s11c=eth0 --sxc=eth0 --prefix=/openair-spgwc/etc --dns1=192.168.18.129 --dns2=8.8.8.8 --apn_list="apn1.carrier.com apn2.carrier.com" --pdn_list="12.0.0.0/24 12.1.0.0/24" --s5p5_production --from_docker_file')
        subprocess_run_w_echo('docker cp ./spgwc-cfg.sh cicd-oai-spgwc:/openair-spgwc')
        subprocess_run_w_echo('docker exec -it cicd-oai-spgwc /bin/bash -c "cd /openair-spgwc && chmod 777 spgwc-cfg.sh && ./spgwc-cfg.sh" > archives/spgwc_config.log')
        subprocess_run_w_echo('docker cp ./spgw_c.conf cicd-oai-spgwc:/openair-spgwc/etc')

    def deploySPGWU(self):
        res = ''
        # first check if tag exists
        try:
            res = subprocess.check_output('docker image inspect oai-spgwu-tiny:' + self.tag, shell=True, universal_newlines=True)
        except:
            sys.exit(-1)

        # check if there is an entrypoint
        entrypoint = re.search('entrypoint', str(res))
        if entrypoint is not None:
            subprocess_run_w_echo('docker run --privileged --name cicd-oai-spgwu-tiny --network cicd-oai-public-net --ip ' + CICD_SPGWU_PUBLIC_ADDR + ' -d --entrypoint "/bin/bash" oai-spgwu-tiny:' + self.tag + ' -c "sleep infinity"')
        else:
            subprocess_run_w_echo('docker run --privileged --name cicd-oai-spgwu-tiny --network cicd-oai-public-net --ip ' + CICD_SPGWU_PUBLIC_ADDR + ' -d oai-spgwu-tiny:' + self.tag + ' /bin/bash -c "sleep infinity"')
        subprocess_run_w_echo('python3 ci-scripts/generate_spgwu-tiny_config_script.py --kind=SPGW-U --sxc_ip_addr=' + CICD_SPGWC_PUBLIC_ADDR + ' --sxu=eth0 --s1u=eth0 --sgi=eth0 --pdn_list="12.0.0.0/24 12.1.0.0/24" --prefix=/openair-spgwu-tiny/etc --from_docker_file')
        subprocess_run_w_echo('docker cp ./spgw_u.conf cicd-oai-spgwu-tiny:/openair-spgwu-tiny/etc')
        subprocess_run_w_echo('touch archives/spgwu_config.log')

    def removeAllContainers(self):
        try:
            subprocess_run_w_echo('docker rm -f cicd-cassandra cicd-oai-hss cicd-oai-mme cicd-oai-spgwc cicd-oai-spgwu-tiny')
        except:
            pass

def subprocess_run_w_echo(cmd):
    print(cmd)
    subprocess.run(cmd, shell=True)

def Usage():
    print('----------------------------------------------------------------------------------------------------------------------')
    print('dsTestDeployTools.py')
    print('   Deploy for DsTester in the pipeline.')
    print('----------------------------------------------------------------------------------------------------------------------')
    print('Usage: python3 dsTestDeployTools.py [options]')
    print('  --help  Show this help.')
    print('---------------------------------------------------------------------------------------------- Mandatory Options -----')
    print('  --action={CreateNetworks,RemoveNetworks,...}')
    print('-------------------------------------------------------------------------------------------------------- Options -----')
    print('  --tag=[Image Tag in registry]')
    print('------------------------------------------------------------------------------------------------- Actions Syntax -----')
    print('python3 dsTestDeployTools.py --action=CreateNetworks')
    print('python3 dsTestDeployTools.py --action=RemoveNetworks')
    print('python3 dsTestDeployTools.py --action=DeployCassandra')
    print('python3 dsTestDeployTools.py --action=DeployHSS --tag=[tag]')
    print('python3 dsTestDeployTools.py --action=DeployMME --tag=[tag]')
    print('python3 dsTestDeployTools.py --action=DeploySPGWC --tag=[tag]')
    print('python3 dsTestDeployTools.py --action=DeploySPGWU --tag=[tag]')
    print('python3 dsTestDeployTools.py --action=RemoveAllContainers')

#--------------------------------------------------------------------------------------------------------
#
# Start of main
#
#--------------------------------------------------------------------------------------------------------

DFDT = deployForDsTester()

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
           action != 'DeployMME' and \
           action != 'DeploySPGWC' and \
           action != 'DeploySPGWU' and \
           action != 'RemoveAllContainers':
            print('Unsupported Action => ' + action)
            Usage()
            sys.exit(-1)
        DFDT.action = action
    elif re.match('^\-\-tag=(.+)$', myArgv, re.IGNORECASE):
        matchReg = re.match('^\-\-tag=(.+)$', myArgv, re.IGNORECASE)
        DFDT.tag = matchReg.group(1)

if DFDT.action == 'CreateNetworks':
    DFDT.createNetworks()
elif DFDT.action == 'RemoveNetworks':
    DFDT.removeNetworks()
elif DFDT.action == 'DeployCassandra':
    DFDT.deployCassandra()
elif DFDT.action == 'DeployHSS':
    if DFDT.tag == '':
        print('Missing OAI-HSS image tag')
        Usage()
        sys.exit(-1)
    DFDT.deployHSS()
elif DFDT.action == 'DeployMME':
    if DFDT.tag == '':
        print('Missing OAI-MME image tag')
        Usage()
        sys.exit(-1)
    DFDT.deployMME()
elif DFDT.action == 'DeploySPGWC':
    if DFDT.tag == '':
        print('Missing OAI-SPGWC image tag')
        Usage()
        sys.exit(-1)
    DFDT.deploySPGWC()
elif DFDT.action == 'DeploySPGWU':
    if DFDT.tag == '':
        print('Missing OAI-SPGWU image tag')
        Usage()
        sys.exit(-1)
    DFDT.deploySPGWU()
elif DFDT.action == 'RemoveAllContainers':
    DFDT.removeAllContainers()

sys.exit(0)
