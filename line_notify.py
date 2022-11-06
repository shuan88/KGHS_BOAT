import requests


def line_notify(message):
    # read token from line_token.txt
    line_notify_token = open('line_token.txt', 'r').read()
    line_notify_api = 'https://notify-api.line.me/api/notify'
    payload = {'message': message}
    headers = {'Authorization': 'Bearer ' + line_notify_token}
    line_notify = requests.post(line_notify_api, data=payload, headers=headers)
    return line_notify.status_code


if __name__ == '__main__':
    line_notify('test')