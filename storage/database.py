import psycopg2
from config import dbOptions

conn = None

def OpenConnection() -> None:
    try:
        global conn
        conn = psycopg2.connect(
            host = dbOptions.host,
            user = dbOptions.user,
            password = dbOptions.password,
            database = dbOptions.db_name,
            port = dbOptions.port
        )
        conn.autocommit = True
        return
    
    except Exception as _ex:
        print("[INF] Error on opening connection: ", _ex)

def CloseConnection() -> None:
    conn.close()

def CreateTables() -> bool:
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                create table if not exists employees (
                    id text primary key,
                    email text
                );

                create table if not exists mails (
                    id text primary key
                );

                create table if not exists employees_mails (
                    employee_id text references employees(id),
                    mail_id text references mails(id)
                );
                """
            )
        return True

    except Exception as _ex:
        print("[ERR] Error while working with database", _ex)

    return False

def AddEmployee(employee_id: str, employee_email: str) -> bool:
    try: 
        with conn.cursor() as cursor:
            cursor.execute(f"select count(*) from employees as u where u.id = '{employee_id}';")
            n: int = cursor.fetchone()

            if (n > 0): 
                return False
            
            else:
                cursor.execute(f"insert into employees values ('{employee_id}', '{employee_email}');")
                return True
    
    except Exception as _ex:
        print("[ERR] Error while working with database", _ex)

    return False

def AddMail(mail_id: str) -> bool:
    try: 
        with conn.cursor() as cursor:
            cursor.execute(f"select count(*) from mails as m where m.id = '{mail_id}';")
            n: int = cursor.fetchone()

            if (n[0] > 0): 
                return False
            
            else:
                cursor.execute(f"insert into mails values ('{mail_id}');")
                return True
    
    except Exception as _ex:
        print("[ERR] Error while working with database", _ex)

    return False

def AddMailToEmployee(mail_id: str, employee_id: str) -> bool: 
    try: 
        with conn.cursor() as cursor:
            cursor.execute(
                f"""
                select count(*) 
                from employees_mails as um 
                where um.employee_id = '{employee_id}' and um.mail_id = '{mail_id}';
                """
            )
            n: int = cursor.fetchone()

            if (n > 0): 
                return False
            
            else:
                cursor.execute(f"insert into employees_mails values ('{employee_id}', '{mail_id}');")
                return True
    
    except Exception as _ex:
        print("[ERR] Error while working with database", _ex)

    return False

def AddEmployeeToMail(employee_id: str, mail_id: str) -> bool: 
    return AddMailToEmployee(mail_id, employee_id)

def GetEmployees() -> list:
    try: 
        with conn.cursor() as cursor:
            cursor.execute(f"select * from employees;")
            data = cursor.fetchall()
            return data
        
    except Exception as _ex:
        print("[ERR] Error while working with database", _ex)

def GetMails() -> list:
    try: 
        with conn.cursor() as cursor:
            cursor.execute(f"select * from mails;")
            data = cursor.fetchall()
            return data
        
    except Exception as _ex:
        print("[ERR] Error while working with database", _ex)