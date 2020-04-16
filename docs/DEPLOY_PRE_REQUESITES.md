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

# 1. Install the proper version of Docker #

At time of writing (2020 / 04 / 16):

```bash
$ dpkg --list | grep docker
ii  docker-ce                             5:19.03.6~3-0~ubuntu-bionic                     amd64        Docker: the open-source application container engine
ii  docker-ce-cli                         5:19.03.6~3-0~ubuntu-bionic                     amd64        Docker CLI: the open-source application container engine
```

# 2. Create an account on Docker Hub #

Go to [https://hub.docker.com/](https://hub.docker.com/) website and create an account.

# 3. Pull base images #

We need 2 base images: `ubuntu:bionic` and `cassandra:2.1`

First log with your Docker Hub credentials.

```bash
$ docker login
Login with your Docker ID to push and pull images from Docker Hub. If you don't have a Docker ID, head over to https://hub.docker.com to create one.
Username: 
Password: 
```

Then pull base images.

```bash
$ docker pull ubuntu:bionic
$ docker pull cassandra:2.1
```

Finally you may logoff --> your token is stored in plain text..

```bash
$ docker logout
```

# 4. Network Configuration #

The docker bridge might be by default on an already used IP range. That was the case in our network.

So we picked a new IP range by adding a `/etc/docker/daemon.json` file:

```json
{
	"bip": "192.168.17.1/24",
}
```

Restart the docker daemon and check the new network configuration:

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

Based on this [recommendation](https://docs.docker.com/network/bridge/#enable-forwarding-from-docker-containers-to-the-outside-world):

```bash
$ sudo sysctl net.ipv4.conf.all.forwarding=1
$ sudo iptables -P FORWARD ACCEPT
```

You are ready to [build the images](./BUILD_IMAGES.md).

