# RELEASE NOTES: #

## v1.2.0 -- February 2022 ##

* `FEDERATION LEVEL`:
  - Obsolescence of Legacy OAI-MME
* `HSS`:
  - Build fixes
  - Docker image layer optimization
* `SPGWC`:
  - Build fixes
  - Docker image layer optimization
  - Association trigger
  - Sanitize leak and UE configurable MTU
  - IE NWI dotted formatting
  - IE UPF Features
  - Custom UPF FQDN support
* `SPGWU-TINY`:
  - Build fixes
  - Docker image layer optimization

## v1.1.5 -- December 2021 ##

* `SPGWU-TINY`:
  - Disable association request if NF registration is enabled

## v1.1.4 -- October 2021 ##

* `SPGWU-TINY`:
  - Fix build issue
  - Fix GTPU DL encapsulation: 8 extraneous bytes

## v1.1.3 -- October 2021 ##

* `HSS`:
  - Fix build on external git sub-modules that are using `main` as master branch name
  - Code clean-up with no more cppcheck errors
* `SPGWU-TINY`:
  - Adding 5G features
    - HTTP2 support

## v1.1.2 -- July 2021 ##

* `FEDERATION LEVEL`:
  - DOC: cleanup, update and fixes on tutorials
* `HSS`:
  - Enable Dual-Registration- 5G-Indicator flag in S6a/ULR
  - Fix users' provision in case of multi-pdn
  - Adding correct TZ env var to dockerfiles
  - Improved Continuous Integration
* `SPGWC`:
  -  Sanitize leak fixes
  -  Adding correct TZ env var to dockerfiles
  -  Improved Continuous Integration
* `SPGWU-TINY`:
  - Adding 5G features
    - NRF discovery and FQDN support

## v1.1.1 -- February 2021 ##

* `HSS`:
  -  Cloud-native support
  -  RHEL8 support
  -  Proper build in release mode
* `SPGWC`:
  -  Cloud-native support
  -  RHEL8 support
  -  A lot of bug fixes
     -  UE MTU
     -  CSR Collision fix
     -  ...
  -  Last release before change to a JSON-based configuration file and Multi-SPGW-U-instance support
* `SPGWU-TINY`:
  - GTP-U extension headers for 5G support
    - disabled by default for 4G usage
