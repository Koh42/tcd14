#!/bin/sh

INIT_OUTPUT_FILE=/vol/vault_init.txt

echo "Running script $0"

function new_hash() {
  echo $(head -c4096 /dev/urandom | sha1sum | cut -b -40)
}


if [ "$VAULT_ADDR" == "" ]
then
  echo "VAULT_ADDR is not set"
  exit 1
else
  echo "VAULT_ADDR is set to $VAULT_ADDR"
fi

while vault status 2>&1 |grep Error
do
  echo "Vault is not ready"
  sleep 1
done

if vault status |grep -E 'Initialized[[:space:]]+false'
then
  echo "Vault is not initialized"
  echo "Initializing vault and storing the unseal keys in $INIT_OUTPUT_FILE"
  vault operator init -key-shares=3 -key-threshold=2 > $INIT_OUTPUT_FILE
fi

if vault status |grep -E 'Sealed[[:space:]]+true'
then
    echo "Vault is sealed"
    echo "Unsealing vault with the keys in $INIT_OUTPUT_FILE"
    awk '/Unseal Key/ {system("vault operator unseal " $4)}' $INIT_OUTPUT_FILE
fi

echo "Vault is unsealed"

export VAULT_TOKEN=`awk '/Initial Root Token:/ {print $4}' $INIT_OUTPUT_FILE`
if vault token lookup > /dev/null
then
    echo "Root token is valid"
    (vault audit list | grep file/ > /dev/null && echo audit enabled) ||
        vault audit enable file file_path=/vault/logs/audit.log
    (vault secrets list | grep kv-v2/ > /dev/null && echo secrets/ enabled) ||
        vault secrets enable kv-v2
    (vault auth list | grep approle/ > /dev/null && echo approle/ enabled) ||
        vault auth enable approle
    # vault token revoke -self
    # https://developer.hashicorp.com/vault/tutorials/operations/generate-root
else
    echo "Root token is revoked"
fi


echo new hash is $(new_hash)

#sleep infinity
