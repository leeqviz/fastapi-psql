```shell
# gen private key for jwt
openssl genrsa -out private.pem 2048
```

```shell
# gen public key for jwt
openssl rsa -in private.pem -outform PEM -pubout -out public.pem
```
