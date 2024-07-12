import requests
from config import ApiOptions

class ApiParser():
    def GetEmployeesInOrganization() -> requests.Response:
        return Get(f"/directory/v1/org/{ApiOptions.org_id}/users") 
    
    def GetMailsByEmployeeId(user_id: str) -> requests.Response:
        return Get(f"/admin/v1/org/{ApiOptions.org_id}/mail/delegated/{user_id}/resources")

def Get(path: str) -> requests.Response:
    hs = {"Authorization": "OAuth " + ApiOptions.auth_token}
    full_path = ApiOptions.host + path
    return requests.get(full_path, headers=hs)
    