from prettytable import PrettyTable

def display_accounts(cnx, user_selection):
    cur = cnx.cursor()
    query = "SELECT idAccount, account_type FROM account WHERE idClient = %s"
    cur.execute(query, (user_selection,))
    results = cur.fetchall()
    table = PrettyTable(['Account ID','Account Type'])
    for idAccount, account_type in results:
        table.add_row([idAccount, account_type])
    print("\n~ Accounts available for this client ~")
    print(table)
    return results

def returnAccountiD(cnx, account_type, idClient):
    cur = cnx.cursor()
    query = "SELECT acc.idAccount FROM account acc, clients c WHERE c.idClient = acc.idClient and acc.account_type = %s and c.idClient = %s"
    value = (account_type, idClient,)
    cur.execute(query, value)
    result = (cur.fetchone())[0]
    return(result)

def select_account(cnx, account_selection):
    cur = cnx.cursor()
    query = "SELECT acc.idAccount FROM account acc, credit_card cc, checking ck,\
            saving s, loan l WHERE acc.idAccount = cc.idAccount, acc.idAccount = ck.idAccount,\
            acc.idAccount = s.idAccount, acc.idAccount = l.idAccount,\
            acc.idAccount = {}".format(account_selection)
    value = (account_selection,)
    cur.execute(query, value)
    results = cur.fetchall()
    print(results)

def trigger():
    trig = input("\n-> Press [ENTER] to CONTINUE: ")
    print("\nAVAILABLE CLIENTS:")

def trigger_next():
    trig = input("\n-> Press [ENTER] to CONTINUE: ")

def transaction_isolation(cnx):
    cur = cnx.cursor()
    query = "set global transaction_isolation='serializable';"
    cur.execute(query)
