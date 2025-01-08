import asyncio
from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey
from solders.keypair import Keypair
from solders.transaction import Transaction
from solders.system_program import transfer
from data.config import PRIVATE_KEY
from utils.logger import logger

SOL_TO_LAMPORTS = 1_000_000_000

class Wallet:
    
    def __init__(self, recipient: str, private_key=PRIVATE_KEY):
        self.client = AsyncClient("https://api.testnet.solana.com")
        self.keypair = Keypair.from_bytes(private_key)
        self.recipient = recipient


    def get_balance(self):
        balance = self.client.get_balance(self.keypair.pubkey)
        return balance['result']['value'] / SOL_TO_LAMPORTS


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