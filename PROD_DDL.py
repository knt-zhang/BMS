from prettytable import PrettyTable

# --- Procedure DDL --- #
def s_calculator(cnx):
    # Procedure DDL = savings_calculator
    cnx.reconnect()
    cur = cnx.cursor()
    initial_deposit = input('\n~Savings Calculator~\n-> How much would you like to deposit? $')
    max = input('How many years do you want to save for? ')
    print("Our bank interest rate is: 0.0125%")
    data = (initial_deposit, max,)
    query = """
        DROP PROCEDURE IF EXISTS savings_calculator;
        CREATE PROCEDURE savings_calculator (in initial_deposit INT, in max INT)
        BEGIN
            DECLARE counter INT DEFAULT 1;
            DECLARE Calculations DECIMAL(65,2);

            DROP TABLE IF EXISTS savings_table;
            CREATE TABLE savings_table (
                years INT,
                balance INT
            );

            WHILE(counter <= max)
        		DO BEGIN
        			IF initial_deposit > 0 THEN
        				SET calculations = initial_deposit + (initial_deposit * .0125 * counter);
        				INSERT INTO savings_table VALUES (counter, calculations);
        				SET counter = counter + 1;
        			END IF;
        		END;
            END WHILE;
        END
    """
    cur.execute(query)
    cnx.reconnect()
    cur.callproc('savings_calculator', data)
    query = "SELECT years, balance FROM savings_table;"
    cur.execute(query)
    results = cur.fetchall()
    table = PrettyTable(['Years','Savings'])
    for yrs, savings_interest in results:
        table.add_row([yrs, savings_interest])
    print(table)

def l_calculator(cnx):
    # PROCEDURE DDL = loan_calculator
    cur = cnx.cursor()
    initial_loan = input('\n~Loan Calculator~\n-> How much would you like to request? $')
    max = input('How many years until you pay off the loan? ')
    interest_rate = input('What is the interest rate? ')
    data = (initial_loan, max, interest_rate,)
    query = """
        DROP PROCEDURE IF EXISTS loan_calculator;
        CREATE PROCEDURE loan_calculator (in initial_loan INT, in max INT, in interest_rate DECIMAL(65,2))
        BEGIN
            DECLARE counter INT DEFAULT 1;
            DECLARE calculations DECIMAL(65,2);

            DROP TABLE IF EXISTS loan_table;
            CREATE TABLE loan_table (
                years INT,
                balance INT
            );

            WHILE(counter <= max)
        		DO BEGIN
        			IF initial_loan > 0 THEN
        				SET calculations = initial_loan + (initial_loan * (interest_rate/100) * counter);
        				INSERT INTO loan_table VALUES (counter, calculations);
        				SET counter = counter + 1;
        			END IF;
        		END;
            END WHILE;
        END

    """
    cur.execute(query)
    cnx.reconnect()
    cur.callproc('loan_calculator', data)
    query = "SELECT years, balance FROM loan_table;"
    cur.execute(query)
    results = cur.fetchall()
    table = PrettyTable(['Years','Loan Balance'])
    for yrs, loan_debt in results:
        table.add_row([yrs, loan_debt])
    print(table)



# --- 2 Function DDL --- #

def checking_rank(cnx):
    # leaderboard rating
    cur = cnx.cursor()
    query = """
        DROP FUNCTION IF EXISTS balance_leaderboard;
        CREATE FUNCTION balance_leaderboard(money DECIMAL(65,2))
        RETURNS VARCHAR(64)
        DETERMINISTIC
        BEGIN
            DECLARE ranking VARCHAR(64);
            IF money > 100000 THEN
                SET ranking = 'DIAMOND';
            ELSEIF(money <= 100000 and money >= 50000) THEN
                SET ranking = 'PLATINUM';
            ELSEIF(money <= 50000 and money >= 25000) THEN
                SET ranking = 'GOLD';
            ELSEIF(money <= 25000 and money >= 10000) THEN
                SET ranking = 'SILVER';
            ELSEIF money < 10000 THEN
                SET ranking = 'BRONZE';
            END IF;
            RETURN (ranking);
        END
    """

    cur.execute(query)

