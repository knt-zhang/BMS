import os, mysql.connector
from mysql.connector import errorcode
from prettytable import PrettyTable
from PROD_Checking import *
from PROD_Client import *
from PROD_CreditCard import *
from PROD_Loan import *
from PROD_Saving import *
from PROD_Account import *
from PROD_View import *
from PROD_DDL import *

cnx = mysql.connector.connect(user=[YOUR USERNAME], password=[YOUR PASSWORD], host='localhost', database='bank_management_system')

# ###############################################################################
# # BRANCH
# ###############################################################################

def display_branch(cnx):
    query = 'SELECT idBranch, name FROM branch'
    cur = cnx.cursor(buffered=True)
    cur.execute(query)
    results = cur.fetchall()
    table = PrettyTable(['Branch ID', 'Name'])
    for idBranch, name in results:
        table.add_row([idBranch, name])
    print('\n~ Available branches ~'); print(table)

# main
def main():
    print("\nWelcome to the Admin Bank Management System")
    transaction_isolation(cnx)
    c_transaction(cnx)

    # display branches
    while True:
        display_branch(cnx)
        branch_selection = input("\n-> Please select a Branch ID: ")
        if branch_selection == '1' or branch_selection == '2' or branch_selection == '3':
            break
        print('\nYour input was not a valid selection. Please try again!\n')

    # display client view
    while True:
        while True:
            while True:
                branch_summary = []
                branch_summary.append(branch_ck_summary(cnx, 1))
                branch_summary.append(branch_cc_summary(cnx, 1))
                branch_summary.append(branch_s_summary(cnx, 1))
                branch_summary.append(branch_l_summary(cnx, 1))
                table = PrettyTable(['Checking Balances', 'Savings Balances', 'Credit Card Balances', 'Loan Balances'])
                table.add_row(branch_summary)
                print("\n~ Branch Summary ~"); print(table)

                display_clients(cnx, branch_selection)
                client_selection = input("\n-> Please select a Client ID: ")
                try:
                    val = int(client_selection)
                    break
                except ValueError:
                    print('\nYour input was not a valid selection. Please try again!\n')

            if compareClientID(cnx, branch_selection, client_selection):
                print("\nYou selected Client ID # {}\n".format(client_selection))
                break
            else:
                display_clients(cnx, branch_selection)
                print('\nYour input was not a valid selection. Please try again!\n')

        display_current_client(cnx, client_selection)
        print("\n" + "*" * 106 + "\n* [Add a client | Delete a client | Update existing information on client | View current client summary] *\n" + "*" * 106)
        modify_client = input("-> Modify the current client [Y/n]? "); print("\n")

        if modify_client == 'Yes' or modify_client == 'yes' or modify_client == 'y' or modify_client == 'Y':
            while True:
                display_current_client(cnx, client_selection)
                print("\n" + "*" * 111 + "\n* [1] Add client | [2] Delete client | [3] Update current client | [4] View current client summary | [0] Exit *\n" + "*" * 111)
                selection = input("-> Please select an option: ")
                if selection == '1':
                    create_client(cnx)
                    trigger()
                    break
                elif selection == '2':
                    delete_client(cnx, client_selection)
                    trigger()
                    break
                elif selection == '3':
                    update_client(cnx, client_selection)
                    trigger()
                elif selection == '4':
                    client_summary_view(cnx, client_selection)
                    trigger()
                elif selection =='5':
                    display_updated_clients(cnx)
                    trigger()
                elif selection == '0':
                    break
                else:
                    print('\nYour input was not a valid selection. Please try again!\n')

        elif modify_client == 'No' or modify_client == 'no' or modify_client == 'n' or modify_client == 'N':
            break
        else:
            print('\nYour input was not a valid selection. Please try again!\n')

    # display user information
    while True:
        temp = 1
        while temp:
            user_account = display_accounts(cnx, client_selection)
            print("\n" + "*" * 43 + "\n* [B] Return to the beginning | [Q] Quit: *\n" + "*" * 43)
            account_selection = input("-> Please select an available account ID: ")
            try:
                val = int(account_selection)
                for entry in user_account:
                    if int(entry[0]) == int(account_selection):
                        account_type = entry[1]
                        temp = 0
            except ValueError:
                if account_selection == "b" or account_selection == "B":
                    main()
                elif account_selection == "q" or account_selection == "Q":
                    quit()
                print('\nYour input was not a valid selection. Please try again!\n')

        if account_type == 'checking':
            c_balance(cnx, account_selection)
            while True:
                print("\n" + "*" * 110 + "\n* [D] Deposit | [W] Withdraw | [V] View balance | [H] View transaction history | [L] Leaderboard | [B] Exit: *\n" + "*" * 110)
                checking = input("\n-> Please select an option: ")
                if checking == "d" or checking == "D":
                    c_deposit(cnx, account_selection)
                    trigger_next()
                elif checking == "w" or checking == "W":
                    c_withdrawal(cnx, account_selection)
                    trigger_next()
                elif checking == "v" or checking == "V":
                    c_balance(cnx, account_selection)
                    trigger_next()
                elif checking == "h" or checking == "H":
                    c_records(cnx, account_selection)
                    trigger_next()
                elif checking == "l" or checking == "L":
                    checking_rank(cnx)
                    display_rank(cnx, client_selection)
                    trigger_next()
                elif checking == "b" or checking == "B":
                    break
                else:
                    print('\nYour input was not a valid selection. Please try again!\n')

        elif account_type == 'credit_card':
            cc_balance(cnx, account_selection)
            while True:
                print("\n" + "*" * 74 + "\n* [P] Pay | [V] View balance | [R] View credit score ratings | [B] Exit: *\n" + "*" * 74)
                cc = input("-> Please select an option: ")
                if cc == "p" or cc == "P":
                    cc_pay(cnx, account_selection)
                    trigger_next()
                elif cc == "v" or cc == "V":
                    cc_balance(cnx, account_selection)
                    trigger_next()
                elif cc == "r" or cc == "R":
                    credit_score(cnx)
                    display_credit_score(cnx, client_selection)
                    trigger_next()
                elif cc == "b" or cc == "B":
                    break
                else:
                    print('\nYour input was not a valid selection. Please try again!\n')

        elif account_type == 'loan':
                l_balance(cnx, account_selection)
                while True:
                    print("\n" + "*" * 69 + "\n* [P] Pay | [V] View balance | [C] View loan calculator | [B] Exit: *\n" + "*" * 69)
                    loan = input("-> Please select an option: ")
                    if loan == "p" or loan == "P":
                        l_pay(cnx, account_selection)
                        trigger_next()
                    elif loan == "v" or loan == "V":
                        l_balance(cnx, account_selection)
                        trigger_next()
                    elif loan == "c" or loan == "C":
                        l_calculator(cnx)
                        trigger_next()
                    elif loan == "b" or loan == "B":
                        break
                    else:
                        print('\nYour input was not a valid selection. Please try again!\n')

        elif account_type == 'saving':
            s_balance(cnx, account_selection)
            while True:
                print("\n" + "*" * 91 + "\n* [D] Deposit | [W] Withdraw | [V] View balance | [C] View savings calculator | [B] Exit: *\n" + "*" * 91)
                saving = input("-> Please select an option: ")
                if saving == "d" or saving == "D":
                    s_deposit(cnx, account_selection)
                    trigger_next()
                elif saving == "w" or saving == "W":
                    s_withdraw(cnx, account_selection)
                    trigger_next()
                elif saving == "v" or saving == "V":
                    s_balance(cnx, account_selection)
                    trigger_next()
                elif saving == "c" or saving == "C":
                    s_calculator(cnx)
                    trigger_next()
                elif saving == "b" or saving == "B":
                    break
                else:
                    print('\nYour input was not a valid selection. Please try again!\n')
        else:
            print('\nInput was not one of the options. Try again.\n')

    # close db connection
    cnx.close()

if __name__ == '__main__':
    main()
