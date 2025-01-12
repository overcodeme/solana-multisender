import asyncio
from core.solana_sender import Wallet
from utils.logger import logger


async def main():
    wallet = Wallet(recipient=None)
    balance = await wallet.get_balance()
    print(f'Wallet balance: {balance} SOL')

    try:
        sol_amount = float(input('Input SOL amount: '))
        address_list = []

        with open('data/address_list.txt', 'r') as file:
            address_list = [address.strip() for address in file.readlines()]


        tasks = [wallet.send(recipient, sol_amount) for recipient in address_list]

        await asyncio.gather(*tasks)
        await wallet.close()

        logger.info(f'Wallet balance after all transactions: {wallet.get_balance()}')
    except:
        logger.error(f'Not enough SOL for all transactions')


if __name__ == '__main__':
    asyncio.run(main())
    