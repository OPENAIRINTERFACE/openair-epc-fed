<h1 align="center">
    <a href="https://openairinterface.org/"><img src="https://openairinterface.org/wp-content/uploads/2015/06/cropped-oai_final_logo.png" alt="OAI" width="550"></a>
</h1>


------------------------------------------------------------------------------

                             OPENAIR-CN
    An implementation of the Evolved Packet Core network.

------------------------------------------------------------------------------

<p align="center">
    <a href="https://github.com/OPENAIRINTERFACE/openair-epc-fed/blob/master/LICENSE"><img src="https://img.shields.io/badge/license-BSD3clause-blue.svg" alt="License"></a>
    <a href="https://github.com/OPENAIRINTERFACE/openair-spgwc/blob/master/LICENSE"><img src="https://img.shields.io/badge/license-OAI--Public--V1.1-blue" alt="License"></a>
    <a href="https://github.com/OPENAIRINTERFACE/openair-epc-fed/releases"><img src="https://img.shields.io/github/v/release/OPENAIRINTERFACE/openair-epc-fed" alt="Release"></a>
</p>

<p align="center">
    <a href="https://jenkins-oai.eurecom.fr/job/OAI-CN-HSS/"><img src="https://img.shields.io/jenkins/build?jobUrl=https%3A%2F%2Fjenkins-oai.eurecom.fr%2Fjob%2FOAI-CN-HSS%2F&label=build%20HSS"></a>
    <a href="https://jenkins-oai.eurecom.fr/job/OAI-CN-SPGWC/"><img src="https://img.shields.io/jenkins/build?jobUrl=https%3A%2F%2Fjenkins-oai.eurecom.fr%2Fjob%2FOAI-CN-SPGWC%2F&label=build%20SPGWC"></a>
    <a href="https://jenkins-oai.eurecom.fr/job/OAI-CN-SPGWU-TINY/"><img src="https://img.shields.io/jenkins/build?jobUrl=https%3A%2F%2Fjenkins-oai.eurecom.fr%2Fjob%2FOAI-CN-SPGWU-TINY%2F&label=build%20SPGWU-TINY"></a>
    <a href="https://jenkins-oai.eurecom.fr/job/MAGMA-MME-master-check/"><img src="https://img.shields.io/jenkins/build?jobUrl=https%3A%2F%2Fjenkins-oai.eurecom.fr%2Fjob%2FMAGMA-MME-master-check%2F&label=build%20MAGMA-MME"></a>
</p>

<p align="center">
  <a href="https://hub.docker.com/r/rdefosseoai/oai-hss"><img alt="Docker Pulls" src="https://img.shields.io/docker/pulls/rdefosseoai/oai-hss?label=HSS%20docker%20pulls"></a>
  <a href="https://hub.docker.com/r/rdefosseoai/oai-spgwc"><img alt="Docker Pulls" src="https://img.shields.io/docker/pulls/rdefosseoai/oai-spgwc?label=SPGWC%20docker%20pulls"></a>
  <a href="https://hub.docker.com/r/rdefosseoai/oai-spgwu-tiny"><img alt="Docker Pulls" src="https://img.shields.io/docker/pulls/rdefosseoai/oai-spgwu-tiny?label=SPGWU-TINY%20docker%20pulls"></a>
  <a href="https://hub.docker.com/r/rdefosseoai/magma-mme"><img alt="Docker Pulls" src="https://img.shields.io/docker/pulls/rdefosseoai/magma-mme?label=MAGMA-MME%20docker%20pulls"></a>
</p>

  Openair-cn is an implementation of the 3GPP specifications concerning the
  Evolved Packet Core Networks, that means it contains the implementation of the
  following network elements:

  * MME,
  * HSS,
  * S-GW+P-GW.

  Each element implementation has its own repository. This repository is a federation of components.

  Currently the purpose of this repository is mainly for CI activities and documentation.

  **AS OF 2022/02/25, WE HAVE OBSOLETED OUR LEGACY OAI-MME. THE ONLY RECOMMENDED AND SUPPORTED MME IS MAGMA-MME.**

  It is also hosting some tutorials:

  - [Deploying a whole EPC with MAGMA MME image](docs/DEPLOY_HOME_MAGMA_MME.md)

# Licence info

  The source code in this repository is mainly written under the [3-Clause BSD License](https://opensource.org/licenses/BSD-3-Clause).

  The text for 3-Clause BSD License is also available under [LICENSE](LICENSE) file in the same directory.

  This repository is just an aggregation of git repositories as sub-modules. Each repository has its own LICENSE file.

  - OAI-HSS --> **3-Clause BSD License**
  - MAGMA-MME --> **3-Clause BSD License**
  - OAI-SPGWC --> **OAI Public License V1.1**
  - OAI-SPGWU-TINY --> **OAI Public License V1.1**

  For more details on third party software, please read the [NOTICE](NOTICE) file in the same directory.

# Collaborative work

  This source code is managed through a GITHUB, a collaborative development platform

  *  URL: [https://github.com/OPENAIRINTERFACE/openair-epc-fed](https://github.com/OPENAIRINTERFACE/openair-epc-fed).

  Process is explained in [CONTRIBUTING](CONTRIBUTING.md) file.

# Contribution requests

  In a general way, anybody who is willing can contribute on any part of the
  code in any network component.

  Contributions can be simple bugfixes, advices and remarks on the design,
  architecture, coding/implementation.

# Release Notes

  They are available on the [CHANGELOG](CHANGELOG.md) file.