def display_rank(cnx, client_selection):
    cnx.reconnect()
    cur = cnx.cursor()
    print("\n~ Checkings Leaderboard ~")
    query = """
        SELECT c.idAccount, clt.name, balance_leaderboard(c.balance)
        FROM checking c, account acc, clients clt
        WHERE c.idAccount = acc.idAccount and acc.idClient = clt.idClient and clt.idClient = %s;
    """
    cur.execute(query, (client_selection,))
    results = cur.fetchall()
    table = PrettyTable(['Account ID', 'Name', 'Rank'])
    for balance in results:
        table.add_row(balance)
    print(table)

def credit_score(cnx):
    # credit score calculation
    cur = cnx.cursor()
    query = """
        DROP FUNCTION IF EXISTS credit_score;
        CREATE FUNCTION credit_score(balance INT, credit_limit INT)
        RETURNS VARCHAR(64)
        DETERMINISTIC
        BEGIN
            DECLARE rating VARCHAR(64);
            IF (balance/credit_limit <= 1 and balance/credit_limit > .6) THEN
                SET rating = 'Below Average';
            ELSEIF (balance/credit_limit <= .6 and balance/credit_limit > .3) THEN
                SET rating = 'Average';
            ELSEIF (balance/credit_limit <= .3 and balance/credit_limit > .1) THEN
                SET rating = 'Good';
            ELSEIF (balance/credit_limit <= .1) THEN
                SET rating = 'Excellent';
            END IF;
            RETURN (rating);
        END
    """
    cur.execute(query)

def display_credit_score(cnx, client_selection):
    cnx.reconnect()
    cur = cnx.cursor()
    print("\n~ Credit Score Ratings ~")
    query = """
        SELECT cc.idAccount, clt.name, credit_score(cc.balance, cc.credit_limit)
        FROM credit_card cc, account acc, clients clt
        WHERE cc.idAccount = acc.idAccount and acc.idClient = clt.idClient and clt.idClient = %s;
    """
    cur.execute(query, (client_selection,))
    results = cur.fetchall()
    table = PrettyTable(['Account ID', 'Name', 'Rating'])
    for balance in results:
        table.add_row(balance)
    print(table)


# --- 2 Trigger DDL --- #

def c_transaction(cnx):
    # creates and activates TRIGGER ddl -- transaction history
    cur = cnx.cursor()
    query_2 = "DROP TRIGGER IF EXISTS after_checking_transaction;"
    cur.execute(query_2)
    query = (
    """CREATE TRIGGER after_checking_transaction
        AFTER UPDATE ON checking FOR EACH ROW BEGIN
        IF OLD.balance <> new.balance THEN
            INSERT INTO checking_records(idAccount, before_balance, after_balance)
            VALUES(old.idAccount, old.balance, new.balance);
        END IF;
    END;""")
    cur.execute(query)

def c_records(cnx, account_selection):
    # displays checking transaction table of TRIGGER -- WHERE idAccount = {};".format(account_selection)
    cur = cnx.cursor()
    query = "SELECT cr.id, cr.idAccount, c.name, cr.before_balance, cr.after_balance FROM checking_records cr, account acc, clients c\
    WHERE cr.idAccount = acc.idAccount and acc.idClient = c.idClient and cr.idAccount = {};".format(account_selection)
    cur.execute(query)
    results = cur.fetchall()
    table = PrettyTable(['ID', 'Account ID', 'Name', 'Before Balance', 'After Balance'])
    for id, idAccount, name, before_balance, after_balance in results:
        table.add_row([id, idAccount, name, before_balance, after_balance])
    print(table)

def client_changes(cnx):
    # TRIGGER DDL - When there is an update with the client's information, insert the change into updated_client_records.
    cur = cnx.cursor()
    query = "DROP TRIGGER IF EXISTS client_records;"
    cur.execute(query)
    query = """
            CREATE TRIGGER client_records
            AFTER UPDATE
            ON clients FOR EACH ROW
            BEGIN
                IF old.name <> new.name OR old.address <> new.address OR old.phone <> new.phone OR old.idBranch <> new.idBranch THEN
                    INSERT INTO updated_client_records (idClient, name, address, phone, idBranch)
                    VALUES (old.idClient, new.name, new.address, new.phone, new.idBranch);
                END IF;
            END;
            """
    cur.execute(query)

def display_updated_clients(cnx):
    cur = cnx.cursor()
    print("\n~ Client Revision Records ~\n")
    query = "SELECT * FROM updated_client_records;"
    cur.execute(query)
    results = cur.fetchall()
    print(results)
