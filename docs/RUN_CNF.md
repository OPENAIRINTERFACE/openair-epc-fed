<table style="border-collapse: collapse; border: none;">
  <tr style="border-collapse: collapse; border: none;">
    <td style="border-collapse: collapse; border: none;">
      <a href="http://www.openairinterface.org/">
         <img src="./images/oai_final_logo.png" alt="" border=3 height=50 width=150>
         </img>
      </a>
    </td>
    <td style="border-collapse: collapse; border: none; vertical-align: center;">
      <b><font size = "5">OpenAirInterface Core Network Docker Deployment : Running it</font></b>
    </td>
  </tr>
</table>

# 1. Starting the Network Functions with tracing #

First launch `tshark` on each container. Not necessary, but useful if you want us to help debugging issues.

```bash
$ docker exec -d prod-oai-hss /bin/bash -c "nohup tshark -i eth0 -i eth1 -w /tmp/hss_check_run.pcap 2>&1 > /dev/null"
$ docker exec -d prod-oai-mme /bin/bash -c "nohup tshark -i eth0 -i lo:s10 -w /tmp/mme_check_run.pcap 2>&1 > /dev/null"
$ docker exec -d prod-oai-spgwc /bin/bash -c "nohup tshark -i eth0 -i lo:p5c -i lo:s5c -w /tmp/spgwc_check_run.pcap 2>&1 > /dev/null"
$ docker exec -d prod-oai-spgwu-tiny /bin/bash -c "nohup tshark -i eth0 -w /tmp/spgwu_check_run.pcap 2>&1 > /dev/null"
```

On **CentOS** images, we have installed `tcpdump` instead of `tshark`:

```bash
$ docker exec -d prod-oai-hss /bin/bash -c "nohup tcpdump -f "port not 22" -i any -w /tmp/hss_check_run.pcap 2>&1 > /dev/null"
$ docker exec -d prod-oai-mme /bin/bash -c "nohup tcpdump -f "port not 22" -i any -w /tmp/mme_check_run.pcap 2>&1 > /dev/null"
$ docker exec -d prod-oai-spgwc /bin/bash -c "nohup tcpdump -f "port not 22" -i any -w /tmp/spgwc_check_run.pcap 2>&1 > /dev/null"
$ docker exec -d prod-oai-spgwu-tiny /bin/bash -c "nohup tcpdump -f "port not 22" -i any -w /tmp/spgwu_check_run.pcap 2>&1 > /dev/null"
```

**THE ORDER OF LAUNCH MATTERS.**

```bash
$ docker exec -d prod-oai-hss /bin/bash -c "nohup ./bin/oai_hss -j ./etc/hss_rel14.json --reloadkey true > hss_check_run.log 2>&1"
$ sleep 2
$ docker exec -d prod-oai-mme /bin/bash -c "nohup ./bin/oai_mme -c ./etc/mme.conf > mme_check_run.log 2>&1"
$ sleep 2
$ docker exec -d prod-oai-spgwc /bin/bash -c "nohup ./bin/oai_spgwc -o -c ./etc/spgw_c.conf > spgwc_check_run.log 2>&1"
$ sleep 2
$ docker exec -d prod-oai-spgwu-tiny /bin/bash -c "nohup ./bin/oai_spgwu -o -c ./etc/spgw_u.conf > spgwu_check_run.log 2>&1"
```

# 2. Stopping #

```bash
$ docker exec -it prod-oai-hss /bin/bash -c "killall --signal SIGINT oai_hss tshark tcpdump"
$ docker exec -it prod-oai-mme /bin/bash -c "killall --signal SIGINT oai_mme tshark tcpdump"
$ docker exec -it prod-oai-spgwc /bin/bash -c "killall --signal SIGINT oai_spgwc tshark tcpdump"
$ docker exec -it prod-oai-spgwu-tiny /bin/bash -c "killall --signal SIGINT oai_spgwu tshark tcpdump"
$ sleep 10
$ docker exec -it prod-oai-hss /bin/bash -c "killall --signal SIGKILL oai_hss tshark tcpdump"
$ docker exec -it prod-oai-mme /bin/bash -c "killall --signal SIGKILL oai_mme tshark tcpdump"
$ docker exec -it prod-oai-spgwc /bin/bash -c "killall --signal SIGKILL oai_spgwc tshark tcpdump"
$ docker exec -it prod-oai-spgwu-tiny /bin/bash -c "killall --signal SIGKILL oai_spgwu tshark tcpdump"
```

# 3. Recovering logs, config and traces #

```bash
$ rm -Rf archives
$ mkdir -p archives/oai-hss-cfg archives/oai-mme-cfg archives/oai-spgwc-cfg archives/oai-spgwu-cfg
```

First retrieve the modified configuration files

```bash
$ docker cp prod-oai-hss:/openair-hss/etc/. archives/oai-hss-cfg
$ docker cp prod-oai-mme:/openair-mme/etc/. archives/oai-mme-cfg
$ docker cp prod-oai-spgwc:/openair-spgwc/etc/. archives/oai-spgwc-cfg
$ docker cp prod-oai-spgwu-tiny:/openair-spgwu-tiny/etc/. archives/oai-spgwu-cfg
```

Then the logs.

```bash
$ docker cp prod-oai-hss:/openair-hss/hss_check_run.log archives
$ docker cp prod-oai-mme:/openair-mme/mme_check_run.log archives
$ docker cp prod-oai-spgwc:/openair-spgwc/spgwc_check_run.log archives
$ docker cp prod-oai-spgwu-tiny:/openair-spgwu-tiny/spgwu_check_run.log archives
```

Finally the PCAP.

```bash
$ docker cp prod-oai-hss:/tmp/hss_check_run.pcap archives
$ docker cp prod-oai-mme:/tmp/mme_check_run.pcap archives
$ docker cp prod-oai-spgwc:/tmp/spgwc_check_run.pcap archives
$ docker cp prod-oai-spgwu-tiny:/tmp/spgwu_check_run.pcap archives
```

Make a zip

```bash
$ zip -r -qq docker_files.zip archives
```

# 4. Notes

After a few hours of running, we see that MME crashes (refusing to attach UE).

Just stop, start MME, SPGW-\*.

You are ready to [generate some traffic](./GENERATE_TRAFFIC.md).


