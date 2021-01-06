<table style="border-collapse: collapse; border: none;">
  <tr style="border-collapse: collapse; border: none;">
    <td style="border-collapse: collapse; border: none;">
      <a href="http://www.openairinterface.org/">
         <img src="../docs/images/oai_final_logo.png" alt="" border=3 height=50 width=150>
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
$ cd docker-compose
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
