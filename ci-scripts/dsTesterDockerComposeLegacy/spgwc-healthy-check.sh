#!/bin/bash

STATUS=0
NB_UNREPLACED_AT=`cat /openair-spgwc/etc/*.json | grep -v contact@openairinterface.org | grep -c @ || true`
if [ $NB_UNREPLACED_AT -ne 0 ]
then    
  STATUS=-1
fi

exit $STATUS
