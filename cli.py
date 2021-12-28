import requests
import json
import sys
import os
import argparse

BASE_URL = 'https://safe-courier-backend-api.herokuapp.com/api/v1'

class API:
    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, url, headers):
        return requests.get(self.base_url + url, headers=headers)

    def post(self, url, data, headers):
        return requests.post(self.base_url + url, data, headers=headers )

    def put(self, url, data, headers):
        return requests.put(self.base_url + url, data, headers=headers)

    def delete(self, url, headers):
        return requests.delete(self.base_url + url, headers=headers)

class Authentication:
    def __init__(self, api):
        self.api = api
        self.token = None

    def login(self, username, password):
        data = {
            'username': username,
            'password': password
        }
        
        # convert data to json
        data = json.dumps(data)
        # add headers
        headers = {
            'Content-Type': 'application/json'
        }
        # make request
        response = self.api.post('/auth/login', data, headers)
        # check if request was successful
        if response.status_code == 200:
            # get token
            self.token = response.json()['token']
            # save token to user's home directory
            with open(os.path.expanduser('~/.safe_courier_token'), 'w') as f:
                f.write(self.token)
            return True
        else:
            print(response.json()['message'])
            return False

    def logout(self):
        # remove token from user's home directory
        os.remove(os.path.expanduser('~/.safe_courier_token'))
        # remove token from Authentication class
        self.token = None

    def get_token(self):
        # check if token exists
        if self.token:
            return self.token
        # check if token exists in user's home directory
        try:
            with open(os.path.expanduser('~/.safe_courier_token'), 'r') as f:
                self.token = f.read()
        except:
            pass
        return self.token

    def signup(self, data):
        # convert data to json
        data = json.dumps(data)
        # add headers
        headers = {
            'Content-Type': 'application/json'
        }
        # make request
        response = self.api.post('/auth/signup', data, headers)
        # check if request was successful
        if response.status_code == 200:
            return True
        else:
            print(response.json()['message'])
            return False

class CLI:
    def __init__(self, api, auth):
        self.api = api
        self.auth = auth

    def get_token(self):
        return self.auth.get_token()

    def login(self, username, password):
        return self.auth.login(username, password)

    def logout(self):
        return self.auth.logout()

    def signup(self, data):
        return self.auth.signup(data)

    def get_user(self):
        # get token
        token = self.get_token()
        # add headers
        headers = {
            'Authorization': 'Bearer ' + token
        }
        # make request
        response = self.api.get('/users/me', headers)
        # check if request was successful
        if response.status_code == 200:
            return response.json()
        else:
            print(response.json()['message'])
            return False

    def get_users(self):
        # get token
        token = self.get_token()
        # add headers
        headers = {
            'Authorization': 'Bearer ' + token
        }
        # make request
        response = self.api.get('/users', headers)
        # check if request was successful
        if response.status_code == 200:
            return response.json()
        else:
            print(response.json()['message'])
            return False

    def get_user_by_id(self, id):
        # get token
        token = self.get_token()
        # add headers
        headers = {
            'Authorization': 'Bearer ' + token
        }
        # make request
        response = self.api.get('/users/' + str(id), headers)
        # check if request was successful
        if response.status_code == 200:
            return response.json()
        else:
            print(response.json()['message'])
            return False

    def get_user_by_username(self, username):
        # get token
        token = self.get_token()
        # add headers
        headers = {
            'Authorization': 'Bearer ' + token
        }
        # make request
        response = self.api.get('/users/username/' + username, headers)
        # check if request was successful
        if response.status_code == 200:
            return response.json()
        else:
            print(response.json()['message'])
            return False

class Parcel:
    def __init__(self, api, auth):
        self.api = api
        self.auth = auth

    def get_parcels(self):
        # get token
        token = self.auth.get_token()
        # add headers
        headers = {
            'Authorization': 'Bearer ' + token
        }
        # make request
        response = self.api.get('/parcels', headers)
        # check if request was successful
        if response.status_code == 200:
            return response.json()
        else:
            print(response.json()['message'])
            return False


def main():
    # create API object
    api = API(BASE_URL)
    # create Authentication object
    auth = Authentication(api)
    # create CLI object
    cli = CLI(api, auth)

    # create Parcel object
    parcel = Parcel(api, auth)

    # create parser
    parser = argparse.ArgumentParser()
    # add arguments
    parser.add_argument('-l', '--login', nargs=2, help='login to Safe Courier')
    parser.add_argument('-s', '--signup', nargs=5, help='signup to Safe Courier')
    parser.add_argument('-g', '--get-user', help='get user info')
    parser.add_argument('-u', '--get-users', help='get all users')
    parser.add_argument('-i', '--get-user-by-id', nargs=1, help='get user by id')
    parser.add_argument('-n', '--get-user-by-username', nargs=1, help='get user by username')
    parser.add_argument('-p', '--get-parcels', help='get all parcels')
    parser.add_argument('-o', '--logout', help='logout')
    # parse arguments
    args = parser.parse_args()
    # check if login argument was passed
    if args.login:
        print(args.login)
        # check if login was successful
        if cli.login(args.login[0], args.login[1]):
            print('Login successful')
        else:
            print('Login failed')
    # check if signup argument was passed
    elif args.signup:
        # create data
        data = {
            'username': args.signup[0],
            'email': args.signup[1],
            'password': args.signup[2],
            'firstName': args.signup[3],
            'lastName': args.signup[4]
        }
        # check if signup was successful
        if cli.signup(data):
            print('Signup successful')
        else:
            print('Signup failed')
    # check if get user argument was passed
    elif args.get_user:
        # get user info
        user = cli.get_user()
        # print user info
        print('Welcome ' + user['username'] + '!')
        print('Your id is ' + str(user['id']))
        print('Your email is ' + user['email'])
        print('Your role is ' + user['role'])
        print('Your created at is ' + user['created_at'])
        print('Your updated at is ' + user['updated_at'])
    # check if get users argument was passed
    elif args.get_users:
        # check for token
        if not cli.get_token():
            print('You must be logged in to get users')
            return
        # get users
        users = cli.get_users()
        # print users
        for user in users:
            print('User id: ' + str(user['_id']))
            print('User username: ' + user['username'])
            print('User email: ' + user['email'])
            print('User Admin role: ' + str(user['isAdmin']))
            print('\n')
    # check if get user by id argument was passed
    elif args.get_user_by_id:
        # get user by id
        user = cli.get_user_by_id(args.get_user_by_id[0])
        # print user info
        print('User id is ' + str(user['id']))
        print('User username is ' + user['username'])
        print('User email is ' + user['email'])
        print('User role is ' + user['role'])
        print('User created at is ' + user['created_at'])
        print('User updated at is ' + user['updated_at'])
    # check if get user by username argument was passed
    elif args.get_user_by_username:
        # get user by username
        user = cli.get_user_by_username(args.get_user_by_username[0])
        # print user info
        print('User id is ' + str(user['id']))
        print('User username is ' + user['username'])
        print('User email is ' + user['email'])
        print('User role is ' + user['role'])
        print('User created at is ' + user['created_at'])
        print('User updated at is ' + user['updated_at'])
    # check if logout argument was passed
    elif args.logout:
        # logout
        cli.logout()
        print('Logout successful')
    # check if get parcels argument was passed
    elif args.get_parcels:
        parcels = parcel.get_parcels()
        for parcel in parcels:
            print(parcel)
    # check if no arguments were passed
    else:
        # print help
        parser.print_help()


if __name__ == '__main__':
    main()

