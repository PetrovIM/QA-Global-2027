def check_status_code(actual, expected):
    if actual == expected:
        print(f'PASS: expected={expected}, actual={actual}')
    else:
        print(f'FAIL: expected={expected}, actual={actual}')


check_status_code(200, 200)
check_status_code(201, 200)
check_status_code(500, 200)
