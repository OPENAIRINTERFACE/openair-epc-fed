<table style="border-collapse: collapse; border: none;">
  <tr style="border-collapse: collapse; border: none;">
    <td style="border-collapse: collapse; border: none;">
      <a href="http://www.openairinterface.org/">
         <img src="./images/oai_final_logo.png" alt="" border=3 height=50 width=150>
         </img>
      </a>
    </td>
    <td style="border-collapse: collapse; border: none; vertical-align: center;">
      <b><font size = "5">OpenAirInterface Core Network Docker Deployment : Pre-Requisites for MAGMA-MME + OAI CN</font></b>
    </td>
  </tr>
</table>

# 1. Install the proper version of Docker #

At time of writing (2021 / 02 / 01):

```bash
$ dpkg --list | grep docker
ii  docker-ce                              5:20.10.2~3-0~ubuntu-bionic                     amd64        Docker: the open-source application container engine
ii  docker-ce-cli                          5:20.10.2~3-0~ubuntu-bionic                     amd64        Docker CLI: the open-source application container engine
ii  docker-ce-rootless-extras              5:20.10.2~3-0~ubuntu-bionic                     amd64        Rootless support for Docker.
```

**CAUTION: do not forget to add your username to the `docker` group**

Otherwise you will have to run in `sudo` mode.

```bash
$ sudo usermod -a -G docker myusername
```

**CAUTION: At time of writing (2021 / 02 / 01), we only support Ubuntu18.04 deployment.**

Please refer to the official [docker engine installation guide page](https://docs.docker.com/engine/install/).

You will get more details than here.

## 1.1. Install a recent version of `docker-compose` ##

Official [installation guide](https://docs.docker.com/compose/install/).

We recommend a version newer than `1.27`.

# 2. Create an account on Docker Hub #

Go to [https://hub.docker.com/](https://hub.docker.com/) website and create an account.

# 3. Pull base images #

* Ubuntu  version: We need 3 base images: `ubuntu:bionic`, `cassandra:2.1` and `redis:6.0.5`

First log with your Docker Hub credentials.

```bash
$ docker login
Login with your Docker ID to push and pull images from Docker Hub. If you don't have a Docker ID, head over to https://hub.docker.com to create one.
Username: 
Password: 
```

Then pull base images.

On a Ubuntu18.04 host:

```bash
$ docker pull ubuntu:bionic
$ docker pull cassandra:2.1
$ docker pull redis:6.0.5
```

Finally you may logoff --> your token is stored in plain text..

```bash
$ docker logout
```

# 4. Network Configuration #

**CAUTION: THIS FIRST STEP IS MANDATORY**

Based on this [recommendation](https://docs.docker.com/network/bridge/#enable-forwarding-from-docker-containers-to-the-outside-world):

```bash
$ sudo sysctl net.ipv4.conf.all.forwarding=1
$ sudo iptables -P FORWARD ACCEPT
```

**CAUTION: THIS SECOND STEP MAY NOT BE NEEDED IN YOUR ENVIRONMENT.**

* The default docker network (ie "bridge") is on "172.17.0.0/16" range.
* In our Eurecom private network, this IP address range is already in use.
  - We have to change it to another IP range is free in our private network configuration.
  - We picked a **new/IDLE** IP range by adding a `/etc/docker/daemon.json` file:

```json
{
	"bip": "192.168.17.1/24"
}
```

Restart the docker daemon:

```bash
$ sudo service docker restart
$ docker info
```

Check the new network configuration:

```bash
$ docker network inspect bridge
[
    {
        "Name": "bridge",
....
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": null,
            "Config": [
                {
                    "Subnet": "192.168.17.1/24",
                    "Gateway": "192.168.17.1"
                }
            ]
        },
....
```

You are ready to [build the images (including MAGMA-MME)](./BUILD_IMAGES_MAGMA_MME.md).

