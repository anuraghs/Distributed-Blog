import helpers
from helpers import PAYLOAD_DELIMITER

import csv
import os
from hashlib import sha256

#TODO change this function to print the proper blockchain

def print_blockchain(blockchain):
    result = ""
    index = 0
    if len(blockchain) == 0:
        return "Blog Empty"
    while index < len(blockchain):
        b = blockchain[index]
        result += f"[{index}] {b.operation.op} {b.operation.username} {b.operation.title} {b.operation.content} {b.hash} {b.nonce}\n"
        index += 1
    return result

def print_username(blockchain, client):
    msg = ""
    index = 0
    while index < len(blockchain):
        b = blockchain[index]
        if b.operation.username == client:
            msg = msg + b.operation.title + ' ' + b.operation.content + '\n'
        index += 1
    if msg == "":
        return "No Post"
    return msg

def print_title(blockchain, title):
    index = 0
    msg = ""
    msg += "["
    while index < len(blockchain):
        b = blockchain[index]
        if b.operation.title == title:
            msg += "(" + b.operation.username + ": " + b.operation.content + ")\n"
            
        index += 1

    msg += "]"

    if msg == "[]":
        return "Post Not Found"

    return msg

# ex. payload put - key - value - hash - nonce TODO check this function later
def parse_block_from_payload(payload):
    payload_tokens = payload.split(PAYLOAD_DELIMITER)
    op = Operation(op=payload_tokens[0], usr=payload_tokens[1], title=payload_tokens[2], content=payload_tokens[3])
    block = Block(op=op, prev_hash=payload_tokens[4], nonce=payload_tokens[5])
    return block

def doesNotExist(blockchain, title):
    i = 0
    while i < len(blockchain):
        b = blockchain[i]
        if b.operation.title == title:
            return False
        
        i += 1
        
    return True

def get_file_name(pid):
    return f"blockchain_p{pid}.csv"

def persist(pid, blockchain, callback = None):
    file_name = get_file_name(pid)
    with open(file_name, 'w', newline='') as csvfile:
        fieldnames = ['operations', 'prev_hash', 'nonce']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # writer.writeheader()
        for block in blockchain:
            writer.writerow(block.to_csv())
    
    if callback:
        callback()

def reconstruct(pid):
    file_name = get_file_name(pid)
    blockchain = []
    with open(file_name, newline='') as csvfile:
        blocks = csv.reader(csvfile, delimiter=',', quotechar='|')
        firstBlock = True
        for block in blocks:
            operationTokens = block[0].split(PAYLOAD_DELIMITER)
            operation = Operation(op=operationTokens[0], usr=operationTokens[1], title=operationTokens[2], content=operationTokens[3])
            blockchain.append(Block(op=operation, prev_hash=block[1], nonce=block[2]))
    return blockchain

def is_valid_nonce(char):
    if(char == "1" or char == "0"):
        return True
    else:
        return False

def hash_block(block):
    return sha256((block.hash + block.operation.op + str(block.nonce)).encode(encoding='utf-8')).hexdigest()

# str(Block) => <put,someKey,someValue> someReallyLongHash1283812312 35
class Block:
    #TODO maybe need to change the prev_hash to set the correct hash
    def __init__(self, op, prev_block = None, prev_hash = None, nonce = None):
        self.operation = op
        if prev_hash != None and prev_hash != "None":
            self.hash = prev_hash
        elif prev_block != None and prev_block != "None":
            self.hash = hash_block(prev_block)
        else:
            self.hash = "0000000000000000000000000000000000000000000000000000000000000000"
        self.nonce = nonce


    def mine(self):
        randomNonce = 0
        currHash = sha256((self.hash + self.operation.op + str(randomNonce)).encode(encoding='utf-8')).hexdigest()
        while (not is_valid_nonce(currHash[0])):
            randomNonce += 1
            currHash = sha256((self.hash + self.operation.op + str(randomNonce)).encode(encoding='utf-8')).hexdigest()
        self.nonce = randomNonce
        # print(f'Done mining, took {randomNonce} attempts.')

    def to_csv(self):
        return {'operations': str(self.operation), 'prev_hash': str(self.hash), 'nonce': str(self.nonce)}

    def __str__(self):
        return str(self.operation) + helpers.PAYLOAD_DELIMITER + str(self.hash) + helpers.PAYLOAD_DELIMITER + str(self.nonce)

# str(Operation) => <put,someKey,someValue>
class Operation:
    def __init__(self, op, usr, title, content):
        self.op = op
        self.username = usr
        self.title = title
        self.content = content

    def to_payload(self):
        return f"{self.op}{PAYLOAD_DELIMITER}{self.username}{PAYLOAD_DELIMITER}{self.title}{PAYLOAD_DELIMITER}{self.content}"

    def __eq__(self, other):
        if other == None:
            return False
        elif self.username == "get" and other.username == "get":
            return self.title == other.title
        
        return self.username == other.username and self.title == other.title and self.content == other.content
        
    def __str__(self):
     return str(self.op) + helpers.PAYLOAD_DELIMITER + str(self.username) + helpers.PAYLOAD_DELIMITER + str(self.title) + helpers.PAYLOAD_DELIMITER + str(self.content)
