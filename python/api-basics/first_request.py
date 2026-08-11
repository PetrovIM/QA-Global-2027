import requests

#url = 'https://jsonplaceholder.typicode.com/users/1'
#url = "https://jsonplaceholder.typicode.com/users/9999"
url = "https://jsonplaceholder.typicode.com/users"


res = requests.get(url)
response_data = res.json()

def check_status_code_200(response):
    if response.status_code == 200:
        print('PASS')
    else:
        print('FAIL')

def check_name(data):
    if data.get("name") is None:
        print('FAIL')
    else:
        print('PASS')

def check_email(data):
    if data.get("email") != "" and data.get("email") is not None:
        print('PASS')
    else:
        print('FAIL')


def check_status_code_404(response):
    if response.status_code == 404:
        print('PASS')
    else:
        print('FAIL')


def check_userId(data):
    if data.get("id") == 9999:
        print('FAIL')
    else:
        print('PASS')


def check_users(data):
    count = len(data)
    if count == 10:
        print('PASS')
    else:
        print('FAIL')

def check_user_data(data):
     for item in data:
        if item.get("id") is not None and item.get("email") is not None and item.get("name") is not None:
            isExist = "PASS"
        else:
            isExist = "FAIL"
            break
     print(isExist)


print(response_data)