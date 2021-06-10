<table style="border-collapse: collapse; border: none;">
  <tr style="border-collapse: collapse; border: none;">
    <td style="border-collapse: collapse; border: none;">
      <a href="http://www.openairinterface.org/">
         <img src="./images/oai_final_logo.png" alt="" border=3 height=50 width=150>
         </img>
      </a>
    </td>
    <td style="border-collapse: collapse; border: none; vertical-align: center;">
      <b><font size = "5">OpenAirInterface Core Network Docker Deployment : Pre-Requisites </font></b>
    </td>
  </tr>
</table>

# 1. Install the proper version of `docker` #

At time of writing (2020 / 04 / 16):

```bash
$ dpkg --list | grep docker
ii  docker-ce                             5:19.03.6~3-0~ubuntu-bionic                     amd64        Docker: the open-source application container engine
ii  docker-ce-cli                         5:19.03.6~3-0~ubuntu-bionic                     amd64        Docker CLI: the open-source application container engine
```

Also python3 (at least 3.6) shall be installed.

```bash
$ python3 --version
Python 3.6.9
```

**CAUTION: do not forget to add your username to the `docker` group**

Otherwise you will have to run in `sudo` mode.

```bash
$ sudo usermod -a -G docker myusername
```

On Centos 7.7 host:

```bash
$ sudo yum install -y yum-utils
$ sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
$ sudo yum install docker-ce docker-ce-cli containerd.io
$ sudo systemctl start docker
$ docker info
```

Please refer to the official [docker engine installation guide page](https://docs.docker.com/engine/install/).

You will get more details than here.

## 1.1. Install a recent version of `docker-compose` ##

Official [installation guide](https://docs.docker.com/compose/install/).

We recommend a version newer than `1.27`.

# 2. Create an account on Docker Hub #

Go to [https://hub.docker.com/](https://hub.docker.com/) website and create an account.

# 3. Pull base images #

* Ubuntu  version: We need 2 base images: `ubuntu:bionic` and `cassandra:2.1`
* CentOS7 version: We need 3 base images: `centos:7`, `centos:8` and `cassandra:2.1`
* CentOS8 version: We need 2 base images: `centos:8` and `cassandra:2.1`

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
```

On a Centos 7.7 host:

```bash
$ docker pull centos:7
$ docker pull centos:8
$ docker pull cassandra:2.1
```

On a Centos 8 host:

```bash
$ docker pull centos:8
$ docker pull cassandra:2.1
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

You are ready to [build the images](./BUILD_IMAGES.md).

