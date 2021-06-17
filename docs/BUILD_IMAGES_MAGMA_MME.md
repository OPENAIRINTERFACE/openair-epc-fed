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

# 1.  Retrieve the proper code version on the OAI-CN part #

At the time of writing (2021 / 02 / 08), if you want to use the OpenAir-CN for a Dual Connectivity use case, you need to use proper branches:

**cNF Name** | **Branch Name** | **Tags**   | **Commit at time of writing**              | Ubuntu18 |
------------ | --------------- | ---------- | ------------------------------------------ | -------- |
HSS          | `develop`       | `2021.w10` | `93dfcbca245ec97652c4d62ba3913a899d956d68` | X        |
SPGW-C       | `develop`       | `2021.w10` | `b10256535e47ffb86c86a8581d9c50b1f380dcf5` | X        |
SPGW-U-TINY  | `develop`       | `2021.w10` | `acd293e616f879f4dacead152c59384d1e533167` | X        |

```bash
$ git clone https://github.com/OPENAIRINTERFACE/openair-epc-fed.git
$ cd openair-epc-fed

# You can specify a tag on the parent GIT repository such as `2021.w22`
$ git checkout 2021.w22
# Or you can sync to the latest version
$ git checkout master

# Then you need to resync the sub-modules (ie HSS, SPGW-CUPS).
# You can specify:
#   ---  a valid tag (such as seen)
#   ---  a newer tag
#   ---  a branch to get the latest (`develop` being the latest stable)
#        Usually the better option is to specify `develop`

$ ./scripts/syncComponents.sh --hss-branch 2021.w10 --spgwc-branch 2021.w10 --spgwu-tiny-branch 2021.w10
---------------------------------------------------------
OAI-HSS    component branch : 2021.w10
OAI-SPGW-C component branch : 2021.w10
OAI-SPGW-U component branch : 2021.w10
---------------------------------------------------------
....

# Or to not specify anything
$ ./scripts/syncComponentsLegacy.sh
---------------------------------------------------------
OAI-HSS    component branch : develop
OAI-SPGW-C component branch : develop
OAI-SPGW-U component branch : develop
---------------------------------------------------------
....
```

In general, the `docker-compose` files (even in the tutorials) are up-to-date w/ `develop` latest commits in each sub-module.

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
               --build-arg EURECOM_PROXY="http://proxy.eurecom.fr:8080" component/oai-hss
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
               --build-arg EURECOM_PROXY="http://proxy.eurecom.fr:8080" component/oai-spgwc
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
               --build-arg EURECOM_PROXY="http://proxy.eurecom.fr:8080" component/oai-spgwu-tiny
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

## 6.3. Build the MAGMA-MME Ubuntu18 Docker image ##

On our CI server (a 48-CPU server), this operation takes around **30-35 minutes**. Please be patient.

The reason: a lot of needed packages/libraries are installed from source for a very specific version.

Once again, if you need a proxy, add your proxy URL. If not, remove the option.

```bash
$ docker build --target magma-mme --tag magma-mme:master \
               --file lte/gateway/docker/mme/Dockerfile.ubuntu18.04 \
               --build-arg GIT_PROXY="http://proxy.eurecom.fr:8080" .
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

This will only take **5 minutes** to re-build a MAGMA-MME image.

Normally you are ready to deploy and test.

See [Deploy with MAGMA-MME](../docker-compose/magma-mme-demo/README.md).
