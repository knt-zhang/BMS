from prettytable import PrettyTable

def l_balance(cnx, id):
    cur = cnx.cursor()
    query = (
        "SELECT l.idAccount,  c.name, l.amount, l.type_of_loan \
        FROM loan l, account acc, clients c \
        WHERE l.idAccount = acc.idAccount and acc.idClient = c.idClient and l.idAccount = %s"
    )
    value = (id,)
    cur.execute(query, value)
    results = cur.fetchall()
    table = PrettyTable(['Account ID', 'Client Name', 'Loan Amount', 'Type of Loan'])
    for idAccount, name, amount, type_of_loan in results:
        table.add_row([idAccount, name, amount, type_of_loan])
    print("\n~ Loan Account ~")
    print(table)

def l_pay(cnx, id):
    cur = cnx.cursor()
    amount = input('\n~SELECTED LOAN PAYMENT~\n-> How much would you like to pay? $')
    query = "UPDATE loan SET amount = (amount - %s) where idAccount = %s"
    data = (amount, id,)
    cur.execute(query, data)
    cnx.commit()
    l_balance(cnx, id)
    print({True: "\nSuccessfully paid off ${} from your Loan balance!".format(amount), \
        False: "\nUnable to pay off ${} from your Loan balance!".format(amount)} \
        [cur.rowcount==1])
