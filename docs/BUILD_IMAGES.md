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

**CAUTION: PLEASE READ THIS SECTION VERY CAREFULLY!**

This repository only has tutorials and Continuous Integration scripts.

Each 4G Network Function source code is managed in its own repository.

They are called as git sub-modules in the component folder.

Before doing anything, you SHALL retrieve the code for each git sub-module.

## 1.1. You are interested on a very stable version. ##

We recommend to synchronize with the master branches on all git sub-modules.

We also recommend that you synchronize this "tutorial" repository with a provided tag. By doing so, the `docker-compose` files will be aligned with feature sets of each NF.

**At the time of writing (2022/02/25), the release tag is v1.2.0.**

| CNF Name    | Branch Name | Tag        | Ubuntu 18.04 | RHEL8 (UBI8)    |
| ----------- | ----------- | ---------- | ------------ | ----------------|
| FED REPO    | N/A         | `v1.1.2`   |              |                 |
| HSS         | `master`    | `v1.1.2`   | X            | X               |
| SPWG-C      | `master`    | `v1.1.2`   | X            | X               |
| SPGW-U-TINY | `master`    | `v1.1.2`   | X            | X               |
| MAGMA-MME   | `master`    | `N/A`      | X            | X               |

```bash
# Clone directly on the latest release tag
$ git clone --branch v1.2.0 https://github.com/OPENAIRINTERFACE/openair-epc-fed.git
$ cd openair-epc-fed
# If you forgot to clone directly to the latest release tag
$ git checkout -f v1.2.0

# Synchronize all git submodules
$ ./scripts/syncComponents.sh
---------------------------------------------------------
OAI-HSS    component branch : master
OAI-SPGW-C component branch : master
OAI-SPGW-U component branch : master
---------------------------------------------------------
git submodule deinit --all --force
git submodule init
git submodule update
```

## 1.2. You are interested on the latest features. ##

All the latest features are somehow pushed to the `develop` branches of each NF repository.

It means that we/you are able to build and the Continuous Integration test suite makes sure it
does NOT break any existing tested feature.

Anyhow, the tutorials' docker-compose files on the latest commit of the `master` branch of
`openair-epc-fed` repository SHALL support any additional un-tested feature.

```bash
# Clone
$ git clone  https://gitlab.eurecom.fr/oai/cn5g/oai-cn5g-fed.git
$ cd oai-cn5g-fed
# On an existing repository, resync to the last `master` commit
$ git fetch --prune
$ git checkout master
$ git rebase origin/master

# Synchronize all git submodules
$ ./scripts/syncComponents.sh --hss-branch develop \
                              --spgwc-branch develop --spgwu-tiny-branch develop
---------------------------------------------------------
OAI-HSS    component branch : develop
OAI-SPGW-C component branch : develop
OAI-SPGW-U component branch : develop
---------------------------------------------------------
git submodule deinit --all --force
git submodule init
git submodule update
```

**CAUTION: At the time of writing (2020 / 10 / 26), only HSS and MME have a full CentOS-7 support.**

It means that if you are on a CentOS 7 host, you will need to build a CentOS8 image of SPGW-C / SPGW-U-TINY.

**CAUTION: (2021 / 07 / 28): CentOS dockerfiles are not part of the OAI CI process. They are certainly in need of maintenance.**

# 2. Generic Parameters #

Here in our network configuration, we need to pass the "GIT PROXY" configuration.

*   If you do not need, remove the `--build-arg EURECOM_PROXY=".."` option.
*   If you do need it, change with your proxy value.

If you have re-building CN4G images, be careful that `docker` or `podman` may re-use `cached` blobs
to construct the intermediate layers.

We recommend to add the `--no-cache` option in that case.

**CAUTION: the location of the dockerfiles HAVE CHANGED.**

# 3. Build HSS Image #

## 3.1 On a Ubuntu 18.04 Host ##

```bash
$ docker build --target oai-hss --tag oai-hss:production \
               --file component/oai-hss/docker/Dockerfile.ubuntu18.04 \
               # The following line about proxy is certainly not needed in your env \
               --build-arg EURECOM_PROXY="http://proxy.eurecom.fr:8080" \
               component/oai-hss
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

# 4. Build SPGW-C Image #

## 4.1 On a Ubuntu 18.04 Host ##

```bash
$ docker build --target oai-spgwc --tag oai-spgwc:production \
               --file component/oai-spgwc/docker/Dockerfile.ubuntu18.04 \
               # The following line about proxy is certainly not needed in your env \
               --build-arg EURECOM_PROXY="http://proxy.eurecom.fr:8080" \
               component/oai-spgwc
$ docker image prune --force
$ docker image ls
oai-spgwc               production             b1ba7dd16bc5        1 minute ago          218MB
...
```

## 4.2 On a CentOS 7/8 Host ##

**Even if we are on a CentOS7 host, we build the SPGW-C image using the CentOS-8 dockerfile.**

```bash
$ docker build --target oai-spgwc --tag oai-spgwc:production \
               --file component/oai-spgwc/docker/Dockerfile.centos8 component/oai-spgwc
$ docker image prune --force
$ docker image ls
oai-spgwc               production             15ad64676b1f        1 minute ago          379MB
...
```

# 5. Build SPGW-U Image #

## 5.1 On a Ubuntu 18.04 Host ##

```bash
$ docker build --target oai-spgwu-tiny --tag oai-spgwu-tiny:production \
               --file component/oai-spgwu-tiny/docker/Dockerfile.ubuntu18.04 \
               # The following line about proxy is certainly not needed in your env \
               --build-arg EURECOM_PROXY="http://proxy.eurecom.fr:8080" \
               component/oai-spgwu-tiny
$ docker image prune --force
$ docker image ls
oai-spgwu-tiny          production             588e14481f2b        1 minute ago          220MB
...
```

## 5.2 On a CentOS 7/8 Host ##

**Even if we are on a CentOS7 host, we build the SPGW-U image using the CentOS-8 dockerfile.**

```bash
$ docker build --target oai-spgwu-tiny --tag oai-spgwu-tiny:production \
               --file component/oai-spgwu-tiny/docker/Dockerfile.centos8 component/oai-spgwu-tiny
$ docker image prune --force
$ docker image ls
oai-spgwu-tiny          production             f2d0a07fba2c        1 minute ago          378MB
...
```

# 6. Build MAGMA-MME image #

It is possible to build it on a RHEL8 Base image.
