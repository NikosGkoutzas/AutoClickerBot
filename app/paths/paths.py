import os


'''
Path to the Google Chrome executable
'''
chrome_path = '/usr/bin/google-chrome'


'''
Remote debugging port used by Chrome and Selenium
'''
port = 9222


'''
Directory used by Chrome to store the Selenium user profile
NOTE: The directory must exist before running the application.
Example:
    mkdir -p /home/nick/selenium-profile
'''
user_data_dir = os.path.join(f'{os.getcwd()}/app/' , 'selenium-profile')