import time
import storage.database as database
from data.parser import ApiParser

def main():
    while True:
        database.OpenConnection()
        employees = updateEmployees()
        if (len(employees) > 0):
            updateMails(employees)
        
        database.CloseConnection()

        time.sleep(60)

def updateEmployees() -> list:
    employeesResponse = ApiParser.GetEmployeesInOrganization()
        
    if employeesResponse.ok:
        r = employeesResponse.json()

        employees = r['users']
        for e in employees:
            database.AddEmployee(e['id'], e['email'])

        return employees
    
    else:
        print(employeesResponse.json())
        return list()

def updateMails(employees: list) -> None:
    for e in employees:
        mailsResponse = ApiParser.GetMailsByEmployeeId(e['id'])

        if mailsResponse.ok:
            r = mailsResponse.json()

            e['resources'] = r['resources']
            mails = r['resources']
            for m in mails:
                database.AddMail(m['resourceId'])
                database.AddEmployeeToMail(e['id'], m['resourceId'])
    

if __name__ == "__main__":
    main()