responses = {
    'status': 'success',
    'code' : 200
}

responses_1 = {
    'status': 'error',
    'code': 500
}


def check_status(response):
    if response['status'] == 'success':
        print('PASS')
    else:
        print('FAIL')



def check_status_code(response):
    if response['code'] == 200:
        print('PASS')
    else:
        print('FAIL')

check_status(responses_1)
check_status_code(responses_1)
