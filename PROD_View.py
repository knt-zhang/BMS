from prettytable import PrettyTable

# --- 1 View DDL --- #

def client_summary_view(cnx, id):
    cur = cnx.cursor()
    print('\n~ Account summary of the available assets for this client ~')
    queries = (
        "DROP VIEW IF EXISTS checking_summary;\
        CREATE VIEW checking_summary AS\
        	SELECT 'checking', ck.balance FROM checking ck, account acc, clients c\
            WHERE ck.idAccount = acc.idAccount and acc.idClient = c.idClient and c.idClient = %s;"

        "DROP VIEW IF EXISTS saving_summary;\
        CREATE VIEW saving_summary AS\
        	SELECT 'saving', s.balance, s.interest FROM saving s, account acc, clients c\
            WHERE s.idAccount = acc.idAccount and acc.idClient = c.idClient and c.idClient = %s;"

        "DROP VIEW IF EXISTS cc_summary;\
        CREATE VIEW cc_summary AS\
        	SELECT 'credit_card', cc.balance, cc.credit_limit FROM credit_card cc, account acc, clients c\
            WHERE cc.idAccount = acc.idAccount and acc.idClient = c.idClient and c.idClient = %s;"

        "DROP VIEW IF EXISTS loan_summary;\
        CREATE VIEW loan_summary AS\
        	SELECT 'loan', l.amount, l.type_of_loan FROM loan l, account acc, clients c\
            WHERE l.idAccount = acc.idAccount and acc.idClient = c.idClient and c.idClient = %s;"
    )
    data = (id, id, id, id,)
    cur.execute(queries, data)
    ck_view(cnx)
    s_view(cnx)
    cc_view(cnx)
    l_view(cnx)

# --- 4 Reports --- #

def branch_ck_summary(cnx, id):
    cur = cnx.cursor()
    query = """
        DROP VIEW IF EXISTS branch_ck_balance;
        CREATE VIEW branch_ck_balance AS
            SELECT CONCAT('$', FORMAT(SUM(ck.balance), 0)) 'Checking Summary' FROM branch b, account acc, checking ck
            WHERE b.idBranch = acc.idBranch and acc.idAccount = ck.idAccount and b.idbranch = %s;
    """
    cur.execute(query, (id,))
    query = "SELECT * FROM branch_ck_balance;"
    cnx.reconnect()
    cur.execute(query)
    results = cur.fetchone()
    return(results[0])

def branch_s_summary(cnx, id):
    cur = cnx.cursor()
    query = """
        DROP VIEW IF EXISTS branch_s_balance;
        CREATE VIEW branch_s_balance AS
            SELECT CONCAT('$', FORMAT(SUM(s.balance), 0)) 'Savings Summary' FROM branch b, account acc, saving s
            WHERE b.idBranch = acc.idBranch and acc.idAccount = s.idAccount and b.idbranch = %s;
    """
    cur.execute(query, (id,))
    query = "SELECT * FROM branch_s_balance;"
    cnx.reconnect()
    cur.execute(query)
    results = cur.fetchone()
    return(results[0])

def branch_cc_summary(cnx, id):
    cur = cnx.cursor()
    query = """
        DROP VIEW IF EXISTS branch_cc_balance;
        CREATE VIEW branch_cc_balance AS
            SELECT CONCAT('$', FORMAT(SUM(cc.balance), 0)) 'Credit Card Summary' FROM branch b, account acc, credit_card cc
            WHERE b.idBranch = acc.idBranch and acc.idAccount = cc.idAccount and b.idbranch = %s;
    """
    cur.execute(query, (id,))
    query = "SELECT * FROM branch_cc_balance;"
    cnx.reconnect()
    cur.execute(query)
    results = cur.fetchone()
    return(results[0])

def branch_l_summary(cnx, id):
    cur = cnx.cursor()
    query = """
        DROP VIEW IF EXISTS branch_l_balance;
        CREATE VIEW branch_l_balance AS
            SELECT CONCAT('$', FORMAT(SUM(l.amount), 0)) 'Loan Summary' FROM branch b, account acc, loan l
            WHERE b.idBranch = acc.idBranch and acc.idAccount = l.idAccount and b.idbranch = %s;
    """
    cur.execute(query, (id,))
    query = "SELECT * FROM branch_l_balance;"
    cnx.reconnect()
    cur.execute(query)
    results = cur.fetchone()
    return(results[0])

def ck_view(cnx):
    cnx.reconnect()
    cur = cnx.cursor()
    query = """
        SELECT * FROM checking_summary;
        """
    cur.execute(query)
    results = cur.fetchall()
    table = PrettyTable(['Account Type', 'Checking Balance'])
    for balance in results:
        table.add_row(balance)
    print(table)

def s_view(cnx):
    cnx.reconnect()
    cur = cnx.cursor()
    query = "SELECT * FROM saving_summary;"
    cur.execute(query)
    results = cur.fetchall()
    table = PrettyTable(['Account Type', 'Saving Balance', 'Interest'])
    for balance in results:
        table.add_row(balance)
    print(table)

def cc_view(cnx):
    cnx.reconnect()
    cur = cnx.cursor()
    query = "SELECT * FROM cc_summary;"
    cur.execute(query)
    results = cur.fetchall()
    table = PrettyTable(['Account Type', 'Credit Card Balance', 'Credit Card Limit'])
    for balance in results:
        table.add_row(balance)
    print(table)

def l_view(cnx):
    cnx.reconnect()
    cur = cnx.cursor()
    query = "SELECT * FROM loan_summary;"
    cur.execute(query)
    results = cur.fetchall()
    table = PrettyTable(['Account Type', 'Loan Balance', 'Type of Loan'])
    for balance in results:
        table.add_row(balance)
    print(table)
