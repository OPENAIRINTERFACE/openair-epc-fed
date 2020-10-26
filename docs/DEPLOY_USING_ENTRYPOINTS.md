<table style="border-collapse: collapse; border: none;">
  <tr style="border-collapse: collapse; border: none;">
    <td style="border-collapse: collapse; border: none;">
      <a href="http://www.openairinterface.org/">
         <img src="./images/oai_final_logo.png" alt="" border=3 height=50 width=150>
         </img>
      </a>
    </td>
    <td style="border-collapse: collapse; border: none; vertical-align: center;">
      <b><font size = "5">OpenAirInterface Core Network Docker Deployment : Using Entrypoints</font></b>
    </td>
  </tr>
</table>

**TABLE OF CONTENTS**


# 1. Create a Docker Bridged Network #

Similar to [this previously described section](./CONFIGURE_CONTAINERS.md#1-create-a-docker-bridged-network).

```bash
$ docker network create --attachable --subnet 192.168.61.0/26 --ip-range 192.168.61.0/26 prod-oai-public-net
$ docker network create --attachable --subnet 192.168.62.0/26 --ip-range 192.168.62.0/26 prod-oai-private-net
```

# 2. Deploy the containers with automatical configuration #

You can use Helm charts to deploy in a cluster-like environment (such as OpenShift or Kubernetes).

An example is provided [here](https://github.com/OPENAIRINTERFACE/openair-k8s/blob/helm-deployment-S6a-S1C-S1U-in-network-18/charts/README.md).

In this page we will deploy still quite manually but we will use the newly implemented entrypoint scripts in the generated images.

When deploying with Helm charts or manifests, the main feature is to pass `environment variables` when the container is created. 
These `environment variables` are used by the entrypoint scripts to modify template configuration files and run the cNF as soon
as the container is ready.

Also we will use a fixed IP address allocation scheme:

* Cassandra and OAI-HSS will communicate on the `prod-oai-private-net` network:
  - Cassandra: `192.168.62.2`
  - OAI-HSS  : `192.168.62.3`
* OAI-HSS and all the other components will communicate on the `prod-oai-public-net` network:
  - OAI-HSS  : `192.168.61.2`
  - OAI-MME  : `192.168.61.3`
  - OAI-SPGWC: `192.168.61.4`
  - OAI-SPGWU: `192.168.61.5`

## 2.1. Deploying Cassandra service ##

It is what we are already doing:

```bash
$ docker run --name prod-cassandra --network prod-oai-private-net --ip 192.168.62.2 -d
             -e CASSANDRA_CLUSTER_NAME="OAI HSS Cluster" \
             -e CASSANDRA_ENDPOINT_SNITCH=GossipingPropertyFileSnitch cassandra:2.1
```

We are passing 2 env variables.

The rest is similar:

```bash
$ docker cp component/oai-hss/src/hss_rel14/db/oai_db.cql prod-cassandra:/home
$ docker exec -it prod-cassandra /bin/bash -c "nodetool status"
$ docker exec -it prod-cassandra /bin/bash -c "cqlsh --file /home/oai_db.cql 192.168.62.2"
```

## 2.2. Deploying OAI-HSS container ##

```bash
$ python3 ci-scripts/generateConfigFiles.py --kind=HSS \
           --cassandra=192.168.62.2 \
           --hss_s6a=192.168.61.2 \
           --apn1=apn1.carrier.com --apn2=apn2.carrier.com \
           --users=200 --imsi=320230100000001 \
           --ltek=0c0a34601d4f07677303652c0462535b --op=63bfa50ee6523365ff14c1f45f88737d \
           --nb_mmes=1 \
           --from_docker_file --env_for_entrypoint
```

With this python script, we are generating a `hss-env.list` file. Now we can start the container.

```bash
$ docker create --privileged --name prod-oai-hss --network prod-oai-private-net --ip 192.168.62.3 \
                --env-file ./hss-env.list oai-hss:production
ddd2a6f9033afda701839fcacefaead5d1e9c61325a8424e73c7677122363724
$ docker network connect --ip 192.168.61.2 prod-oai-public-net prod-oai-hss
$ docker start prod-oai-hss
prod-oai-hss
```

**TBD** : add logs command.

**IMPORTANT TO KNOW: the HSS container has 2 network interfaces (with 2 different IP addresses). YOU WILL NOT BE ABLE TO PING IT FROM ANOTHER MACHINE BUT THE DOCKER HOST.**

**IT MEANS YOU CANNOT PING FROM YOUR eNB server the HSS. YOU SHALL BE ABLE TO PING MME AND SPGW-U FROM YOUR e/gNB server(s).**

## 2.3. Deploying OAI-MME container ##

```bash
$ python3 component/oai-mme/ci-scripts/generateConfigFiles.py --kind=MME \
          --hss_s6a=192.168.61.2 --mme_s6a=192.168.61.3 \
          --mme_s1c_IP=192.168.61.3 --mme_s1c_name=eth0 \
          --mme_s10_IP=192.168.61.3 --mme_s10_name=eth0 \
          --mme_s11_IP=192.168.61.3 --mme_s11_name=eth0 \
          --spgwc0_s11_IP=192.168.61.4 \
          --mcc=320 --mnc=230 --tac_list="5 6 7" \
          --from_docker_file --env_for_entrypoint
```

With this python script, we are generating a `mme-env.list` file. Now we can start the container.

```bash
$ docker run --privileged --name prod-oai-mme --network prod-oai-public-net --ip 192.168.61.3
             --env-file ./mme-env.list oai-mme:production
```

**TBD** : add logs command.

## 2.4. Deploying OAI-SPGWC container ##

**CAUTION: you need to apply the correct DNS setup of your environment in order to have proper internet access when the UE is connected.**

**SO replace the following YOUR_DNS_IP_ADDRESS and A_SECONDARY_DNS_IP_ADDRESS in your command line.**

```bash
$ python3 component/oai-spgwc/ci-scripts/generateConfigFiles.py --kind=SPGW-C \
          --s11c=eth0 --sxc=eth0 --apn=apn1.carrier.com \
          --dns1_ip=YOUR_DNS_IP_ADDRESS --dns2_ip=A_SECONDARY_DNS_IP_ADDRESS \
          --from_docker_file --env_for_entrypoint
```

With this python script, we are generating a `spgwc-env.list` file. Now we can start the container.

```bash
$ docker run --privileged --name prod-oai-spgwc --network prod-oai-public-net --ip 192.168.61.4
             --env-file ./spgwc-env.list oai-spgwc:production
```

**TBD** : add logs command.

## 2.5. Deploying OAI-SPGWU-TINY container ##

```bash
$ python3 component/oai-spgwu-tiny/ci-scripts/generateConfigFiles.py --kind=SPGW-U \
          --sxc_ip_addr=192.168.61.4 --sxu=eth0 --s1u=eth0 \
          --from_docker_file --env_for_entrypoint
```

With this python script, we are generating a `spgwu-env.list` file. Now we can start the container.

```bash
$ docker run --privileged --name prod-oai-spgwu-tiny --network prod-oai-public-net --ip 192.168.61.5
             --env-file ./spgwu-env.list oai-spgwu-tiny:production
```

**TBD** : add logs command.
