from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey
from solders.keypair import Keypair
from solders.transaction import Transaction
from solders.system_program import transfer
from utils.logger import logger
from base58 import b58decode
from data.config import PRIVATE_KEY

SOL_TO_LAMPORTS = 1_000_000_000

class Wallet:
    
    def __init__(self, recipient: str, private_key=b58decode(PRIVATE_KEY)):
        self.client = AsyncClient("https://api.mainnet-beta.solana.com")
        self.keypair = Keypair.from_bytes(private_key)
        self.recipient = recipient
    

    async def get_balance(self):
        balance = await self.client.get_balance(self.keypair.pubkey())
        return balance.value / SOL_TO_LAMPORTS


    async def send(self, recipient: str, amount: float):
        try:
            amount *= SOL_TO_LAMPORTS
            transaction = Transaction().add(
                transfer(
                    from_pubkey=self.keypair.pubkey,
                    to_pubkey=Pubkey.from_string(recipient),
                    lamports=amount
                )
            )

            response = await self.client.send_transaction(transaction, self.keypair)
            logger.success(f'Successfully sent {amount} SOL to {recipient}: {response}')
        except Exception as e:
            logger.error(f'Error sending to {recipient}: {e}')

    
    async def close(self):
        await self.client.close()