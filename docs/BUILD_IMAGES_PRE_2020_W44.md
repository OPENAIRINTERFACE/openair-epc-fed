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

**CAUTION: if you are reading this page, it means you are using a version prior to 2020 week 44**

At the time of writing (2020 / 06 / 22), if you want to use the OpenAir-CN for a Dual Connectivity use case, you need to use proper branches:

**cNF Name** | **Branch Name** | **Commit at time of writing**              | Ubuntu18 | CentOS7 | CentOS8
------------ | --------------- | ------------------------------------------ | -------- | ------- | -------
HSS          | `develop`       | `cd10de54763368292831415ee6b6b6169f009f2e` | X        | X       | X
MME          | `develop`       | `7b19f50222283e9b4f4a86d3adadc719871abca5` | X        | X       | X
SPGW-C       | `develop`       | `9c2e49fe60351b69a7da1a898e4bbc0fd39dcc41` | X        |         | X
SPGW-U-TINY  | `develop`       | `c7927169b93456af59818d5682d66980bfee874d` | X        |         | X

Prior to 2020-06-19, the Dual-Connectivity case was supported in the `samsumg-s10-5g-g977u-merged` branch.

If the `samsumg-s10-5g-g977u-merged` branch does not exist when you try, it has been merged into `develop` branch of MME repository.

```bash
$ git clone https://github.com/OPENAIRINTERFACE/openair-epc-fed.git
$ cd openair-epc-fed
$ git checkout master
$ git pull origin master
$ ./scripts/syncComponents.sh --mme-branch samsumg-s10-5g-g977u-merged
---------------------------------------------------------
OAI-HSS    component branch : develop
OAI-MME    component branch : samsumg-s10-5g-g977u-merged
OAI-SPGW-C component branch : develop
OAI-SPGW-U component branch : develop
---------------------------------------------------------
....
```

**CAUTION: At the time of writing (2020 / 05 / 04), only HSS and MME have a full CentOS-7 support.**

It means that if you are on a CentOS 7 host, you will need to build a CentOS8 image of SPGW-C / SPGW-U-TINY.

# 2. Generic Parameters #

Here in our network configuration, we need to pass the "GIT PROXY" configuration.

*   If you do not need, remove the `--build-arg EURECOM_PROXY=".."` option.
*   If you do need it, change with your proxy value.

# 3. Build HSS Image #

## 3.1 On a Ubuntu 18.04 Host ##

```bash
$ docker build --target oai-hss --tag oai-hss:production \
               --file component/oai-hss/ci-scripts/Dockerfile.ubuntu18.04 \
               --build-arg EURECOM_PROXY="http://proxy.eurecom.fr:8080" .
$ docker image prune --force
$ docker image ls
oai-hss                 production             f478bafd7a06        1 minute ago          341MB
...
```

## 3.2 On a CentOS 7 Host ##

```bash
$ docker build --target oai-hss --tag oai-hss:production \
               --file component/oai-hss/ci-scripts/Dockerfile.centos7 .
$ docker image prune --force
$ docker image ls
oai-hss                 production             5b277bf98abe        1 minute ago          527MB
...
```

## 3.3 On a CentOS 8 Host ##

```bash
$ docker build --target oai-hss --tag oai-hss:production \
               --file component/oai-hss/ci-scripts/Dockerfile.centos8 .
$ docker image prune --force
$ docker image ls
oai-hss                 production             5fa77e2b6b94        1 minute ago          517MB
...
```

# 4. Build MME Image #

## 4.1 On a Ubuntu 18.04 Host ##

```bash
$ docker build --target oai-mme --tag oai-mme:production \
               --file component/oai-mme/ci-scripts/Dockerfile.ubuntu18.04 \
               --build-arg EURECOM_PROXY="http://proxy.eurecom.fr:8080" .
$ docker image prune --force
$ docker image ls
oai-mme                 prodution              45254be9f987        1 minute ago          256MB
...
```

## 4.2 On a CentOS 7 Host ##

```bash
$ docker build --target oai-mme --tag oai-mme:production \
               --file component/oai-mme/ci-scripts/Dockerfile.centos7 .
$ docker image prune --force
$ docker image ls
oai-mme                 prodution              4133e75b6fc4        1 minute ago          406MB
...
```

## 4.3 On a CentOS 8 Host ##

```bash
$ docker build --target oai-mme --tag oai-mme:production \
               --file component/oai-mme/ci-scripts/Dockerfile.centos8 .
$ docker image prune --force
$ docker image ls
oai-mme                 prodution              413cec7d8f3b        1 minute ago          412MB
...
```

# 5. Build SPGW-C Image #

## 5.1 On a Ubuntu 18.04 Host ##

```bash
$ docker build --target oai-spgwc --tag oai-spgwc:production \
               --file component/oai-spgwc/ci-scripts/Dockerfile.ubuntu18.04 \
               --build-arg EURECOM_PROXY="http://proxy.eurecom.fr:8080" .
$ docker image prune --force
$ docker image ls
oai-spgwc               production             b1ba7dd16bc5        1 minute ago          218MB
...
```

## 5.2 On a CentOS 7/8 Host ##

**Even if we are on a CentOS7 host, we build the SPGW-C image using the CentOS-8 dockerfile.**

```bash
$ docker build --target oai-spgwc --tag oai-spgwc:production \
               --file component/oai-spgwc/ci-scripts/Dockerfile.centos8 .
$ docker image prune --force
$ docker image ls
oai-spgwc               production             15ad64676b1f        1 minute ago          379MB
...
```

# 6, Build SPGW-U Image #

## 6.1 On a Ubuntu 18.04 Host ##

```bash
$ docker build --target oai-spgwu-tiny --tag oai-spgwu-tiny:production \
               --file component/oai-spgwu-tiny/ci-scripts/Dockerfile.ubuntu18.04 \
               --build-arg EURECOM_PROXY="http://proxy.eurecom.fr:8080" .
$ docker image prune --force
$ docker image ls
oai-spgwu-tiny          production             588e14481f2b        1 minute ago          220MB
...
```

## 6.2 On a CentOS 7/8 Host ##

**Even if we are on a CentOS7 host, we build the SPGW-U image using the CentOS-8 dockerfile.**

```bash
$ docker build --target oai-spgwu-tiny --tag oai-spgwu-tiny:production \
               --file component/oai-spgwu-tiny/ci-scripts/Dockerfile.centos8 .
$ docker image prune --force
$ docker image ls
oai-spgwu-tiny          production             f2d0a07fba2c        1 minute ago          378MB
...
```

You are ready to [Configure the Containers](./CONFIGURE_CONTAINERS_PRE_2020_W44.md).

