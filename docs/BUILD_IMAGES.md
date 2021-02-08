<table style="border-collapse: collapse; border: none;">
  <tr style="border-collapse: collapse; border: none;">
    <td style="border-collapse: collapse; border: none;">
      <a href="http://www.openairinterface.org/">
         <img src="./images/oai_final_logo.png" alt="" border=3 height=50 width=150>
         </img>
      </a>
    </td>
    <td style="border-collapse: collapse; border: none; vertical-align: center;">
      <b><font size = "5">OpenAirInterface Core Network Docker Deployment : Building the Images</font></b>
    </td>
  </tr>
</table>

# 1.  Retrieve the proper code version #

At the time of writing (2020 / 10 / 27), if you want to use the OpenAir-CN for a Dual Connectivity use case, you need to use proper branches:

**UPDATE: 2021/02/08 --> this tutorial is still valid for the following tags**

**For later tags, please refer to the MAGMA-based tutorial.**

**cNF Name** | **Branch Name** | **Tags**   | **Commit at time of writing**              | Ubuntu18 | CentOS7 | CentOS8
------------ | --------------- | ---------- | ------------------------------------------ | -------- | ------- | -------
HSS          | `develop`       | `2021.w03` | `9ed4f34fd73d674cd96eaeb5730d9dbda098b0a1` | X        | X       | X
HSS          | `master`        | `v1.1.1`   | `1699b6a1565aa8df925dd04b5d632b49ebf24fc8` | X        | X       | X
MME          | `develop`       | `2020.w47` | `82b11abbd83a346bae220517f09fe8e4233db76b` | X        | X       | X
SPGW-C       | `develop`       | `2021.w04` | `ab1d7f17ac632f06af9ef27f4fb85541051bf974` | X        |         | X
SPGW-C       | `master`        | `v1.1.0`   | `79378aeedebec30f66d6f7783d90103686f4fabb` | X        |         | X
SPGW-U-TINY  | `develop`       | `2021.w03` | `e128259dde256e545ff947d177d82dd597c5a483` | X        |         | X
SPGW-U-TINY  | `master`        | `v1.1.0`   | `c6c4e189d4ec32f84a326af39e37ecd32e962022` | X        |         | X

```bash
$ git clone https://github.com/OPENAIRINTERFACE/openair-epc-fed.git
$ cd openair-epc-fed
$ git checkout 2021.w06
$ ./scripts/syncComponents.sh --hss-branch v1.1.1 --mme-branch 2020.w47 \
                              --spgwc-branch v1.1.0 --spgwu-tiny-branch v1.1.0
---------------------------------------------------------
OAI-HSS    component branch : v1.1.1
OAI-MME    component branch : 2020.w47
OAI-SPGW-C component branch : v1.1.0
OAI-SPGW-U component branch : v1.1.0
---------------------------------------------------------
....
```

**CAUTION: At the time of writing (2020 / 10 / 26), only HSS and MME have a full CentOS-7 support.**

It means that if you are on a CentOS 7 host, you will need to build a CentOS8 image of SPGW-C / SPGW-U-TINY.

**CAUTION: if you are using `develop` branches that are prior to 2020 week 44, please read [this page](./BUILD_IMAGES_PRE_2020_W44.md) instead.**

# 2. Generic Parameters #

Here in our network configuration, we need to pass the "GIT PROXY" configuration.

*   If you do not need, remove the `--build-arg EURECOM_PROXY=".."` option.
*   If you do need it, change with your proxy value.

**CAUTION: the location of the dockerfiles HAVE CHANGED.**

# 3. Build HSS Image #

## 3.1 On a Ubuntu 18.04 Host ##

```bash
$ docker build --target oai-hss --tag oai-hss:production \
               --file component/oai-hss/docker/Dockerfile.ubuntu18.04 \
               --build-arg EURECOM_PROXY="http://proxy.eurecom.fr:8080" component/oai-hss
$ docker image prune --force
$ docker image ls
oai-hss                 production             f478bafd7a06        1 minute ago          341MB
...
```

