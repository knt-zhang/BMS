from prettytable import PrettyTable

# create client
def create_client(cnx):
    cur = cnx.cursor()
    print("\n~SELECTED CREATE~\n-> Enter the following information to create a new Client account!")
    name = input("-> Please enter the client's name: ")
    address = input("-> Please enter the client's address: ")
    phone = input("-> Please enter the client's phone number: ")
    idBranch = input("-> Please enter a Branch ID: ")
    query = (
        "INSERT INTO clients (name, address, phone, idBranch)"
        "VALUES (%s, %s, %s, %s)"
        )
    data = (name, address, phone, idBranch,)
    cur.execute(query, data)
    cnx.commit(); "\n"

    query = "SELECT idClient, name, address, phone, idBranch FROM clients ORDER BY idClient DESC LIMIT 1"
    cur.execute(query)
    results = cur.fetchall()
    table = PrettyTable(['Client ID','Name','Address','Phone Number','Branch ID'])
    for idClient, name, address, phone, idBranch in results:
        table.add_row([idClient, name, address, phone, idBranch])
    print(table)
    print({True: "\nSuccessfully created the {}'s' account!".format(name),
        False: "\nUnable to create the {}'s account!".format(name)} [cur.rowcount==1])

# delete client using idClient record
def delete_client(cnx, client_selection):
    cur = cnx.cursor()
    display_current_client(cnx, client_selection)
    print("\n~SELECTED DELETE~")
    confirm = input("-> Please confirm that you would like to delete this current client? [Y/n] ")
    if confirm == 'Yes' or confirm == 'yes' or confirm == 'Y' or confirm == 'y':
        one = return_ck_idAccount(cnx, client_selection)
        two = return_s_idAccount(cnx, client_selection)
        three = return_cc_idAccount(cnx, client_selection)
        four = return_l_idAccount(cnx, client_selection)
        query = "DELETE FROM checking WHERE idAccount = %s;"
        data = (one)
        cur.executemany(query, data)
        cnx.commit()
        query = "DELETE FROM saving WHERE idAccount = %s;"
        data = (two)
        cur.executemany(query, data)
        cnx.commit()
        query = "DELETE FROM credit_card WHERE idAccount = %s;"
        data = (three)
        cur.executemany(query, data)
        cnx.commit()
        query = "DELETE FROM loan WHERE idAccount = %s;"
        data = (four)
        cur.executemany(query, data)
        cnx.commit()
        query = "DELETE FROM account WHERE idClient = {}".format(client_selection)
        cur.execute(query)
        cnx.commit()
        query = "DELETE FROM clients WHERE idClient = {}".format(client_selection)
        cur.execute(query)
        cnx.commit()
        print({True: "\nSuccessfully deleted Client with an ID of {}!".format(client_selection), \
            False: "\nUnable to delete Client ID: {}!".format(client_selection)} \
            [cur.rowcount==1])
    else:
        print("Selected no")


# client update column
def update_client(cnx, client_selection):
    cur = cnx.cursor()
    display_current_client(cnx, client_selection)
    print("\n~SELECTED UPDATE~\nColumns: [idClient | name | address | phone | idBranch]")
    column = input("-> Please enter the column you would like to modify: ")
    newValue = input("-> Please enter a new value for the column: ")
    query = 'UPDATE clients SET {} = \"{}\" WHERE idClient = {}'.format(column, newValue, client_selection)
    cur.execute(query)
    cnx.commit()
    display_current_client(cnx, client_selection)
    print({True: "\nSuccessfully updated {} to {}!".format(column, newValue), \
        False: "\nUnable to update your {}!".format(column)} \
        [cur.rowcount==1])

def display_clients(cnx, id):
    cur = cnx.cursor()
    query = "SELECT * FROM clients WHERE idBranch = %s"
    value = (id,)
    cur.execute(query, value)
    results = cur.fetchall()
    table = PrettyTable(['Client ID','Name','Address','Phone Number','Branch ID'])
    for idClient, name, address, phone, idBranch in results:
        table.add_row([idClient, name, address, phone, idBranch])
    print("\n~ Client Menu ~")
    print(table)

def display_current_client(cnx, client_selection):
    cur = cnx.cursor()
    query = "SELECT * FROM clients WHERE idClient = %s"
    value = (client_selection,)
    cur.execute(query, value)
    results = cur.fetchall()
    table = PrettyTable(['Client ID','Name','Address','Phone Number','Branch ID'])
    for idClient, name, address, phone, idBranch in results:
        table.add_row([idClient, name, address, phone, idBranch])
    print(table)

def compareClientID(cnx, branch_selection, client_selection):
    cur = cnx.cursor()
    query = "SELECT idClient FROM clients WHERE idBranch = {}".format(branch_selection)
    cur.execute(query)
    all_IDs = (cur.fetchall())
    for id in all_IDs:
        if int(client_selection) == int(id[0]):
            return True
    return False

def return_ck_idAccount(cnx, client_selection):
    cur = cnx.cursor()
    query = """
    SELECT ck.idAccount FROM checking ck, account acc, clients c WHERE c.idClient = acc.idClient and acc.idAccount = ck.idAccount and c.idClient = %s;
    """
    cur.execute(query, (client_selection,))
    results = cur.fetchall()
    return(results)

def return_s_idAccount(cnx, client_selection):
    cur = cnx.cursor()
    query = """
    SELECT s.idAccount FROM saving s, account acc, clients c WHERE c.idClient = acc.idClient and acc.idAccount = s.idAccount and c.idClient = %s;
    """
    cur.execute(query, (client_selection,))
    results = cur.fetchall()
    return(results)

def return_cc_idAccount(cnx, client_selection):
    cur = cnx.cursor()
    query = """
    SELECT cc.idAccount FROM credit_card cc, account acc, clients c WHERE c.idClient = acc.idClient and acc.idAccount = cc.idAccount and c.idClient = %s;
    """
    cur.execute(query, (client_selection,))
    results = cur.fetchall()
    return(results)

def return_l_idAccount(cnx, client_selection):
    cur = cnx.cursor()
    query = """
    SELECT l.idAccount FROM loan l, account acc, clients c WHERE c.idClient = acc.idClient and acc.idAccount = l.idAccount and c.idClient = %s;
    """
    cur.execute(query, (client_selection,))
    results = cur.fetchall()
    return(results)
