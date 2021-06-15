from prettytable import PrettyTable

# display CC balance, limit | add (deposit = pay off),
def cc_pay(cnx, id):
    cur = cnx.cursor()
    amount = input('\n~ SELECTED CREDIT CARD PAYMENT ~\n-> How much would you like to pay? $')
    query = "UPDATE credit_card SET balance = (balance - %s) where idAccount = %s"
    data = (amount, id,)
    cur.execute(query, data)
    cnx.commit()
    cc_balance(cnx, id)
    print({True: "\nSuccessfully paid off ${} from your Credit card balance!".format(amount), \
        False: "\nUnable to pay off ${} from your Credit card balance!".format(amount)} \
        [cur.rowcount==1])

def cc_balance(cnx, id):
    cur = cnx.cursor()
    query = (
        "SELECT cc.idAccount,  c.name, cc.balance, cc.credit_limit \
        FROM credit_card cc, account acc, clients c \
        WHERE cc.idAccount = acc.idAccount and acc.idClient = c.idClient and cc.idAccount = %s"
    )
    value = (id,)
    cur.execute(query, value)
    results = cur.fetchall()
    table = PrettyTable(['Account ID', 'Client Name', 'Credit Card Balance', 'Credit Card Limit'])
    for idAccount, name, balance, credit_limit in results:
        table.add_row([idAccount, name, balance, credit_limit])
    print("\n~ Credit Card Account ~")
    print(table)
