import requests


"""
Message to Line
Error message format :
Time: 2020-11-29 15:00:00
Error Type : ValueError and 
Location: 22.625266504508858, 120.29873388752162
Other Info: {Show other info}
"""

def message2line(message):
    # read token from line_token.txt
    line_notify_token = open('line_token.txt', 'r').read()
    line_notify_api = 'https://notify-api.line.me/api/notify'
    payload = {'message': message}
    headers = {'Authorization': 'Bearer ' + line_notify_token}
    line_notify = requests.post(line_notify_api, data=payload, headers=headers)
    return line_notify.status_code

if __name__ == '__main__':
    message2line('test')