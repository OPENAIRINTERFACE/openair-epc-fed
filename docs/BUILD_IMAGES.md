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

**CAUTION: 2021/02/08 --> the following tags were used.**

**cNF Name** | **Branch Name** | **Tags**   | **Commit at time of writing**              | Ubuntu18 | CentOS7 | CentOS8
------------ | --------------- | ---------- | ------------------------------------------ | -------- | ------- | -------
HSS          | `develop`       | `2021.w10` | `93dfcbca245ec97652c4d62ba3913a899d956d68` | X        | X       | X
MME          | `develop`       | `2020.w47` | `82b11abbd83a346bae220517f09fe8e4233db76b` | X        | X       | X
SPGW-C       | `develop`       | `2021.w10` | `b10256535e47ffb86c86a8581d9c50b1f380dcf5` | X        |         | X
SPGW-U-TINY  | `develop`       | `2021.w10` | `acd293e616f879f4dacead152c59384d1e533167` | X        |         | X

**UPDATE: 2021/05/04 --> I have modified the name of the sync script --> `syncComponentsLegacy.sh`.**

```bash
$ git clone https://github.com/OPENAIRINTERFACE/openair-epc-fed.git
$ cd openair-epc-fed

# You can specify a tag on the parent GIT repository such as `2021.w22`
$ git checkout 2021.w22
# Or you can sync to the latest version
$ git checkout master

# Then you need to resync the sub-modules (ie HSS, SPGW-CUPS, MME).
# You can specify:
#   ---  a valid tag (such as seen)
#   ---  a newer tag
#   ---  a branch to get the latest (`develop` being the latest stable)
#        Usually the better option is to specify `develop`

$ ./scripts/syncComponentsLegacy.sh --hss-branch 2021.w10 --mme-branch 2020.w47 \
                              --spgwc-branch 2021.w10 --spgwu-tiny-branch 2021.w10
---------------------------------------------------------
OAI-HSS    component branch : 2021.w10
OAI-MME    component branch : 2020.w47
OAI-SPGW-C component branch : 2021.w10
OAI-SPGW-U component branch : 2021.w10
---------------------------------------------------------

# Or to not specify anything
$ ./scripts/syncComponentsLegacy.sh
---------------------------------------------------------
OAI-HSS    component branch : develop
OAI-MME    component branch : develop
OAI-SPGW-C component branch : develop
OAI-SPGW-U component branch : develop
---------------------------------------------------------
....
```

In general, the `docker-compose` files (even in the tutorials) are up-to-date w/ `develop` latest commits in each sub-module.

**CAUTION: At the time of writing (2020 / 10 / 26), only HSS and MME have a full CentOS-7 support.**

It means that if you are on a CentOS 7 host, you will need to build a CentOS8 image of SPGW-C / SPGW-U-TINY.

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

To deploy: 

* [Using a docker-compose easier approach](../docker-compose/oai-mme-legacy/README.md) (RECOMMENDED)

