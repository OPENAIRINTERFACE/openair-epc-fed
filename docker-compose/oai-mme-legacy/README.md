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

You can keep but it is dead.

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

* **LTE_K** SHALL match **LTE_KEY** you used in burning the simcard
* **OP_KEY** **is not** the **OPC_KEY** but it can be calculated from it and **LTE_KEY**.
* **APN1** SHALL match the one you created on your smartphone.
* **FIRST_IMSI** should match the one you chose

The **SPGW-C** parameter **DEFAULT_APN** shall match also the APN you created.

## Your Public Land Mobile Network (PLMN)

I strongly recommend to only modify the **MCC**-type and **MNC**-type parameters.

You could touch the **TAC**-type ones but it's quite more difficult for a simple tutorial.

In our example, we used **222** and **01**. 

Note that the **MNC3**-type parameters are encoded over 3 characters. This is mandatory.

**Last important point:** Your MME PLMN **SHALL** match the one in your eNB configuration!

For example, if you are using OAI eNB configuration file:

```bash
    tracking_area_code  =  1;
    plmn_list = (
      { mcc = 222; mnc = 01; mnc_length = 2; }
    );
```

## Your network configuration

Your EPC Docker host has its own gateway --> you need to provide it as "Local DNS server".

On your EPC docker host, type:

```bash
$ route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         192.168.18.129  0.0.0.0         UG    300    0        0 nm-bond
....
```

Use the 2nd field value as **DEFAULT_DNS_IPV4_ADDRESS** field.

In our example, as **DEFAULT_DNS_SEC_IPV4_ADDRESS** we are using Google's 2nd one. You can pick anything else.

Last point: the UE IP address allocation pool. 

In our example, I chose "12.1.1.2 - 12.1.1.254" range.

Note that it is also defined in **CICDR** format for SPGW-U "12.1.1.0/24"

If you have to change, please respect both formats.

# Connecting an eNB

The network configuration on eNB server(s) still is valid.

See [here](../../docs/CONFIGURE_NETWORKS.md#step-2-create-a-route-on-your-enbgnb-servers) for the commands to do

And see [here](../../docs/CONFIGURE_NETWORKS.md#verify-your-network-configuration) for commands to verify.
