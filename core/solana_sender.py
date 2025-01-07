import asyncio
from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey
from solders.keypair import Keypair
from solders.transaction import Transaction
from solders.instruction import Instruction
from solders.system_program import transfer
from data import config


class Wallet:
    PRIVATE_KEY = config.PRIVATE_KEY

    def __init__(self, recipient: str, private_key=PRIVATE_KEY):
        self.client = AsyncClient("https://api.mainnet-beta.solana.com")
        self.keypair = Keypair.from_bytes(private_key)
        self.recipient = recipient


    async def send(self, recipient: str, amount: int):
        try:
            transaction = Transaction().add(
                transfer(
                    from_pubkey=self.keypair.pubkey,
                    to_pubkey=Pubkey.from_string(recipient),
                    lamports=amount
                )
            )

            response = await self.client.send_transaction(transaction, self.keypair)
            print(f'Sent {amount} lamports to {recipient}: {response}')
        except Exception as e:
            print(f'Error sending to {recipient}: {e}')

    
    async def close(self):
        await self.client.close()