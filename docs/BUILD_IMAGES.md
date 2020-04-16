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

At the time of writing (2020 / 04 / 20), if you want to use the OpenAir-CN for a Dual Connectivity use case, you need to use proper branches:

**cNF Name** | **Branch Name** | **Commit at time of writing**
------------ | --------------- | ------------------------------
HSS          | `develop`       | `bca864904870d3430c0cc26b6120c88182b4919a`
MME          | `samsumg-s10-5g-g977u-merged` | `3af7e7525e1bb5a8aeb0ed3cdacc51c79afada7a`
SPGW-C       | `develop`       | `a27aa529fb7e49a02e5d71ead803f03edb16688c`
SPGW-U-TINY  | `develop`       | `1891234b4694a9670e6c9eebb2eabe62cf06c7c9`

If the `samsumg-s10-5g-g977u-merged` branch does not exist when you try, it certainly means it has been merged into `develop` branch of MME repository.

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

# 2. Generic Parameters #

Here in our network configuration, we need to pass the "GIT PROXY" configuration.

*   If you do not need, remove the "--build-arg EURECOM_PROXY=" option.
*   If you do need it, change with your proxy value.

# 3. Build HSS Image #

```bash
$ docker build --target oai-hss --tag oai-hss:production --file component/oai-hss/ci-scripts/Dockerfile.ubuntu18.04 --build-arg EURECOM_PROXY="http://proxy.eurecom.fr:8080" .
$ docker image prune --force
$ docker image ls
oai-hss                 production             f478bafd7a06        1 minute ago          341MB
...
```

# 4. Build MME Image #

Once again, at time of writing, we are using `samsumg-s10-5g-g977u-merged` branch.

```bash
$ docker build --target oai-mme --tag oai-mme:production --file component/oai-mme/ci-scripts/Dockerfile.ubuntu18.04 --build-arg EURECOM_PROXY="http://proxy.eurecom.fr:8080" --build-arg CI_SRC_BRANCH="samsumg-s10-5g-g977u-merged" .
$ docker image prune --force
$ docker image ls
oai-mme                 prodution              45254be9f987        1 minute ago          245MB
...
```

If this branch does not exist, just use the `develop` branch.

```bash
$ docker build --target oai-mme --tag oai-mme:production --file component/oai-mme/ci-scripts/Dockerfile.ubuntu18.04 --build-arg EURECOM_PROXY="http://proxy.eurecom.fr:8080" .
```

# 5. Build SPGW-C Image #

```bash
$ docker build --target oai-spgwc --tag oai-spgwc:production --file component/oai-spgwc/ci-scripts/Dockerfile.ubuntu18.04 --build-arg EURECOM_PROXY="http://proxy.eurecom.fr:8080" .
$ docker image prune --force
$ docker image ls
oai-spgwc               production             b1ba7dd16bc5        1 minute ago          218MB
...
```

# 6, Build SPGW-U Image #

```bash
$ docker build --target oai-spgwu-tiny --tag oai-spgwu-tiny:production --file component/oai-spgwu-tiny/ci-scripts/Dockerfile.ubuntu18.04 --build-arg EURECOM_PROXY="http://proxy.eurecom.fr:8080" .
$ docker image prune --force
$ docker image ls
oai-spgwu-tiny          production             588e14481f2b        1 minute ago          220MB
...
```
