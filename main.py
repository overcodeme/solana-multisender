import asyncio
from core.sender import Sender
from utils.logger import logger
import os

os.system('cls' if os.name == 'nt' else 'clear')

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
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f'Wallet balance: {await wallet.get_balance()} SOL')
        elif choice == '2':
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f'Current gas_fee: {await wallet.get_gas_fee()} SOL')
        elif choice == '3':
            os.system('cls' if os.name == 'nt' else 'clear')
            try:
                if address_list:
                    sol_amount = float(input('Input SOL amount: '))
                    print(f'Found {len(address_list)} wallets')

                    while True:
                        print(f'Total amount you gonna pay is {sol_amount * len(address_list) + len(address_list) * (await wallet.get_gas_fee())} SOL')
                        res = input('Do you want to continue? (yes, no): ')
                        os.system('cls' if os.name == 'nt' else 'clear')
                        if res ==  'yes':
                            tasks = [wallet.send(recipient, sol_amount) for recipient in address_list]
                            await asyncio.gather(*tasks)
                            logger.info(f'Wallet balance after all transactions: {await wallet.get_balance()} SOL')
                        elif res == 'no':
                            break
                        else:
                            print('Invalid option. Please try again.')
                else:
                    logger.error('No wallets in txt file')
            except:
                logger.error('Not enough SOL for all transactions')
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print('Invalid option. Please try again.')
                


if __name__ == '__main__':
    asyncio.run(main())
    