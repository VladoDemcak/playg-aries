# playg-aries


## Setup
Init required repositories:

### VON netowrk with 4 nodes and Ledger browser
```
git clone https://github.com/bcgov/von-network.git
```

### Aries ACA-py framework
```
git clone https://github.com/hyperledger/aries-cloudagent-python
```

### Scripts and runners
```
git clone https://github.com/VladoDemcak/playg-aries.git
```


## Run
Change directory to playground with aries.
```
$ cd playg-aries/
```

Run indy network
```
$ ./ledger/run_von 
Creating von_node4_1     ... done
Creating von_webserver_1 ... done
Creating von_node1_1     ... done
Creating von_node3_1     ... done
Creating von_node2_1     ... done
Want to see the scrolling container logs? Run "./manage logs"
```

Open von_webserver_1 on http://localhost:8080/

Run Alice's agent
```
$ ./agents/run_alice 
```

Expected result
```
Sending build context to Docker daemon  17.37MB
Step 1/11 : FROM bcgovimages/von-image:py36-1.15-0
...
...
Successfully tagged aries-cloudagent-run:latest

::::::::::::::::::::::::::::::::::::::::::::::
:: Aries Cloud Agent                        ::
::                                          ::
::                                          ::
:: Inbound Transports:                      ::
::                                          ::
::   - http://0.0.0.0:8001                  ::
::                                          ::
:: Outbound Transports:                     ::
::                                          ::
::   - http                                 ::
::   - https                                ::
::                                          ::
:: Public DID Information:                  ::
::                                          ::
::   - DID: JdRkpwWwCBqjfcrsjAH1GT          ::
::                                          ::
:: Administration API:                      ::
::                                          ::
::   - http://0.0.0.0:8081                  ::
::                                          ::
::                               ver: 0.5.2 ::
::::::::::::::::::::::::::::::::::::::::::::::

Listening...
```
Open Alice's OpenAPI on http://localhost:8081/api/doc


Run Bob's agent:

```
$ ./agents/run_bob
```

Expected result
```
Sending build context to Docker daemon  17.37MB
Step 1/11 : FROM bcgovimages/von-image:py36-1.15-0
...
...
Successfully tagged aries-cloudagent-run:latest

::::::::::::::::::::::::::::::::::::::::::::::
:: Aries Cloud Agent                        ::
::                                          ::
::                                          ::
:: Inbound Transports:                      ::
::                                          ::
::   - http://0.0.0.0:8002                  ::
::                                          ::
:: Outbound Transports:                     ::
::                                          ::
::   - http                                 ::
::   - https                                ::
::                                          ::
:: Public DID Information:                  ::
::                                          ::
::   - DID: 68qfyRnCfcQnw2NP5rLSWi          ::
::                                          ::
:: Administration API:                      ::
::                                          ::
::   - http://0.0.0.0:8082                  ::
::                                          ::
::                               ver: 0.5.2 ::
::::::::::::::::::::::::::::::::::::::::::::::

Listening...
```
Open Alice's OpenAPI on http://localhost:8082/api/doc
