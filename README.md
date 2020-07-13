# playg-aries


## Setup
Init required repositories:

1. VON netowrk with 4 nodes and Ledger browser `git clone https://github.com/bcgov/von-network.git`

2. Aries ACA-py framework `git clone https://github.com/hyperledger/aries-cloudagent-python`

3. Scripts and runners `git clone https://github.com/VladoDemcak/playg-aries.git`


## Run
0. Change directory to playground with aries. `$ cd playg-aries/`

1. Run indy network
` $ ./ledger/run_von `


2. Register Faber's DID on ledger
```
curl --location --request POST 'http://localhost:8080/register' \
--header 'Content-Type: application/json' \
--data-raw '{
   "did":"JdRkpwWwCBqjfcrsjAH1GT",
   "verkey":"AcFvnqBQUatQmU4kfc9R9XEci8HQfDRPutGFTwpdWUrZ"
}'
```

3. Run Faber's agent `$ ./py/run_faber`

4. Run Alice's agent `$ ./py/run_alice`

5. Import Postman