## 3.2 On a CentOS 7 Host ##

```bash
$ docker build --target oai-hss --tag oai-hss:production \
               --file component/oai-hss/docker/Dockerfile.centos7 component/oai-hss
$ docker image prune --force
$ docker image ls
oai-hss                 production             5b277bf98abe        1 minute ago          527MB
...
```

## 3.3 On a CentOS 8 Host ##

```bash
$ docker build --target oai-hss --tag oai-hss:production \
               --file component/oai-hss/docker/Dockerfile.centos8 component/oai-hss
$ docker image prune --force
$ docker image ls
oai-hss                 production             5fa77e2b6b94        1 minute ago          517MB
...
```

# 4. Build MME Image #

## 4.1 On a Ubuntu 18.04 Host ##

```bash
$ docker build --target oai-mme --tag oai-mme:production \
               --file component/oai-mme/docker/Dockerfile.ubuntu18.04 \
               --build-arg EURECOM_PROXY="http://proxy.eurecom.fr:8080" component/oai-mme
$ docker image prune --force
$ docker image ls
oai-mme                 prodution              45254be9f987        1 minute ago          256MB
...
```

## 4.2 On a CentOS 7 Host ##

```bash
$ docker build --target oai-mme --tag oai-mme:production \
               --file component/oai-mme/docker/Dockerfile.centos7 component/oai-mme
$ docker image prune --force
$ docker image ls
oai-mme                 prodution              4133e75b6fc4        1 minute ago          406MB
...
```

## 4.3 On a CentOS 8 Host ##

```bash
$ docker build --target oai-mme --tag oai-mme:production \
               --file component/oai-mme/docker/Dockerfile.centos8 component/oai-mme
$ docker image prune --force
$ docker image ls
oai-mme                 prodution              413cec7d8f3b        1 minute ago          412MB
...
```

# 5. Build SPGW-C Image #

## 5.1 On a Ubuntu 18.04 Host ##

```bash
$ docker build --target oai-spgwc --tag oai-spgwc:production \
               --file component/oai-spgwc/docker/Dockerfile.ubuntu18.04 \
               --build-arg EURECOM_PROXY="http://proxy.eurecom.fr:8080" component/oai-spgwc
$ docker image prune --force
$ docker image ls
oai-spgwc               production             b1ba7dd16bc5        1 minute ago          218MB
...
```

## 5.2 On a CentOS 7/8 Host ##

**Even if we are on a CentOS7 host, we build the SPGW-C image using the CentOS-8 dockerfile.**

```bash
$ docker build --target oai-spgwc --tag oai-spgwc:production \
               --file component/oai-spgwc/docker/Dockerfile.centos8 component/oai-spgwc
$ docker image prune --force
$ docker image ls
oai-spgwc               production             15ad64676b1f        1 minute ago          379MB
...
```

# 6, Build SPGW-U Image #

## 6.1 On a Ubuntu 18.04 Host ##

```bash
$ docker build --target oai-spgwu-tiny --tag oai-spgwu-tiny:production \
               --file component/oai-spgwu-tiny/docker/Dockerfile.ubuntu18.04 \
               --build-arg EURECOM_PROXY="http://proxy.eurecom.fr:8080" component/oai-spgwu-tiny
$ docker image prune --force
$ docker image ls
oai-spgwu-tiny          production             588e14481f2b        1 minute ago          220MB
...
```

## 6.2 On a CentOS 7/8 Host ##

**Even if we are on a CentOS7 host, we build the SPGW-U image using the CentOS-8 dockerfile.**

```bash
$ docker build --target oai-spgwu-tiny --tag oai-spgwu-tiny:production \
               --file component/oai-spgwu-tiny/docker/Dockerfile.centos8 component/oai-spgwu-tiny
$ docker image prune --force
$ docker image ls
oai-spgwu-tiny          production             f2d0a07fba2c        1 minute ago          378MB
...
```

You are ready to [Configure the Containers](./CONFIGURE_CONTAINERS.md).

