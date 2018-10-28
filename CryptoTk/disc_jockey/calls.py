' Network wrapper module for web3 '

import ujson
import addr
import network

GAS_PRICE = int(1e9 * 10) # Do not hardcode.

def get_nft():
    return network.contract(address=network.to_checksum(addr.NFT_CONTRACT), abi=open('cryptotk.abi').read().strip())

def wait_for_tx(tx_hash):
    ' Wait for tx - ignore return value '
    network.WEB3.eth.waitForTransactionReceipt(tx_hash)

def vote(method, media_id, nonce_inc=0):
    ' upvote. method=voteUp or voteDown. '
    data_to_encode = get_nft().encodeABI(fn_name=method, args=[media_id])
    signed_txn = network.WEB3.eth.account.signTransaction(dict(
        nonce = network.WEB3.eth.getTransactionCount(network.to_checksum(addr.PUB)) + nonce_inc,
        gasPrice = GAS_PRICE,
        data=data_to_encode,
        gas = 100000,
        to = network.to_checksum(addr.NFT_CONTRACT),
        ), addr.PRIV)
    tx_hash = network.WEB3.eth.sendRawTransaction(signed_txn.rawTransaction)
    return tx_hash

def send_xdai(dest, amount_wei, nonce_inc=0):
    ' Send xdai away '
    signed_txn = network.WEB3.eth.account.signTransaction(dict(
        nonce = network.WEB3.eth.getTransactionCount(network.to_checksum(addr.PUB)),
        gasPrice = gasPrice,
        gas = 25000,
        to = network.to_checksum(dest),
        value = amount_wei,
        ), addr.PRIV)
    return network.WEB3.eth.sendRawTransaction(signed_txn.rawTransaction)

def test_vote():
  ' send a vote '
  wait_for_tx(vote('voteUp', 0))

def main():
  ' main '
  # test_vote() # OK

if __name__ == "__main__":
    main()
