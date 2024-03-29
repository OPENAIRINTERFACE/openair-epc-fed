<table style="border-collapse: collapse; border: none;">
  <tr style="border-collapse: collapse; border: none;">
    <td style="border-collapse: collapse; border: none;">
      <a href="http://www.openairinterface.org/">
         <img src="../../docs/images/oai_final_logo.png" alt="" border=3 height=50 width=150>
         </img>
      </a>
    </td>
    <td style="border-collapse: collapse; border: none; vertical-align: center;">
      <b><font size = "5">OpenAirInterface Core Network Docker Deployment : a Docker-Compose MAGMA-MME example</font></b>
    </td>
  </tr>
</table>

**Table of Contents**

1.  [Initialize the Cassandra Database](#1-initialize-the-cassandra-db)
2.  [Deploy the rest of EPC](#2-deploy-the-rest-of-epc)
3.  [Undeploy the EPC](#3-undeploy-the-epc)
4.  [How to edit the docker-compose file](#4-how-to-edit-the-docker-compose-file)
    1.  [UE simcard and other UE configurations](#41-ue-simcard-and-other-ue-configurations)
    2.  [Your Public Land Mobile Network](#42-your-public-land-mobile-network)
    3.  [Your network configuration](#43-your-network-configuration)
    4.  [Miscellaneous](#44-miscellaneous)
5.  [Connecting an eNB](#5-connecting-an-enb)
6.  [Connecting a Smartphone in 5G using NSA support from OAI RAN](#6-connecting-a-smartphone-in-5g-using-nsa-support-from-oai-ran)

# 1. Initialize the Cassandra DB #

Starting and initializing a data-base takes a bit of time.

In `docker-compose 3.x`, there are no more support for conditional healthy dependency when deploying.

This step is now **manual**.

```bash
$ cd docker-compose/magma-mme-demo
$ docker-compose up -d db_init
Creating network "demo-oai-private-net" with the default driver
Creating network "demo-oai-public-net" with the default driver
Creating demo-cassandra ... done
Creating demo-db-init   ... done

$ docker logs demo-db-init --follow
Connection error: ('Unable to connect to any servers', {'192.168.68.130': error(111, "Tried connecting to [('192.168.68.130', 9042)]. Last error: Connection refused")})
Connection error: ('Unable to connect to any servers', {'192.168.68.130': error(111, "Tried connecting to [('192.168.68.130', 9042)]. Last error: Connection refused")})
Connection error: ('Unable to connect to any servers', {'192.168.68.130': error(111, "Tried connecting to [('192.168.68.130', 9042)]. Last error: Connection refused")})
Connection error: ('Unable to connect to any servers', {'192.168.68.130': error(111, "Tried connecting to [('192.168.68.130', 9042)]. Last error: Connection refused")})
OK

$ docker rm -f demo-db-init
demo-db-init
```

Note: we are removing the `demo-db-init` container because it is not needed anymore.

You can keep the container but it is dead.

To go to the next step, you **SHALL** have the "OK" message in the `demo-db-init` container logs.

Wait a bit to ensure that the following logs are present in launching the cassandra docker image. If its not the case, the HSS docker image will stop in the next step prematurely.

```bash
$ docker logs demo-cassandra
....
INFO  20:19:40 Initializing vhss.extid_imsi_xref
```


# 2. Deploy the rest of EPC #

```bash
$ docker-compose up -d oai_spgwu
demo-cassandra is up-to-date
Creating demo-redis   ... done
Creating demo-oai-hss ... done
Creating demo-magma-mme ... done
Creating demo-oai-spgwc ... done
Creating demo-oai-spgwu-tiny ... done

# wait a bit

$ docker ps -a
CONTAINER ID        IMAGE                       COMMAND                  CREATED             STATUS                    PORTS                                         NAMES
cf93fa4c5fdf        oai-spgwu-tiny:production   "/openair-spgwu-tiny…"   46 seconds ago      Up 44 seconds (healthy)   2152/udp, 8805/udp                            demo-oai-spgwu-tiny
f59ceac1dba5        oai-spgwc:production        "/openair-spgwc/bin/…"   49 seconds ago      Up 46 seconds (healthy)   2123/udp, 8805/udp                            demo-oai-spgwc
80d71373ef4d        magma-mme:nsa-support       "/bin/bash -c 'cd /m…"   51 seconds ago      Up 49 seconds             3870/tcp, 2123/udp, 5870/tcp                  demo-magma-mme
7b2f67eeeac0        oai-hss:production          "/openair-hss/bin/en…"   56 seconds ago      Up 51 seconds (healthy)   5868/tcp, 9042/tcp, 9080-9081/tcp             demo-oai-hss
b94d74330f92        redis:6.0.5                 "/bin/bash -c 'redis…"   56 seconds ago      Up 52 seconds             6379/tcp                                      demo-redis
e51afc6e107c        cassandra:2.1               "docker-entrypoint.s…"   2 minutes ago       Up 2 minutes (healthy)    7000-7001/tcp, 7199/tcp, 9042/tcp, 9160/tcp   demo-cassandra

```

You are ready to connect the RAN and UE.

# 3. Undeploy the EPC #

```
$ docker-compose down
Stopping demo-oai-spgwu-tiny ... done
Stopping demo-oai-spgwc      ... done
Stopping demo-magma-mme      ... done
Stopping demo-oai-hss        ... done
Stopping demo-redis          ... done
Stopping demo-cassandra      ... done
Removing demo-oai-spgwu-tiny ... done
Removing demo-oai-spgwc      ... done
Removing demo-magma-mme      ... done
Removing demo-oai-hss        ... done
Removing demo-redis          ... done
Removing demo-cassandra      ... done
Removing network demo-oai-private-net
Removing network demo-oai-public-net
```

# 4. How to edit the docker-compose file

Obviously you want an EPC that runs for your environment. It means:

*  Dedicated UE simcard configuration
*  A different PLMN
*  Your network configuration is certainly different

**Try to modify as little as possible the number of environment variables values in the docker-compose file.**

The variables I describe in the next few sections should be the ones you shall focus on!

* They are formatted in this markdown page as **<code>ENV_VARIABLE</code>**

If you don't understand a value, it is better to **NOT** touch it!

## 4.1. UE simcard and other UE configurations ##

The final purpose of deploying an EPC is to connect a 4G UE (smartphone or dongle) to internet through an eNB.

When "burning" a simcard, you need to decide the following parameters:

* **IMSI** : International Mobile Subscriber Identity
  * Formatting is explained [here](https://en.wikipedia.org/wiki/International_mobile_subscriber_identity)
* **LTE_KEY** and **OPC_KEY**
* There are more but I won't go into details.

Once you've done this, put the simcard in your smartphone and power up it. You will need to add an new **APN** (Access Point Name).

Here you can be creative. It's a string. Our only requirement --> It **SHALL** have at least one "." (dot). In our example "oai.ipv4".

Now you need to provision the user(s) into the Cassandra Database, hence some of the **HSS** parameters:

* **<code>LTE_K</code>** SHALL match **LTE_KEY** you used in burning the simcard
* **<code>OP_KEY</code>** **is not** the **OPC_KEY** but it can be calculated from it and **LTE_KEY**.
  * A example of a generator can be found at [Ki/OPc Generator](https://github.com/PodgroupConnectivity/kiopcgenerator)
* **<code>APN1</code>** SHALL match the one you created on your smartphone.
* **<code>FIRST_IMSI</code>** should match the one you chose

The **SPGW-C**, since the introduction of FDQN support, has 2 variables:

* **<code>APN_NI_1</code>**
* **<code>DEFAULT_APN_NI_1</code>**

that shall match also the APN you created.

## 4.2. Your Public Land Mobile Network ##

AKA PLMN.

I strongly recommend to only modify the **MCC**-type and **MNC**-type parameters.

You could touch the **TAC**-type ones but it's quite more difficult for a simple tutorial.

In our example, we used **222** and **01** with TACs **1**, **2**, **3** (**1** being primary TAC).

**CAUTION** : for **MCC**, **MNC** values, I am using a `'` -- 2 or 3 digits -- `'` notation:

- I do this especially if your **MNC** is something like **'02'**, 2 digits with 1st being '0'
- This 1st `zero` digit **SHALL** present in all of the cNF configuration files!

Note that the **MNC3**-type parameters are encoded over 3 characters. This is mandatory.
You have to fill with `zeroes` if needed.

For the **MME**, at the time of writing, the configuration file is hard-coded in the same folder as the docker-compose file (`mme.conf`):

```bash
    # ------- MME served GUMMEIs
    GUMMEI_LIST = (
         { MCC="222" ; MNC="01"; MME_GID="32768" ; MME_CODE="3"; }
    );

    # ------- MME served TAIs
    TAI_LIST = (
         {MCC="222" ; MNC="01";  TAC = "1"; },
         {MCC="222" ; MNC="01";  TAC = "2"; },
         {MCC="222" ; MNC="01";  TAC = "3"; }
    );

    TAC_LIST = (
         {MCC="222" ; MNC="01";  TAC = "1"; }
    );

    CSFB :
    {
        NON_EPS_SERVICE_CONTROL = "OFF";
        CSFB_MCC = "222";
        CSFB_MNC = "01";
        LAC = "1";
    };
```

For the **SPGWC-C** and **SPGW-U-TINY** section of the docker-compose file:

* **<code>MCC</code>**
* **<code>MNC</code>**
* **<code>MNC03</code>**
* **<code>TAC</code>**

**Last important point:** Your MME PLMN **SHALL** match the one in your eNB configuration!

For example, if you are using OAI eNB configuration file:

```bash
    tracking_area_code  =  1;
    plmn_list = (
      { mcc = 222; mnc = 01; mnc_length = 2; }
    );
```

## 4.3. Your network configuration ##

### DNS Settings ###

Your EPC Docker host has its own gateway --> you need to provide it as "Local DNS server".

**Otherwise** you won't have Internet access on your UE when it is connected to the Core Network!

On your EPC docker host, type:

```bash
$ route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         192.168.18.129  0.0.0.0         UG    300    0        0 nm-bond
....
```

In the **SPGW-C** section of the docker-compose file.

Use the 2nd field value as **<code>DEFAULT_DNS_IPV4_ADDRESS</code>** field.

In our example, as **<code>DEFAULT_DNS_SEC_IPV4_ADDRESS</code>** we are using Google's 2nd one. You can pick anything else.

You can also ask your IT team!

You can tweak with the following 2 variables (but they are already at best values):

* **<code>PUSH_PROTOCOL_OPTION</code>**
* **<code>NETWORK_UE_NAT_OPTION</code>**

### the UE IP address allocation pool ###

Last point: the UE IP address allocation pool is used to assign an IP address to the UE when it gets connected.

In our example, I chose "12.1.1.2 - 12.1.1.254" range.

Note that it is also defined in **CICDR** format for SPGW-U "12.1.1.0/24"

If you have to change, please respect both formats.

**SPGW-C** section of docker-compose file:

* **<code>UE_IP_ADDRESS_POOL_1</code>**

**SPGW-U-TINY** section of docker-compose file:

* **<code>NETWORK_UE_IP</code>**

## 4.4. Miscellaneous ##

At the time of writing (2021 / 02 / 01), the automation on the MAGMA-MME image is not completed.

There are no entry-point scripts, no default MME configuration file.

Hence there are 2 files in this folder:

- `mme-cfg.sh` that behaves as `entrypoint`
- `mme.conf` already completed MME configuration file

Both files do have pre-filled parameters such realm, IP addresses...

Be careful when modifying them.

Note that in the `mme.conf`, the **S6A** section has changed: the MME supports now the connection with an HSS entity in a different realm.

```bash
    S6A :
    {
        S6A_CONF                   = "/magma-mme/etc/mme_fd.conf"; # YOUR MME freeDiameter config file path
        HSS_HOSTNAME               = "hss.openairinterface.org";
        HSS_REALM                  = "openairinterface.org";
    };
```

### Time-Zone Settings ###

You can specify the timezone at deployment time in each container.

Just modify **<code>TZ</code>** in each container section!

Note that by default at build I've set up `Europe/Paris`.

Proper values can be found in your Linux system at `/usr/share/zoneinfo/`.

# 5. Connecting an eNB #

The network configuration on eNB server(s) still is valid.

See [here](../../docs/CONFIGURE_NETWORKS_MAGMA.md#step-2-create-a-route-on-your-enbgnb-servers) for the commands to do

And see [here](../../docs/CONFIGURE_NETWORKS_MAGMA.md#verify-your-network-configuration) for commands to verify.

# 6. Connecting a Smartphone in 5G using NSA support from OAI RAN #

This part explains the RAN-related section to the demo made during MAGMA-dev conference in February 3rd, 2021.
See [here](../../docs/NSA_SUPPORT_OAI_RAN.md)
