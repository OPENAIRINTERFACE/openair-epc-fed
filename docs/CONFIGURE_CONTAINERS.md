<table style="border-collapse: collapse; border: none;">
  <tr style="border-collapse: collapse; border: none;">
    <td style="border-collapse: collapse; border: none;">
      <a href="http://www.openairinterface.org/">
         <img src="./images/oai_final_logo.png" alt="" border=3 height=50 width=150>
         </img>
      </a>
    </td>
    <td style="border-collapse: collapse; border: none; vertical-align: center;">
      <b><font size = "5">OpenAirInterface Core Network Docker Deployment : Configure Containers</font></b>
    </td>
  </tr>
</table>


**TABLE OF CONTENTS**

1.  [Networking](#1-create-a-docker-bridged-network)
2.  [Deploy](#2-deploy-the-containers)
3.  [Configure](#3-configure-the-containers)
    1.  [Cassandra](#31-cassandra)
    2.  [HSS](#32-hss)
    3.  [MME](#33-mme)
    4.  [SPGW-C](#34-spgw-c)
    5.  [SPGW-U](#35-spgw-u)

# 1. Create a Docker Bridged Network #

```bash
$ docker network create --attachable --subnet 192.168.61.192/26 --ip-range 192.168.61.192/26 prod-oai-public-net
```

Once again we choose an idle IP range in our network. Please change to proper value in your environment.

In the servers that are hosting the eNB(s) and/or gNB(s), create IP route(s):

```bash
# On minimassive
sudo ip route add 192.168.61.192/26 via 192.168.18.197 dev bond0

# On mozart
sudo ip route add 192.168.61.192/26 via 192.168.18.197 dev p1p1
```

Where `192.168.18.197` is the IP address of the Docker Host
Where `bond0` or `p1p1` are the NIC of the eNB/gNB server(s).

# 2. Deploy the containers #

```bash
$ docker run --name prod-cassandra -d -e CASSANDRA_CLUSTER_NAME="OAI HSS Cluster" -e CASSANDRA_ENDPOINT_SNITCH=GossipingPropertyFileSnitch cassandra:2.1
$ docker run --privileged --name prod-oai-hss -d oai-hss:production /bin/bash -c "sleep infinity"
$ docker network connect prod-oai-public-net prod-oai-hss
$ docker run --privileged --name prod-oai-mme --network prod-oai-public-net -d oai-mme:production /bin/bash -c "sleep infinity"
$ docker run --privileged --name prod-oai-spgwc --network prod-oai-public-net -d oai-spgwc:production /bin/bash -c "sleep infinity"
$ docker run --privileged --name prod-oai-spgwu-tiny --network prod-oai-public-net -d oai-spgwu-tiny:production /bin/bash -c "sleep infinity"
```

# 3. Configure the containers #

We are using the following configuration. You need to adapt to your setup.

*  PLMN
   *   MCC = 320
   *   MNC = 230
*  TAC
   * 5  <--- Primary TAC
   * 6
   * 7
*  APN1 = apn1.carrier.com
*  APN2 = apn2.carrier.com
*  200 Users with the 1st IMSI = 320230100000001
*  LTE-KEY = 0c0a34601d4f07677303652c0462535b
*  OP = 63bfa50ee6523365ff14c1f45f88737d

## 3.1. Cassandra ##

```bash
$ docker cp component/oai-hss/src/hss_rel14/db/oai_db.cql prod-cassandra:/home
$ docker exec -it prod-cassandra /bin/bash -c "nodetool status"
$ Cassandra_IP=`docker inspect --format="{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}" prod-cassandra`
$ docker exec -it prod-cassandra /bin/bash -c "cqlsh --file /home/oai_db.cql ${Cassandra_IP}"
```

## 3.2. HSS ##

```bash
$ HSS_IP=`docker exec -it prod-oai-hss /bin/bash -c "ifconfig eth1 | grep inet" | sed -f ./ci-scripts/convertIpAddrFromIfconfig.sed`
$ python3 component/oai-hss/ci-scripts/generateConfigFiles.py --kind=HSS --cassandra=${Cassandra_IP} --hss_s6a=${HSS_IP} --apn1=apn1.carrier.com --apn2=apn2.carrier.com --users=200 --imsi=320230100000001 --ltek=0c0a34601d4f07677303652c0462535b --op=63bfa50ee6523365ff14c1f45f88737d --nb_mmes=1 --from_docker_file
$ docker cp ./hss-cfg.sh prod-oai-hss:/openair-hss/scripts
$ docker exec -it prod-oai-hss /bin/bash -c "cd /openair-hss/scripts && chmod 777 hss-cfg.sh && ./hss-cfg.sh"
INFO:root:320230100000181 181 41 0c0a34601d4f07677303652c0462535b mme.openairinterface.org 3 openairinterface.org 2683b376d1056746de3b254012908e0e 96 {"Subscription-Data":{"Access-Restriction-Data":41,"Subscriber-Status":0,"Network-Access-Mode":2,"Regional-Subscription-Zone-Code":["0x0123","0x4567","0x89AB","0xCDEF","0x1234","0x5678","0x9ABC","0xDEF0","0x2345","0x6789"],"MSISDN":"0x181","AMBR":{"Max-Requested-Bandwidth-UL":50000000,"Max-Requested-Bandwidth-DL":100000000},"APN-Configuration-Profile":{"Context-Identifier":0,"All-APN-Configurations-Included-Indicator":0,"APN-Configuration":{"Context-Identifier":0,"PDN-Type":0,"Service-Selection":"apn1.carrier.com","EPS-Subscribed-QoS-Profile":{"QoS-Class-Identifier":9,"Allocation-Retention-Priority":{"Priority-Level":15,"Pre-emption-Capability":0,"Pre-emption-Vulnerability":0}},"AMBR":{"Max-Requested-Bandwidth-UL":50000000,"Max-Requested-Bandwidth-DL":100000000},"PDN-GW-Allocation-Type":0,"MIP6-Agent-Info":{"MIP-Home-Agent-Address":["172.26.17.183"]}},"APN-Configuration":{"Context-Identifier":0,"PDN-Type":0,"Service-Selection":"apn2.carrier.com","EPS-Subscribed-QoS-Profile":{"QoS-Class-Identifier":9,"Allocation-Retention-Priority":{"Priority-Level":13,"Pre-emption-Capability":1,"Pre-emption-Vulnerability":0}},"AMBR":{"Max-Requested-Bandwidth-UL":50000000,"Max-Requested-Bandwidth-DL":100000000},"PDN-GW-Allocation-Type":0,"MIP6-Agent-Info":{"MIP-Home-Agent-Address":["172.26.17.183"]}}},"Subscribed-Periodic-RAU-TAU-Timer":0}}
....
DEBUG:cassandra.io.libevreactor:Closing connection (140274865011456) to 192.168.17.4
DEBUG:cassandra.io.libevreactor:Closed socket to 192.168.17.4
DEBUG:cassandra.io.libevreactor:Closing connection (140274819517464) to 192.168.17.4
DEBUG:cassandra.io.libevreactor:All Connections currently closed, event loop ended
DEBUG:cassandra.io.libevreactor:Closed socket to 192.168.17.4
DEBUG:cassandra.io.libevreactor:Waiting for event loop thread to join...
DEBUG:cassandra.io.libevreactor:Event loop thread was joined
DEBUG:cassandra.cluster:Shutting down Cluster Scheduler
DEBUG:cassandra.cluster:Shutting down control connection
vhss.mmeidentity truncated
vhss.mmeidentity_host truncated
3 mme-isdn mme.openairinterface.org openairinterface.org 1
....
Generating a RSA private key
.................................................................................+++++
.....................+++++
writing new private key to 'cakey.pem'
-----
Generating RSA private key, 1024 bit long modulus (2 primes)
....................................................+++++
........................................+++++
e is 65537 (0x010001)
Using configuration from /usr/lib/ssl/openssl.cnf
###########################################################
# The following lines in error are OK
Can't open ./demoCA/index.txt.attr for reading, No such file or directory
140684118282688:error:02001002:system library:fopen:No such file or directory:../crypto/bio/bss_file.c:72:fopen('./demoCA/index.txt.attr','r')
140684118282688:error:2006D080:BIO routines:BIO_new_file:no such file:../crypto/bio/bss_file.c:79:
###########################################################
Check that the request matches the signature
Signature ok
Certificate Details:
        Serial Number: 1 (0x1)
        Validity
            Not Before: Apr 10 17:08:34 2020 GMT
            Not After : Apr 10 17:08:34 2021 GMT
        Subject:
            countryName               = FR
            stateOrProvinceName       = BdR
            organizationName          = fD
            organizationalUnitName    = Tests
            commonName                = hss.openairinterface.org
        X509v3 extensions:
            X509v3 Basic Constraints:
                CA:FALSE
            Netscape Comment:
                OpenSSL Generated Certificate
            X509v3 Subject Key Identifier:
                D6:1A:46:9D:69:91:58:D2:C7:2C:CC:D8:91:68:68:DF:FA:D6:A1:1D
            X509v3 Authority Key Identifier:
                keyid:B0:54:5F:E4:37:79:B3:F3:5A:C1:33:75:8E:93:A1:B6:61:A1:A3:CF

Certificate is to be certified until Apr 10 17:08:34 2021 GMT (365 days)

Write out database with 1 new entries
Data Base Updated
'hss.cert.pem' -> '/openair-hss/etc/hss.cert.pem'
'cacert.pem' -> '/openair-hss/etc/cacert.pem'
'hss.key.pem' -> '/openair-hss/etc/hss.key.pem'
```

## 3.3. MME ##

```bash
$ MME_IP=`docker inspect --format="{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}" prod-oai-mme`
$ SPGW0_IP=`docker inspect --format="{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}" prod-oai-spgwc`
$ python3 component/oai-mme/ci-scripts/generateConfigFiles.py --kind=MME --hss_s6a=${HSS_IP} --mme_s6a=${MME_IP} --mme_s1c_IP=${MME_IP} --mme_s1c_name=eth0 --mme_s10_IP=${MME_IP} --mme_s10_name=eth0 --mme_s11_IP=${MME_IP} --mme_s11_name=eth0 --spgwc0_s11_IP=${SPGW0_IP} --mcc=320 --mnc=230 --tac_list="5 6 7" --from_docker_file
$ docker cp ./mme-cfg.sh prod-oai-mme:/openair-mme/scripts
$ docker exec -it prod-oai-mme /bin/bash -c "cd /openair-mme/scripts && chmod 777 mme-cfg.sh && ./mme-cfg.sh"', 'archives/mme_config.log
ifconfig lo:s10 127.0.0.10 up --> OK
####################################
### THIS IS NORMAL
File /openair-mme/etc/mme.cert.pem not found
MME S6A: Did not find valid certificate in /openair-mme/etc
####################################
MME S6A: generating new certificate in /openair-mme/etc...
Creating MME certificate for user 'mme.openairinterface.org'
Generating a RSA private key
.....+++++
....+++++
writing new private key to 'mme.cakey.pem'
-----
Generating RSA private key, 1024 bit long modulus (2 primes)
..............+++++
.................+++++
e is 65537 (0x010001)
Using configuration from /usr/lib/ssl/openssl.cnf
####################################
### THIS IS NORMAL
Can't open ./demoCA/index.txt.attr for reading, No such file or directory
140419321815488:error:02001002:system library:fopen:No such file or directory:../crypto/bio/bss_file.c:72:fopen('./demoCA/index.txt.attr','r')
140419321815488:error:2006D080:BIO routines:BIO_new_file:no such file:../crypto/bio/bss_file.c:79:
####################################
Check that the request matches the signature
Signature ok
Certificate Details:
        Serial Number: 1 (0x1)
        Validity
            Not Before: Apr 10 17:08:42 2020 GMT
            Not After : Apr 10 17:08:42 2021 GMT
        Subject:
            countryName               = FR
            stateOrProvinceName       = PACA
            organizationName          = Eurecom
            organizationalUnitName    = CM
            commonName                = mme.openairinterface.org
        X509v3 extensions:
            X509v3 Basic Constraints:
                CA:FALSE
            Netscape Comment:
                OpenSSL Generated Certificate
            X509v3 Subject Key Identifier:
                78:13:2C:26:A0:53:D9:5D:0C:B9:AF:90:B6:20:15:59:34:5F:32:0A
            X509v3 Authority Key Identifier:
                keyid:4A:08:98:D8:33:12:49:E9:FE:C6:59:AF:71:65:C5:8B:6B:71:98:9E

Certificate is to be certified until Apr 10 17:08:42 2021 GMT (365 days)

Write out database with 1 new entries
Data Base Updated
/openair-mme/scripts
MME S6A: Found valid certificate in /openair-mme/etc
```

**IMPORTANT: MME_IP VALUE IS THE ONE YOU NEED TO PASS TO YOUR ENB/GNB CONFIGURATION FILE**

and not the Docker Host IP address.

## 3.4. SPGW-C ##

```bash
$ python3 component/oai-spgwc/ci-scripts/generateConfigFiles.py --kind=SPGW-C --s11c=eth0 --sxc=eth0 --apn=apn1.carrier.com --dns1_ip=YOUR_DNS_IP_ADDRESS --dns2_ip=A_SECONDARY_DNS_IP_ADDRESS --from_docker_file
$ docker cp ./spgwc-cfg.sh prod-oai-spgwc:/openair-spgwc
$ docker exec -it prod-oai-spgwc /bin/bash -c "cd /openair-spgwc && chmod 777 spgwc-cfg.sh && ./spgwc-cfg.sh"
ifconfig lo:s5c 127.0.0.15 up --> OK
ifconfig lo:p5c 127.0.0.16 up --> OK
```

## 3.5. SPGW-U ##

```bash
$ python3 component/oai-spgwu-tiny/ci-scripts/generateConfigFiles.py --kind=SPGW-U --sxc_ip_addr=${SPGW0_IP} --sxu=eth0 --s1u=eth0 --from_docker_file
$ docker cp ./spgwu-cfg.sh prod-oai-spgwu-tiny:/openair-spgwu-tiny
$ docker exec -it prod-oai-spgwu-tiny /bin/bash -c "cd /openair-spgwu-tiny && chmod 777 spgwu-cfg.sh && ./spgwu-cfg.sh"
```

**CAUTION: IF YOU MADE A MISTAKE WHILE CONFIGURING (I.E. EXECUTING ONE OF THE `-cfg.sh` SCRIPTS IN A CONTAINER): 2 WAYS TO RECOVER:**

1.  Remove all containers and redeploy. Because the template configuration files have been modified, re-running the -cfg.sh script with modified parameters is **USELESS**.
2.  Install an editor (such as `vim`) on the container and edit manually. This is **NOT** the recommended way.

You are now ready to [start the network functions](./RUN_CNF.md).
