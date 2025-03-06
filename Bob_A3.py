import hashlib
import json
import threading
import os
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-b4e960bb-d4ed-4e2b-a6a4-3383bfb9e5f8'
pnconfig.publish_key = 'pub-c-d244b6a1-a46b-46e8-bd45-3d49034dc872'
pnconfig.uuid = 'Bob'
pubnub = PubNub(pnconfig)

class MySubscribeCallback(SubscribeCallback):
    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pass
        elif status.category == PNStatusCategory.PNConnectedCategory:
            pass
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            pass
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass

    def message(self, pubnub, message):
        if 'from' in message.message and message.message['from'] == 'Alice':
            verify_block(message.message)

def my_publish_callback(envelope, status):
    if not status.is_error():
        pass
    else:
        pass

def mine_block(block_number):
    global nonce, transactions
    pre_block_hash = hashlib.sha256(json.dumps(block_number - 1).encode()).hexdigest()
    while True:
        block = {
            'Block number': block_number,
            'Hash': '',
            'Transaction': transactions[block_number - 1],
            'Nonce': nonce
        }
        block_string = json.dumps(block, sort_keys=True, indent=4, separators=(',', ':'))
        block_hash = hashlib.sha256(block_string.encode()).hexdigest()
        if int(block_hash, 16) < 2 ** 236:
            block['Hash'] = block_hash
            print("Block mined by Bob:", block)
            os.makedirs("BobBlocks", exist_ok=True)
            with open(f"BobBlocks/block_{block_number}.json", 'w') as f:
                json.dump(block, f)
            pubnub.publish().channel('channel-alice').message(block).pn_async(my_publish_callback)
            verify_block(block)  # Verify the block
            break
        nonce += 1

def verify_block(block):
    pass  # Verification can be implemented here if needed

def main():
    global nonce, transactions
    transactions = [
        "[3, 4, 5, 6]", "[4, 5, 6, 7]", "[5, 6, 7, 8]", "[6, 7, 8, 9]", "[7, 8, 9, 10]",
        "[8, 9, 10, 11]", "[9, 10, 11, 12]", "[10, 11, 12, 13]", "[11, 12, 13, 14]", "[12, 13, 14, 15]",
        "[13, 14, 15, 16]"
    ]
    nonce = 1000000000
    pubnub.add_listener(MySubscribeCallback())
    pubnub.subscribe().channels('channel-bob').execute()
    print("Bob is mining...")
    for i in range(1, len(transactions)):
        if i % 2 == 0:  # Bob generates blocks for even block numbers
            bob_thread = threading.Thread(target=mine_block, args=(i,))
            bob_thread.start()

if __name__ == "__main__":
    main()

