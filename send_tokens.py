#!/usr/bin/python3

from algosdk.v2client import algod
from algosdk import mnemonic
from algosdk import account, encoding
from algosdk import transaction

#Connect to Algorand node maintained by PureStake
algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = "B3SU4KcVKi94Jap2VXkK83xx38bsv95K5UZm2lab"
#algod_token = 'IwMysN3FSZ8zGVaQnoUIJ9RXolbQ5nRY62JRqF2H'
headers = {
   "X-API-Key": algod_token,
}

acl = algod.AlgodClient(algod_token, algod_address, headers)
min_balance = 100000 #https://developer.algorand.org/docs/features/accounts/#minimum-balance

# ACCOUNT CREATION

# generate an account
#sk, pk = account.generate_account()
#print("Private key:", sk)
#print("Address:", pk)

mnemonic_secret = "pretty frequent slogan collect lyrics culture nest focus crystal remain ketchup voice garage village build wear noble luxury lens acoustic host december focus above primary"
sk = mnemonic.to_private_key(mnemonic_secret)
pk = mnemonic.to_public_key(mnemonic_secret)

print("Private key:", sk)
print("Address:", pk)

#Check balance
#account_info = acl.account_info(pk)
#print("Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")


def send_tokens( receiver_pk, tx_amount ):
    params = acl.suggested_params()
    gen_hash = params.gh
    first_valid_round = params.first
    tx_fee = params.min_fee
    last_valid_round = params.last

    #Your code here

    unsigned_tx = transaction.PaymentTxn(pk, tx_fee, first_valid_round, last_valid_round, gen_hash, receiver_pk, tx_amount, flat_fee=True)
    signed_tx = unsigned_tx.sign(sk)

    txid = acl.send_transaction(signed_tx)
    print("Succesful sent trx with ID: {}".format(txid))

    wait_for_confirmation(acl, txid)

    sender_pk = pk


    return sender_pk, txid

# Function from Algorand Inc.
def wait_for_confirmation(client, txid):
    """
    Utility function to wait until the transaction is
    confirmed before proceeding.
    """
    last_round = client.status().get('last-round')
    txinfo = client.pending_transaction_info(txid)
    while not (txinfo.get('confirmed-round') and txinfo.get('confirmed-round') > 0):
        print("Waiting for confirmation")
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(txid)
    print("Transaction {} confirmed in round {}.".format(txid, txinfo.get('confirmed-round')))
    return txinfo

