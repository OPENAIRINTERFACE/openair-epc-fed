<table style="border-collapse: collapse; border: none;">
  <tr style="border-collapse: collapse; border: none;">
    <td style="border-collapse: collapse; border: none;">
      <a href="http://www.openairinterface.org/">
         <img src="../../docs/images/oai_final_logo.png" alt="" border=3 height=50 width=150>
         </img>
      </a>
    </td>
    <td style="border-collapse: collapse; border: none; vertical-align: center;">
      <b><font size = "5">OpenAirInterface Core Network Docker Deployment : a Docker-Compose example</font></b>
    </td>
  </tr>
</table>

# Initialize the Cassandra DB #

Starting and initializing a data-base takes a bit of time.

In `docker-compose 3.x`, there are no more support for conditional healthy dependency when deploying.

This step is now **manual**.

```bash
$ cd docker-compose/oai-mme-legacy
$ docker-compose up -d db_init
Creating network "prod-oai-private-net" with the default driver
Creating network "prod-oai-public-net" with the default driver
Creating prod-cassandra ... done
Creating prod-db-init   ... done

$ docker logs prod-db-init --follow
Connection error: ('Unable to connect to any servers', {'192.168.68.2': error(111, "Tried connecting to [('192.168.68.2', 9042)]. Last error: Connection refused")})
Connection error: ('Unable to connect to any servers', {'192.168.68.2': error(111, "Tried connecting to [('192.168.68.2', 9042)]. Last error: Connection refused")})
Connection error: ('Unable to connect to any servers', {'192.168.68.2': error(111, "Tried connecting to [('192.168.68.2', 9042)]. Last error: Connection refused")})
Connection error: ('Unable to connect to any servers', {'192.168.68.2': error(111, "Tried connecting to [('192.168.68.2', 9042)]. Last error: Connection refused")})
OK

$ docker rm -f prod-db-init
prod-db-init
```

Note: we are removing the `prod-db-init` container because it is not needed anymore.

You can keep the container but it is dead.

To go to the next step, you **SHALL** have the "OK" message in the `prod-db-init` container logs.

# Deploy the rest of EPC #

```bash
$ docker-compose up -d oai_spgwu
prod-cassandra is up-to-date
Creating prod-oai-hss ... done
Creating prod-oai-mme ... done
Creating prod-oai-spgwc ... done
Creating prod-oai-spgwu-tiny ... done

# wait a bit

$ docker ps -a
CONTAINER ID        IMAGE                       COMMAND                  CREATED             STATUS                    PORTS                                         NAMES
124beeee2bd4        oai-spgwu-tiny:production   "/openair-spgwu-tiny…"   18 seconds ago      Up 15 seconds (healthy)   2152/udp, 8805/udp                            prod-oai-spgwu-tiny
c0d884650cd9        oai-spgwc:production        "/openair-spgwc/bin/…"   21 seconds ago      Up 18 seconds (healthy)   2123/udp, 8805/udp                            prod-oai-spgwc
0188a5ac505c        oai-mme:production          "/openair-mme/bin/en…"   23 seconds ago      Up 20 seconds (healthy)   3870/tcp, 2123/udp, 5870/tcp                  prod-oai-mme
06e6eff74762        oai-hss:production          "/openair-hss/bin/en…"   26 seconds ago      Up 22 seconds (healthy)   5868/tcp, 9042/tcp, 9080-9081/tcp             prod-oai-hss
514e5e3171b5        cassandra:2.1               "docker-entrypoint.s…"   3 minutes ago       Up 3 minutes (healthy)    7000-7001/tcp, 7199/tcp, 9042/tcp, 9160/tcp   prod-cassandra

```

# Undeploy

```
$ docker-compose down
Stopping prod-oai-spgwu-tiny ... done
Stopping prod-oai-spgwc      ... done
Stopping prod-oai-mme        ... done
Stopping prod-oai-hss        ... done
Stopping prod-cassandra      ... done
Removing prod-oai-spgwu-tiny ... done
Removing prod-oai-spgwc      ... done
Removing prod-oai-mme        ... done
Removing prod-oai-hss        ... done
Removing prod-cassandra      ... done
Removing network prod-oai-private-net
Removing network prod-oai-public-net
```

# How to edit the docker-compose file

Obviously you want an EPC that runs for your environment. It means:

*  Dedicated UE simcard configuration
*  A different PLMN
*  Your network configuration is certainly different

**Try to modify as little as possible the number of environment variables values in the docker-compose file.**

The variables I describe in the next few sections should be the ones you shall focus on!

* They are formatted in this markdown page as **<code>ENV_VARIABLE</code>**

If you don't understand a value, it is better to **NOT** touch it!

## UE simcard and other UE configurations

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

## Your Public Land Mobile Network (PLMN)

I strongly recommend to only modify the **MCC**-type and **MNC**-type parameters.

You could touch the **TAC**-type ones but it's quite more difficult for a simple tutorial.

In our example, we used **208** and **96** with TACs **1**, **2**, **3** (**1** being primary TAC).

**CAUTION** : for **MCC**, **MNC** values, I am using a `'` -- 2 or 3 digits -- `'` notation:

- I do this especially if your **MNC** is something like **'02'**, 2 digits with 1st being '0'
- This 1st `zero` digit **SHALL** present in all of the cNF configuration files!

Note that the **MNC3**-type parameters are encoded over 3 characters. This is mandatory.
You have to fill with `zeroes` if needed.

For the **MME**:

* **<code>MCC</code>**
* **<code>MNC</code>**
* **<code>TAC_0</code>**
* **<code>MCC_SGW_0</code>**
* **<code>MNC3_SGW_0</code>**
* **<code>TAC_LB_SGW_0</code>**
* **<code>TAC_HB_SGW_0</code>**

For the **SPGWC-C** and **SPGW-U-TINY**:

* **<code>MCC</code>**
* **<code>MNC</code>**
* **<code>MNC03</code>**
* **<code>TAC</code>**

**Last important point:** Your MME PLMN **SHALL** match the one in your eNB configuration!

For example, if you are using OAI eNB configuration file:

```bash
    tracking_area_code  =  1;
    plmn_list = (
      { mcc = 208; mnc = 96; mnc_length = 2; }
    );
```

## Your network configuration

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

# Time-Zone Settings #

You can specify the timezone at deployment time in each container.

Just modify **<code>TZ</code>** in each container section!

Note that by default at build I've set up `Europe/Paris`.

Proper values can be found in your Linux system at `/usr/share/zoneinfo/`.

# Connecting an eNB

The network configuration on eNB server(s) still is valid.

See [here](../../docs/CONFIGURE_NETWORKS.md#step-2-create-a-route-on-your-enbgnb-servers) for the commands to do

And see [here](../../docs/CONFIGURE_NETWORKS.md#verify-your-network-configuration) for commands to verify.
