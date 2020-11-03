<table style="border-collapse: collapse; border: none;">
  <tr style="border-collapse: collapse; border: none;">
    <td style="border-collapse: collapse; border: none;">
      <a href="http://www.openairinterface.org/">
         <img src="./images/oai_final_logo.png" alt="" border=3 height=50 width=150>
         </img>
      </a>
    </td>
    <td style="border-collapse: collapse; border: none; vertical-align: center;">
      <b><font size = "5">OpenAirInterface Core Network Docker Deployment : Generating Traffic</font></b>
    </td>
  </tr>
</table>

I will not explain here:

-  how to start/stop EPC nor
-  how to start/stop eNB or gNb nor
-  how to attach an UE

Once your UE is attached, you can either see if you have internet connection.

# 0. Common issues if your UE is connected but without any access to Internet #

## 0.1. Have you properly configured the DNS in SPGW-C ? ##

See [SPGWC Configure Section](./CONFIGURE_CONTAINERS.md#34-spgw-c)

**YOUR_DNS_IP_ADDRESS** shall have a correct value.

from your EPC **Docker Host**:

```bash
$ route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         192.168.21.179  0.0.0.0         UG    300    0        0 ens3
...
```

In this example, the DNS IP address is `192.168.21.179`.

## 0.2. May you need to enable "NATTING" on the UE pool ##

See [SPGWU Configure Section](./CONFIGURE_CONTAINERS.md#35-spgw-u)

Add the `--network_ue_nat_option=yes` option to the python command.

```bash
$ python3 component/oai-spgwu-tiny/ci-scripts/generateConfigFiles.py --kind=SPGW-U \
          ...
          --network_ue_nat_option=yes
```

## 0.3. Last trick: enable PUSH-PROTOCOL on SPGW-C. ##

See [SPGWC Configure Section](./CONFIGURE_CONTAINERS.md#34-spgw-c)

Add the `--push_protocol_option=yes` option to the python command.

```bash
$ python3 component/oai-spgwc/ci-scripts/generateConfigFiles.py --kind=SPGW-C \
          ...
          --push_protocol_option=yes
```

**But us for testing purposes (not use our Internet bandwidth) we prefer to manage traffic internally.**

# 1. Build a traffic generator image #

```bash
$ cd openair-epc-fed
$ cd ci-scripts
$ docker build --target trf-gen --tag trf-gen:production --file Dockerfile.traffic.generator.ubuntu18.04 .
$ docker image prune --force
$ docker image ls
trf-gen         production             bfdfe4e7ac51        1 minute ago      217MB
```

# 2. Instantiate a container #

```bash
$ docker run --privileged --name prod-trf-gen --network prod-oai-public-net -d trf-gen:production
```

# 3. Redirect the traffic from the UE Allocation pool(s) to SPGW-U container #

```bash
$ SPGWU_IP=`docker inspect --format="{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}" prod-oai-spgwu-tiny`
$ docker exec -it prod-trf-gen /bin/bash -c "ip route add 12.1.1.0/24 via ${SPGWU_IP} dev eth0"
```

# 4. Ping an attached UE #

```bash
$ docker exec -it prod-trf-gen /bin/bash -c "ping -c 20 12.1.1.2"
```

# 5. Iperf versions #

Depending on the `iperf` version that is installed on your UE, use:

```bash
$ docker exec -it prod-trf-gen /bin/bash -c "iperf --version"
iperf version 2.0.10 (2 June 2018) pthreads
$ docker exec -it prod-trf-gen /bin/bash -c "/iperf-2.0.5/bin/iperf --version"
iperf version 2.0.5 (08 Jul 2010) pthreads
```

