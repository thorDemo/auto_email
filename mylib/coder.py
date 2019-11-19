import base64


def encode_header(string, email):
    s = string.encode('utf-8')
    return f'=?UTF-8?B?{base64.b64encode(s)}?= {email}'
