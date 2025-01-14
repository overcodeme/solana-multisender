import asyncio
from core.sender import Sender
from utils.logger import logger

wallet=Sender()
address_list = []
with open('data/address_list.txt', 'r') as file:
    address_list = [address.strip() for address in file.readlines()]


async def main():
    while True:
        print("\nMenu:")
        print("1. Get wallet balance")
        print("2. Get gas fee")
        print("3. Send SOL")
        print("4. Exit")

        choice = input('Choose an option(1-4): ')

        if choice == '1':
            print(f'Wallet balance: {await wallet.get_balance()} SOL')
        elif choice == '2':
            print(wallet.get_gas_fee())
        elif choice == '3':
            try:
                sol_amount = float(input('Input SOL amount: '))
                tasks = [wallet.send(recipient, sol_amount) for recipient in address_list]
                await asyncio.gather(*tasks)
                logger.info(f'Wallet balance after all transactions: {await wallet.get_balance()}')
            except:
                logger.error(f'Not enough SOL for all transactions')
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print('Invalid option. Please try again.')
                


if __name__ == '__main__':
    asyncio.run(main())
    