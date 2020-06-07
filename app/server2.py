from flask import Flask, jsonify, request, redirect
from blockchain import Block, Blockchain, Mempool, Data
import json
import requests

app = Flask(__name__)

blockchain = Blockchain()

peers = set()

@app.route("/")
def home():
	return "Here we are"

@app.route('/chain')
def chain():
	global blockchain
	chain_data = []
	for block in blockchain.chain:
		chain_data.append(block.__dict__)
	return json.dumps({"length": len(chain_data),
					   "chain": chain_data,
					   "peers": list(peers)})

@app.route('/add_to_chain', methods = ["POST"])
def add_to_chain():
	if request.method == "POST":
		title = request.form.get('title')
		content = request.form.get('content')
		if title and content:
			data = Data(title = title, content = content)
			Mem = Mempool(data.__dict__)
			Mem.add()
			unconfirmed_data = Mem.unconfirmed_data
			block = Block(data = unconfirmed_data)
			global blockchain
			blockchain.add_block(block)
			return redirect("/")
		else:
			return("No data found")
	else:
		return("No request made")


@app.route("/is_chain_valid")
def is_chain_valid():
	global blockchain
	if not blockchain.is_chain_valid:
		return "The chain is invalid"
	return "The chain is valid and very healthy"

@app.route("/verify_and_add_block", methods = ["POST"])
def verify_and_add_block():
	block_data = request.get_json()
	block = Block(block_data["index"],
                  block_data["data"],
                  block_data["id"],
                  block_data["prev_hash"],
                  block_data["nonce"])
	added = blockchain.add_block(block)

	if not added:
		return "The block was discarded by the node", 400
	return "Block added to the chain", 201

@app.route("/register_new_peers", methods = ["POST"])
def register_new_peers():
	global blockchain
	new_node = request.form.get("node")
	if new_node:
		peers.add(new_node)
		return chain()
	return "Invalid address", 400

@app.route("/register_with_existing_node", methods = ["POST"])
def register_with_existing_node():
	node_address = request.form.get('node')
	if not node_address:
		return "Invalid node", 400
	data = {"node": request.host_url}
	headers = {"Content-Type": "application/json"}

	response = requests.post(node_address + "/register_new_peers", data = json.dumps(data), headers = headers)
	if response.status_code == 200:
		global blockchain
		global peers
		chain_dump = response.json()["chain"]
		#blockchain = create_chain_from_dump(chain_dump)
		peers.update(response.json()['peers'])
		return "Registration successful", 200
	else:
		return response.content, response.status_code

def announce_mined_block(block):
	if not block.proof_of_work():
		return "Invalid block"
	for peer in peers:
		url = f"{peer}/verify_and_add_block"
		response = requests.post(url, data = block)

def consensus():
	global blockchain

	length1 = len(blockchain.chain)
	longest_chain = None

	for peer in peers:
		url = f"{peer}/verify_and_add_block"
		response = requests.get(url)
		length = response.json()["length"]
		chain = response.json()["chain"]
		if length > length1 and blockchain.is_chain_valid:
			longest_chain = chain
			length1 = length1
	if longest_chain:
		blockchain = longest_chain
		return True
	return False

def create_chain_from_dump(chain_dump):
    generated_blockchain = Blockchain()
    generated_blockchain.create_genesis_block()
    for idx, block_data in enumerate(chain_dump):
        if idx == 0:
            continue  # skip genesis block
        block = Block(block_data["index"],
                      block_data["data"],
                      block_data["id"],
                      block_data["prev_hash"],
                      block_data["nonce"])
        added = generated_blockchain.add_block(block)
        if not added:
            raise Exception("The chain dump is tampered!!")
    return generated_blockchain


if __name__ == '__main__':
	app.run(debug = True, port = 9000)