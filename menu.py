import os
from getpass import getpass
from sys import exit
from netcheck import CheckNetwork
from netchange import ChangeNetwork
#import logging


username = input('\nUsername : ')
pwd = getpass()
chg, chk = ChangeNetwork(username, password=pwd), CheckNetwork(username, password=pwd)

#logging.basicConfig(filename='/opt/script/menu/menu.log',filemode='a', format='%(asctime)s %(name)s  %(levelname)s - %(message)s', datefmt="%b %d-%Y %H:%M:%S", level=logging.DEBUG)
#logger = logging.getLogger("Network")

def main_menu():
    os.system('clear')
    print("\nWelcome, \n\n")
    print("1. Check Connection")
    print("2. Change Configuration")
    print("3. Type Custom Command")
    print("4. Backup Configuration")
    print("\n\n Type 'q' for Quit\n")
    choice = input(" >>  ").lower()
    if choice == '':
        main_menu()
    else:
        try:
            main_menus[choice]()
        except KeyError:
            print("Invalid selection, Please try again.\n")
            main_menu()
    return


def checking_configuration():
    os.system('clear')
    print("\n Check Connection Menu\n\n")
    print("1. Check Internet Connection")
    print("2. Check Bank Leaseline Connection")
    print("3. Check Metro-E Connection")
    print("\n\n0. Back\n")
    print("Type 'q' for Quit\n")
    choice = input(" >>  ").lower()
    if choice == '':
        checking_configuration()
    else:
        try:
            check_config_menu[choice]()
        except KeyError:
            print("Invalid selection, Please try again.\n")
            checking_configuration()
    return

def check_bank():
    os.system('clear')
    print("\n Check Leaseline To Bank\n\n")
    print("1. Check BCA Connection")
    print("2. Check BRI Connection")
    print("3. Check Mandiri Connection")
    print("4. Check BNI Connection")
    print("5. Check Danamon Connection")
    print("\n\n0. Back")
    print("Type 'q' for Quit\n")
    choice = input(" >>  ").lower()
    if choice == '':
        check_bank()
    else:
        try:
            check_bank_menu[choice]()
        except KeyError:
            print("Invalid selection, Please try again.\n")
            check_bank()
    return

def change_bank():
    os.system('clear')
    print("\n Change Leaseline To Bank\n\n")
    print("1. Change BRI To Telkom")
    print("2. Change BRI To Lintasarta")
    print("3. Change BNI To Telkom")
    print("4. Change BNI To Lintasarta")
    print("5. Change Danamon To Telkom")
    print("6. Change Danamon To Lintasarta")
    print("\n\n0. Back")
    print("Type 'q' for Quit\n")
    choice = input(" >>  ").lower()
    if choice == '':
        change_bank()
    else:
        try:
            change_bank_menu[choice]()
        except KeyError:
            print("Invalid selection, Please try again.\n")
            change_bank()
    return

def change_configuration():
    os.system('clear')
    print("\n Change Configuration Menu\n\n")
    print("1. Change Internet Connection To Lintasarta")
    print("2. Change Internet Connection To Telkom")
    print("3. Change Domestic Connection To Lintasarta")
    print("4. Change Domestic Connection To Telkom")
    print("5. Change International Connection To Lintasarta")
    print("6. Change International Connection To Telkom")
    print("7. Change Bank Leaseline Connection")
    print("\n\n0. Back")
    print("Type 'q' for Quit\n")
    choice = input(" >>  ").lower()
    if choice == '':
        change_configuration()
    else:
        try:
            change_config_menu[choice]()
        except KeyError:
            print("Invalid selection, Please try again.\n")
            change_configuration()
    return


def exit_menu():
    exit()

main_menus = {
    '1': checking_configuration,
    '2': change_configuration,
    #    '3': custom_command,
    #    '4': backup_configuration,
    'q': exit_menu,
}

check_config_menu = {
    '1': chk.check_inet,
    '2': check_bank,
    '3': chk._check_metro,
    '0': main_menu,
    'q': exit_menu,
}

check_bank_menu = {
    '1': chk.check_bca,
    '2': chk.check_bri,
    '3': chk.check_mandiri,
    '0': main_menu,
    'q': exit_menu,
}
change_bank_menu = {
    '1': chg.change_bri_tlkm,
    '2': chg.change_bri_lintas,
    '3': chg.change_bni_tlkm,
    '4': chg.change_bni_lintas,
    '5': chg.change_danamon_tlkm,
    '6': chg.change_danamon_lintas,
    '0': change_configuration,
    'q': exit_menu,
}

change_config_menu = {
    '1': chg.change_to_lintas,
    '2': chg.change_to_telkom,
    '3': chg.change_la_domestic,
    '4': chg.change_telkom_domestic,
    '5': chg.change_la_global,
    '6': chg.change_telkom_global,
    '7': change_bank,
    '0': main_menu,
    'q': exit_menu,
}

if __name__ == "__main__":
    main_menu()