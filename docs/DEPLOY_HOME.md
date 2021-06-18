<table style="border-collapse: collapse; border: none;">
  <tr style="border-collapse: collapse; border: none;">
    <td style="border-collapse: collapse; border: none;">
      <a href="http://www.openairinterface.org/">
         <img src="./images/oai_final_logo.png" alt="" border=3 height=50 width=150>
         </img>
      </a>
    </td>
    <td style="border-collapse: collapse; border: none; vertical-align: center;">
      <b><font size = "5">OpenAirInterface Core Network Docker Deployment Home Page</font></b>
    </td>
  </tr>
</table>

In these pages, we are describing how to build and deploy an LTE EPC using the **OAI Legacy MME**.

# Why you should use this deployment? #

-  It builds faster than the `MAGMA-MME` image.
-  At the time of writing (2021-05-04), you need to connect the `OAI LTE-UE softmodem`.
   -  Currently `OAI LTE-UE softmodem` does **NOT** connect with `MAGMA-MME`.
-  You will deploy, connect your eNB(s), your COTS-UE(s),
   - Then do your experiments and then stop everything.

# Why you should NOT be using this deployment? #

-  You expect the whole EPC to be running for hours and days without any restart
   - This MME is very leaky and not robust.
   - After a few hours, you won't be able to attach a UE.
-  You want the latest updates:
   - We are **NO MORE** performing maintenance on the legacy **OAI MME**.
   - The last valid tag on the MME is **2020.w47**.
   - Our developers are now contributing to the **MAGMA-MME**.


**Table of Contents**

1.  [Pre-requisites](./DEPLOY_PRE_REQUESITES.md)
2.  [Building the Docker Images](./BUILD_IMAGES.md)
3.  [Deploying using docker-compose](../docker-compose/oai-mme-legacy/README.md)
4.  [Verify/Correct your network environment](./CONFIGURE_NETWORKS.md)
5.  [Generating Traffic to a connected UE](./GENERATE_TRAFFIC.md)
