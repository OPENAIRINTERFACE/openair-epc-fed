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

**Table of Contents**

1. [Retrieve the proper code version on the OAI-CN part](#1-retrieve-the-proper-code-version-on-the-oai-cn-part)
2. [Generic Parameters](#2-generic-parameters)
3. [Build OAI-HSS Image](#3-build-hss-image)
4. [Build OAI-SPGW-C Image](#4-build-spgw-c-image)
5. [Build OAI-SPGW-U Image](#5-build-spgw-u-image)
6. [Retrieve the MAGMA source code](#6-retrieve-the-magma-source-code)
   1. [Get the NSA-Support source code](#61-get-the-nsa-support-source-code)
   2. [Prepare the source code for a MAGMA-MME Docker Image build](#62-prepare-the-source-code-for-a-magma-mme-docker-image-build)
   3. [Build the MAGMA-MME Ubuntu18 Docker image](#63-build-the-magma-mme-ubuntu18-docker-image)


This page is only for `Ubuntu18` builds. For other distributions, see [here](./BUILD_IMAGES.md).

# 1.  Retrieve the proper code version on the OAI-CN part #

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
| FED REPO    | N/A         | `v1.2.0`   |              |                 |
| HSS         | `master`    | `v1.2.0`   | X            | X               |
| SPWG-C      | `master`    | `v1.2.0`   | X            | X               |
| SPGW-U-TINY | `master`    | `v1.2.0`   | X            | X               |
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
$ ./scripts/syncComponentsLegacy.sh --hss-branch develop --spgwc-branch develop --spgwu-tiny-branch develop
---------------------------------------------------------
OAI-HSS    component branch : develop
OAI-SPGW-C component branch : develop
OAI-SPGW-U component branch : develop
---------------------------------------------------------
git submodule deinit --all --force
git submodule init
git submodule update
```

# 2. Generic Parameters #

Here in our network configuration, we need to pass the "GIT PROXY" configuration.

*   If you do not need, remove the `--build-arg EURECOM_PROXY=".."` option.
*   If you do need it, change with your proxy value.

# 3. Build HSS Image #

## 3.1 On a Ubuntu 18.04 Host ##

On our CI server (a 48-CPU server), this operation takes around **13 minutes**. Please be patient.

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

# 4. Build SPGW-C Image #

## 4.1 On a Ubuntu 18.04 Host ##

On our CI server (a 48-CPU server), this operation takes around **10 minutes**. Please be patient.

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

# 5. Build SPGW-U Image #

## 5.1 On a Ubuntu 18.04 Host ##

On our CI server (a 48-CPU server), this operation takes around **9 minutes**. Please be patient.

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

# 6. Retrieve the MAGMA source code #

## 6.1. Get the NSA-Support source code ##

**Important Update (2021 / 03 / 20), the NSA Support was merged into `master`.**

```bash
$ cd ~
$ git clone https://github.com/magma/magma.git
$ cd magma
$ git log | grep -i NSA
```

You should see Mohit's Pull request being merged (`[Converged MME]NSA-Addition (#4513)`).

## 6.2. Prepare the source code for a MAGMA-MME Docker Image build ##

The `.dockerignore` file is meant for the image building on the Orchestrator.

**It is NOT suitable for the MAGMA-MME image building. If you don't remove/rename, build won't complete.**

```bash
$ rm .dockerignore
```

During the UE attachment, we have seen that when UE receives the `EMM-Information` NAS packet, the UE disconnects.

**So at the time of writing (2021 / 02 / 01), we are disabling the sending of EMM-INFO packet.**

```bash
$ git diff lte/gateway/c/core/oai/tasks/nas/emm/Attach.c
diff --git a/lte/gateway/c/core/oai/tasks/nas/emm/Attach.c b/lte/gateway/c/core/oai/tasks/nas/emm/Attach.c
index 34f353a88..b354b18b7 100644
--- a/lte/gateway/c/core/oai/tasks/nas/emm/Attach.c
+++ b/lte/gateway/c/core/oai/tasks/nas/emm/Attach.c
@@ -840,7 +840,7 @@ int emm_proc_attach_complete(
           LOG_NAS_EMM,
           " Sending EMM INFORMATION for ue_id = " MME_UE_S1AP_ID_FMT "\n",
           ue_id);
-      emm_proc_emm_informtion(ue_mm_context);
+      //emm_proc_emm_informtion(ue_mm_context);
       increment_counter("ue_attach", 1, 1, "result", "attach_proc_successful");
       attach_success_event(ue_mm_context->emm_context._imsi64);
     }
```

This issue is in our **TODO** list and we are still investigating.

Another known issue is if the UE send a `TAU request` to the MME. Currently the MAGMA MME with an OAI eNB
does not handle it well. We are also working on providing a fix for this issue.

**Update (2021/11/22): Implementation of `TAU request` response in the MME has been merged in September in MAGMA `master` branch.**
We validated it on our RAN CI bench.

## 6.3. Build the MAGMA-MME Ubuntu18 Docker image ##

On our CI server (a 48-CPU server), this operation takes around **30-35 minutes**. Please be patient.

The reason: a lot of needed packages/libraries are installed from source for a very specific version.

Once again, if you need a proxy, add your proxy URL. If not, remove the option.

```bash
$ docker build --target magma-mme --tag magma-mme:master \
               --file lte/gateway/docker/mme/Dockerfile.ubuntu18.04 \
               # The following line about proxy is certainly not needed in your env \
               --build-arg GIT_PROXY="http://proxy.eurecom.fr:8080" \
               .
$ docker image ls
magma-mme               nsa-support            b6fb01eb0d07        1 minute ago          492MB
...
```

If you are planning to re-build MAGMA-MME Docker image, here is is a trick:

Normally after the 35 minutes, you should get the MME image but also a dangling image that should
be quite large (5+ GBytes).

```bash
$ docker image ls
magma-mme               nsa-support            b6fb01eb0d07        1 minute ago          492MB
<none>                  <none>                 91259fd827ee        5 minutes ago         5.24GB
...
```

Re-tag the dangling image:

```bash
$ docker image tag 91259fd827ee magma-dev-mme:ci-base-image
```

And use the CI docker file.

```bash
$ docker build --target magma-mme --tag magma-mme:next-image-tag --file ci-scripts/docker/Dockerfile.mme.ci.ubuntu18 .
```

This will only take **5 to 10 minutes** to re-build a MAGMA-MME image.

Normally you are ready to deploy and test.

See [Deploy with MAGMA-MME](../docker-compose/magma-mme-demo/README.md).
