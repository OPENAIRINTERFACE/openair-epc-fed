<table style="border-collapse: collapse; border: none;">
  <tr style="border-collapse: collapse; border: none;">
    <td style="border-collapse: collapse; border: none;">
      <a href="http://www.openairinterface.org/">
         <img src="./images/oai_final_logo.png" alt="" border=3 height=50 width=150>
         </img>
      </a>
    </td>
    <td style="border-collapse: collapse; border: none; vertical-align: center;">
      <b><font size = "5">OpenAirInterface Core Network : MAGMA MME based Deployment</font></b>
    </td>
  </tr>
</table>

# Why you should use this deployment? #

-  You want the latest updates:
   - the `master` branch on the `magma` project is updated every day with new features, bug fixes...
-  You expect the whole EPC to be running for hours and days without any restart

**CAUTION: there is still a few issues when running the whole OAI stack**

  *  OAI LTE eNB Softmodem
  *  OAI LTE UE Softmodem

We are currently working on the RAN side to fix these issues.

**Table of Contents**

1.  [Pre-requisites](./DEPLOY_PRE_REQUESITES_MAGMA.md)
2.  [Building the Docker Images](./BUILD_IMAGES_MAGMA_MME.md)
3.  [Deploying with MAGMA-MME using docker-compose](../docker-compose/magma-mme-demo/README.md)
4.  [Verify/Correct your network environment](./CONFIGURE_NETWORKS_MAGMA.md)
5.  [Demo made during 2021 MAGMA-dev conference](./NSA_SUPPORT_OAI_RAN.md)
