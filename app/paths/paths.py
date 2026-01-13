import os

chrome_path = '/usr/bin/google-chrome'
port = 9222
# You must create the profile like this: 'mkdir -p /home/nick/selenium-profile'
user_data_dir = os.path.join(f'{os.getcwd()}/app/' , 'selenium-profile')