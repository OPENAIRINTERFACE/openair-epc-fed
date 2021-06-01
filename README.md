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
    <a href="https://jenkins-oai.eurecom.fr/job/OAI-CN-HSS/"><img src="https://img.shields.io/jenkins/build?jobUrl=https%3A%2F%2Fjenkins-oai.eurecom.fr%2Fjob%2FOAI-CN-HSS%2F&label=build%20HSS"></a>
    <a href="https://jenkins-oai.eurecom.fr/job/OAI-CN-SPGWC/"><img src="https://img.shields.io/jenkins/build?jobUrl=https%3A%2F%2Fjenkins-oai.eurecom.fr%2Fjob%2FOAI-CN-SPGWC%2F&label=build%20SPGWC"></a>
    <a href="https://jenkins-oai.eurecom.fr/job/OAI-CN-SPGWU-TINY/"><img src="https://img.shields.io/jenkins/build?jobUrl=https%3A%2F%2Fjenkins-oai.eurecom.fr%2Fjob%2FOAI-CN-SPGWU-TINY%2F&label=build%20SPGWU-TINY"></a>
    <a href="https://jenkins-oai.eurecom.fr/job/MAGMA-MME-production/"><img src="https://img.shields.io/jenkins/build?jobUrl=https%3A%2F%2Fjenkins-oai.eurecom.fr%2Fjob%2FMAGMA-MME-production%2F&label=build%20MAGMA-MME"></a>
</p>

  Openair-cn is an implementation of the 3GPP specifications concerning the
  Evolved Packet Core Networks, that means it contains the implementation of the
  following network elements:

  * MME,
  * HSS,
  * S-GW+P-GW.

  Each element implementation has its own repository. This repository is a federation of components.

  Currently the purpose of this repository is mainly for CI activities and documentation.

  It is also hosting some tutorials:

  - [Simple Docker Deployment using the OAI Legacy MME](./docs/DEPLOY_HOME.md)
  - [Deploying a whole EPC with MAGMA MME image](docs/DEPLOY_HOME_MAGMA_MME.md)

# Licence info

  The source code in this repository is mainly written under the [3-Clause BSD License](https://opensource.org/licenses/BSD-3-Clause).

  The text for 3-Clause BSD License is also available under [LICENSE](LICENSE) file in the same directory.

  This repository is just an aggregation of git repositories as sub-modules. Each repository has its own LICENSE file.

  - OAI-HSS --> **3-Clause BSD License**
  - OAI-MME --> **3-Clause BSD License**
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
