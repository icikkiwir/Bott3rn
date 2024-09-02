from web3 import Web3
from eth_account import Account
import time
import sys
import os

# Fungsi untuk menampilkan teks di tengah layar
def center_text(text):
    terminal_width = os.get_terminal_size().columns
    lines = text.splitlines()
    centered_lines = [line.center(terminal_width) for line in lines]
    return "\n".join(centered_lines)

# ASCII 
ascii_art = """
 __     ___ _    _ _            _     _ 
 \ \   / (_) | _(_) |_ ___  ___| |__ (_)
  \ \ / /| | |/ / | __/ _ \/ __| '_ \| |
   \ V / | |   <| | || (_) \__ \ | | | |
    \_/  |_|_|\_\_|\__\___/|___/_| |_|_|
                                         
"""

# Deskripsi teks
description = """
Bot Auto Bridge Arbitrum Sepolia ke Base Sepolia https://bridge.t1rn.io/
Airdrop Atambua
"""

# Output
print("\033[92m" + center_text(ascii_art) + "\033[0m")
print(center_text(description))

# Tambahkan jarak dua paragraf setelah deskripsi teks
print("\n\n")

# Detail jaringan
private_key = '6f65eda2976e75239485fec11ab6381d0c22187b89735b054239007169acf4f7' # GANTI DENGAN PRIVATE KEY ANDA
rpc_url = 'https://arb-sepolia.g.alchemy.com/v2/YhkuU2iX0rA1pk2F880RLF3ZiIpxmf6M' # JANGAN DIGANTI
chain_id = 421614 # JANGAN DIGANTI
contract_address = '0x8D86c3573928CE125f9b2df59918c383aa2B514D' # JANGAN DIGANTI
my_address = '0xcAB1D8411c3A60D6BF1d1C625b6763e8018A163A' # GANTI DENGAN ADDRESS EVM ANDA

# Koneksi ke jaringan
web3 = Web3(Web3.HTTPProvider(rpc_url))
if not web3.is_connected():
    raise Exception("Tidak dapat terhubung ke jaringan")

# Buat akun dari private key
account = Account.from_key(private_key)

# Data transaksi untuk bridge
data = '0x56591d59627373700000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004CBB1421DF1CF362DC618d887056802d8adB7BC000000000000000000000000000000000000000000000000000005ae1a09d680e0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000005af3107a4000'

# Fungsi untuk membuat dan mengirim transaksi
def send_bridge_transaction():
    # Ambil nonce untuk alamat pengirim
    nonce = web3.eth.get_transaction_count(my_address)

    # Estimasi gas
    try:
        gas_estimate = web3.eth.estimate_gas({
            'to': contract_address,
            'from': my_address,
            'data': data,
            'value': web3.to_wei(0.0001, 'ether')  # Mengirim 0.0001 ETH
        })
        gas_limit = gas_estimate + 10000  # Tambahkan buffer gas
    except Exception as e:
        print(f"Error estimating gas: {e}")
        return None

    # Buat transaksi
    transaction = {
        'nonce': nonce,
        'to': contract_address,
        'value': web3.to_wei(0.0001, 'ether'),  # Mengirim 0.0001 ETH
        'gas': gas_limit,  # Gunakan gas limit yang diestimasi
        'gasPrice': web3.eth.gas_price,
        'chainId': chain_id,
        'data': data
    }

    # Tanda tangani transaksi dengan private key
    try:
        signed_txn = web3.eth.account.sign_transaction(transaction, private_key)
    except Exception as e:
        print(f"Error signing transaction: {e}")
        return None

    # Kirim transaksi
    try:
        tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        return web3.to_hex(tx_hash)
    except Exception as e:
        print(f"Error sending transaction: {e}")
        return None

# Jalankan script sampai dihentikan secara manual
successful_txs = 0

try:
    while True:
        tx_hash = send_bridge_transaction()
        if tx_hash:
            successful_txs += 1
            print(f"Tx Hash: {tx_hash} | Total Tx Sukses: {successful_txs}")
        time.sleep(20)  # Delay 20 detik setiap transaksi
except KeyboardInterrupt:
    print("\nScript dihentikan oleh pengguna.")
    print(f"Total transaksi sukses: {successful_txs}")
    sys.exit(0)
