from prettytable import PrettyTable

def c_withdrawal(cnx, id):
    cur = cnx.cursor()
    amount = input('\n~ SELECTED CHECKINGS WITHDRAWAL ~\n-> How much would you like to withdraw? $')
    print('\n')
    query = "UPDATE checking SET balance = (balance - %s) where idAccount = %s"
    data = (amount, id,)
    cur.execute(query, data)
    cnx.commit()
    c_balance(cnx, id)
    print({True: "\nSuccessfully withdrew ${} from your Checking balance!".format(amount), \
        False: "\nUnable to withdraw ${} from your Checking balance!".format(amount)} \
        [cur.rowcount==1])

def c_deposit(cnx, id):
    cur = cnx.cursor()
    amount = input('\n~ SELECTED CHECKINGS DEPOSIT ~\n-> How much would you like to deposit? $')
    query = "UPDATE checking SET balance = (balance + %s) where idAccount = %s"
    data = (amount, id,)
    cur.execute(query, data)
    cnx.commit()
    c_balance(cnx, id)
    print({True: "\nSuccessfully added ${} to your Checking balance!".format(amount), \
        False: "\nUnable to add ${} to your Checking balance!".format(amount)} \
        [cur.rowcount==1])

def c_balance(cnx, id):
    cur = cnx.cursor()
    query = (
        "SELECT ck.idAccount, c.name, ck.balance \
        FROM checking ck, account acc, clients c \
        WHERE ck.idAccount = acc.idAccount and acc.idClient = c.idClient and ck.idAccount = %s"
    )
    value = (id,)
    cur.execute(query, value)
    results = cur.fetchall()
    table = PrettyTable(['Account ID', 'Client Name', 'Checking balance'])
    for idAccount, name, balance in results:
        table.add_row([idAccount, name, balance])
    print("\n~ Checking Account ~")
    print(table)
