import mysql.connector
from mysql.connector import errorcode
from prettytable import PrettyTable

# display saving's balance, int rate | update (withdrawal), add (deposit)
def s_withdraw(cnx, id):
    cur = cnx.cursor()
    amount = input('\n~ SELECTED SAVINGS WITHDRAWAL ~\n-> How much would you like to withdraw? $')
    query = "UPDATE saving SET balance = (balance - %s) where idAccount = %s"
    data = (amount, id,)
    cur.execute(query, data)
    cnx.commit()
    s_balance(cnx, id)
    print({True: "\nSuccessfully withdrew ${} from your balance in Saving!".format(amount), \
        False: "\nUnable to withdraw ${} from your balance in Saving!".format(amount)} \
        [cur.rowcount==1])

def s_deposit(cnx, id):
    cur = cnx.cursor()
    amount = input('\n~ SELECTED SAVINGS DEPOSIT ~\n-> How much would you like to deposit? $')
    query = "UPDATE saving SET balance = (balance + %s) where idAccount = %s"
    data = (amount, id,)
    cur.execute(query, data)
    cnx.commit()
    s_balance(cnx, id)
    print({True: "\nSuccessfully added ${} to your Saving balance!".format(amount), \
        False: "\nUnable to add ${} to your Saving balance!".format(amount)} \
        [cur.rowcount==1])

def s_balance(cnx, id):
    cur = cnx.cursor()
    query = (
        "SELECT s.idAccount,  c.name, s.balance, s.interest \
        FROM saving s, account acc, clients c \
        WHERE s.idAccount = acc.idAccount and acc.idClient = c.idClient and s.idAccount = %s"
    )
    value = (id,)
    cur.execute(query, value)
    results = cur.fetchall()
    table = PrettyTable(['Account ID', 'Client Name', 'Saving balance', 'Interest Rate'])
    for idAccount, name, balance, interest in results:
        table.add_row([idAccount, name, balance, interest])
    print("\n~ Saving Account ~")
    print(table)
