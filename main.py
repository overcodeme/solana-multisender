import asyncio
from core.solana_sender import Wallet


async def main():
    sol_amount = float(input('Input SOL amount: '))
    address_list = []

    with open('data/address_list.txt', 'r') as file:
        address_list = [address.strip() for address in file.readlines()]

    wallet = Wallet()

    tasks = [wallet.send(recipient, sol_amount) for recipient in address_list]

    await asyncio.gather(*tasks)
    await wallet.close()


if __name__ == '__main__':
    asyncio.run(main)
    