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
            lamports = int(amount * SOL_TO_LAMPORTS)

            recent_blockhash_response = await self.client.get_latest_blockhash()
            blockhash = recent_blockhash_response.value.blockhash

            # Создаем сообщение для транзакции
            message = transfer(
                from_pubkey=self.keypair.pubkey(),
                to_pubkey=Pubkey.from_string(recipient),
                lamports=lamports
            )

            # Создаем транзакцию с необходимыми параметрами
            transaction = Transaction(
                from_keypairs=[self.keypair],
                message=message,
                recent_blockhash=blockhash
            )

            response = await self.client.send_transaction(transaction, self.keypair)
            logger.success(f'Successfully sent {amount} SOL to {recipient}. Transaction ID: {response["result"]}')
        except Exception as e:
            logger.error(f'Error sending to {recipient}: {e}')

    
    async def close(self):
        await self.client.close()
