from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey
from solders.keypair import Keypair
from solders.system_program import TransferParams, transfer
from solders.transaction import VersionedTransaction
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
    

    async def get_gas_fee(self):
        try:
            lamports = 1_000_000_000
            receiver_pubkey = Pubkey.from_string('Fd2vuPqWwVoxnEe8gjYonb2qq251HPwPFgtzrQoX5wKJ') # Test address for checking gas fee

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
                address_lookup_table_accounts = [],
                recent_blockhash = blockhash
            )

            fee_response = await self.client.get_fee_for_message(message)
            return fee_response.value / SOL_TO_LAMPORTS
        except Exception as e:
            logger.error(f'Error getting gas fee: {e}')
            return None



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
                address_lookup_table_accounts = [],
                recent_blockhash = blockhash
            )

            tx = VersionedTransaction(message, [self.keypair])

            response = await self.client.send_transaction(tx)
            logger.success(f'Successfully sent {amount} SOL to {recipient}. Transaction ID: {response["result"]}')
        except Exception:
            logger.error(f'Error sending to {recipient}: {response['result']}')
        finally:
            await self.client.close()
