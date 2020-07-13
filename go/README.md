docker login for sidetree.mock
```
docker login https://docker.pkg.github.com -u VladoDemcak
```

Get github token as described [here](https://github.com/hyperledger/aries-framework-go/blob/master/docs/test/build.md) "Configure Docker to use GitHub Packages - Authenticate using GitHub token".

*For Token select scopes*:
+ repo
+ read:packages

Run demo
```
cd aries-framework-go
make run-openapi-demo
```


Import `aries-flow-go.postman_collection.json` postman.