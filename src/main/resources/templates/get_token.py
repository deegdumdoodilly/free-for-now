import requests

API_ENDPOINT = 'https://discord.com/api/v10'
CLIENT_ID = '1121095357590413412'
CLIENT_SECRET = 'EIqSOMmqjFz52yQ1PPCRyveWcRIEEDMB'
REDIRECT_URI = 'http://pfvsrd.com/'

def exchange_code(code):
  data = {
    'client_id': '1121095357590413412',
    'client_secret': 'EIqSOMmqjFz52yQ1PPCRyveWcRIEEDMB',
    'grant_type': 'authorization_code',
    'code': '6QEgi9rFj4U5kNG01Mqolv6mzoJJLH',
    'redirect_uri': 'http://pfvsrd.com/'
  }
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
  }
  r = requests.post('%s/oauth2/token' % API_ENDPOINT, data=data, headers=headers)
  r.raise_for_status()
  return r.json()

if __name__ == "__main__":
  print(exchange_code("6QEgi9rFj4U5kNG01Mqolv6mzoJJLH"))