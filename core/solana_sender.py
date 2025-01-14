from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey
from solders.keypair import Keypair
from solders.system_program import TransferParams, transfer
from solders.transaction import Transaction, VersionedTransaction
from solders.message import MessageV0
from utils.logger import logger
from data.config import PRIVATE_KEY

SOL_TO_LAMPORTS = 1_000_000_000

class Sender:
    
    def __init__(self, private_key=PRIVATE_KEY):
        self.client = AsyncClient("https://api.mainnet-beta.solana.com")
        self.keypair = Keypair.from_base58_string(private_key)
    

    async def get_balance(self):
        balance = await self.client.get_balance(self.keypair.pubkey())
        return balance.value / SOL_TO_LAMPORTS


    async def send(self, recipient: str, amount: float):
        try:
            lamports = int(amount * SOL_TO_LAMPORTS)
            receiver_pubkey = Pubkey.from_string(recipient)

            ix = transfer(
                TransferParams(
                    from_pubkey=self.keypair.pubkey(),
                    to_pubkey=receiver_pubkey,
                    lamports=lamports
                )
            )

            recent_blockhash_response = await self.client.get_latest_blockhash()
            blockhash = recent_blockhash_response.value.blockhash

            message = MessageV0.try_compile(
                payer = self.keypair.pubkey(),
                instructions = [ix],
                address_lookup_table_accounts=[],
                recent_blockhash = blockhash
            )

            tx = VersionedTransaction(message, [self.keypair])

            response = await self.client.send_transaction(tx)
            logger.info(f'Successfully sent {amount} SOL to {recipient}. Transaction ID: {response["result"]}')
        except Exception as e:
            logger.error(f'Error sending to {recipient}: {e}')
        finally:
            await self.client.close()

    
    async def close(self):
        await self.client.close()
