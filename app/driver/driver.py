from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from ..paths.paths import port
from .driver_interface import DriverInterface
from ..files.write_files_interface import WriteFilesInterface
from ..files.read_files_interface import ReadFilesInterface
from dotenv import load_dotenv
import os , time , pyautogui , inject



class Driver(DriverInterface):
    @inject.autoparams()
    def __init__(self ,
                 write_files_interface: WriteFilesInterface ,
                 read_files_interface: ReadFilesInterface
                 ):
        
        self.write_files = write_files_interface
        self.read_files = read_files_interface
        self.driver = None
    
                
    
    def start_driver(self):
        '''
        Initializes and starts the Chrome WebDriver instance.

        :Parameters: None
        :Returns: None
        '''
        
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        service = Service("/usr/local/bin/chromedriver")
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
    
    
    
    def quit_driver(self):
        '''
        Closes the Chrome WebDriver and terminates the debugging Chrome process.

        :Parameters: None
        :Returns: None
        '''
        
        self.driver.quit()
        os.system(f"pkill -f 'remote-debugging-port={port}'")
    
    


    def login(self) -> int:
        '''
        Attempts to log in to the www.car.gr, handles CAPTCHA challenge and credential errors.

        :Parameters: None
        :Returns: int: 0 if the CAPTCHA challenge was solved after one or more attempts,
                       1 if no CAPTCHA was active and login succeeded,
                       2 if the CAPTCHA challenge failed to solve,
                       3 if login failed due to wrong credentials after 3 attempts.
        '''
        
        total_attempts = 3
        
        self.decline_cookies()
        self.is_captcha_active_before_login_credentials()
            
        for _ in range(total_attempts):
            if(self.is_logged_in()):
                return 1
            
            try:
                load_dotenv(override=True)
                site_username = os.getenv('site_username')
                site_password = os.getenv('site_password')
                username_input = self.find_input("#input-username")
                username_input.click()
                username_input.clear()
                username_input.send_keys(site_username)
                password_input = self.find_input("#current-password")
                password_input.click()
                password_input.clear()
                password_input.send_keys(site_password)
                log_in_button = self.find_button(By.CSS_SELECTOR , ".submit-btn")
                log_in_button.click()
                
                
                result = self.is_captcha_active_after_login_credentials()
                if(result != 3):    # wrong credentials, try again
                    return result
                    
            except Exception as e:
                print(f'An error occured trying to logging in: {str(e)}')
                self.write_files.write_total_errors()
               
                
        return 3    # wrong credentials




    def logout(self) -> None:
        '''
        Logs the user out of the application if currently logged in.

        :Parameters: None
        :Returns: None
        '''
        
        if(not self.is_logged_in()):
            return

        try:
            WebDriverWait(self.driver , 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR ,"a[href='/account']"))).click()
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/logout/']"))).click()
        
        except Exception as e:
            print(f'An error occured trying to logging out: {str(e)}')
            self.write_files.write_total_errors()
    

    
    
    def wrong_credentials_in_login(self) -> bool:
        '''
        Checks whether a wrong credentials message is displayed during login.

        :Parameters: None
        :Returns: True if the wrong username or password message is visible,
                  otherwise False.
        '''
        
        try:
            WebDriverWait(self.driver , 10).until(EC.visibility_of_element_located((By.XPATH ,
            "//div[contains(. , 'Λάθος όνομα χρήστη ή κωδικός')]"
            )))

            return True
            
        except TimeoutException:
            self.write_files.write_total_errors()
            return False

        
    
    
    
    
    def decline_cookies(self) -> bool:
        '''
        Declines the cookies popup window, if it's displayed.

        :Parameters: None
        :Returns: True if the cookies popup was found and declined,
                  otherwise False.
        '''
        
        self.open_url('https://www.car.gr/login/')
        
        if not self.has_cookies_popup():
            return False

        try:
            button = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.ID , "disagree-btn")))
            button.click()
            return True
        
        except TimeoutException:
            self.write_files.write_total_errors()
            return False







    def update_machine(self , url_link: str) -> int:
        '''
        Opens the given machine URL and performs the update process.

        :Parameters: url_link (int): The URL of the machine to be updated.
        :Returns: bool: 1 if the update process completed successfully,
                        -1 if CAPTCHA chalenge failed to solve,
                        otherwise 0.
        '''
        
        try:
            self.open_url(url_link)
            return self.update()

        except Exception as e:
            print(f'An error occured updating a machine: {str(e)}')
            self.write_files.write_total_errors()
    
    



    def open_url(self , url: str) -> None:
        '''
        Opens the specified URL in the browser.

        :Parameters: url (str): The URL to be opened.
        :Returns: None
        '''
        
        try:
            self.driver.get(url)

        except Exception as e:
            print(f'An error occured opening url: {str(e)}')
            self.write_files.write_total_errors()
        






    def update(self) -> int:
        '''
        Checks whether the update button is available and ready to be clicked.

        :Parameters: None
        :Returns: bool: 1 if the update button displays 'Ανανέωση',
                        -1 if CAPTCHA challenge fails,
                        0 if the update button do not display 'Ανανέωση'
                        or an excpetion occurs.
        '''
        
        try:
            if(self.is_captcha_active_before_login_credentials() == 2):
                return -1
            
            xpath = ".//span[contains(@class,'tw-max-w-full') and (normalize-space(text())='Ανανέωση' or normalize-space(text())='Ανανεώθηκε')]"
            state_span = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
            button = state_span.find_element(By.XPATH, "./ancestor::button")

            if(state_span.text.strip() == 'Ανανέωση'):
                self.driver.execute_script("arguments[0].click();", button)
                
            return state_span.text.strip() == 'Ανανέωση'

        except TimeoutException as e:
            print(f'No update button found: {str(e)}')
            self.write_files.write_total_errors()
            return 0

        except Exception as e:
            print(f"An error occured while trying to update: {str(e)}")
            self.write_files.write_total_errors()
            return 0

            





    def find_input(self, selector: str) -> WebElement:
        '''
        Finds and returns an input field (username/password)
        using a CSS selector, waiting until it becomes clickable.

        :Parameters: selector (str): The CSS selector of the input field.
        :Returns: WebElement: The input element so it can be interacted with
                              (click, clear, send_keys).
        '''
        
        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR , selector)))




    def find_button(self , by: By , value: str) -> WebElement:
        '''
        Finds and returns a clickable button element using a Selenium locator.

        :Parameters: by (By): Selenium locator strategy (e.g. By.ID, By.XPATH, By.CSS_SELECTOR).
                     value (str): The locator value used to identify the button.
        :Returns: WebElement: The clickable button element so it can be clicked or inspected.
        '''
        
        return WebDriverWait(self.driver , 10).until(EC.element_to_be_clickable((by , value)))
    
    
    

    def find_element(self , button_string: str) -> WebElement:
        '''
        Finds and returns a clickable element using a CSS selector.

        :Parameters: button_string (str): The CSS selector of the element.
        :Returns: WebElement: The clickable web element that was found.
        '''
        
        return WebDriverWait(self.driver , 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR , button_string)))



            
    def has_cookies_popup(self) -> bool:
        '''
        Checks whether the cookies popup window is present on the page.

        :Parameters: None
        :Returns: bool: True, if the cookies popup is detected, False otherwise.
        '''
        
        try:
            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, "//button[@id='disagree-btn']")))
            return True
        
        except TimeoutException:
            self.write_files.write_total_errors()
            return False

        




    def is_logged_in(self) -> None:
        '''
        Checks whether the user is currently logged in.
        Logged-in users have an avatar image inside the account link.

        :Parameters: None
        :Returns: bool: True if the user is logged in, False otherwise.
        '''
    
        elements = self.driver.find_elements(By.CSS_SELECTOR , 'a[href="/account"] img')
        
        return len(elements) > 0
    
    
    
    

    def captcha_challenge_after_login_credentials(self) -> bool:
        '''
        Checks whether a captcha challenge appears after submitting login credentials.
        If the login submit button is no longer clickable within the timeout,
        it is assumed that a captcha or challenge has been triggered.

        :Parameters: None
        :Returns: bool: True, if a captcha challenge is detected, False otherwise.
        '''
        
        try:
            WebDriverWait(self.driver , 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR , ".submit-btn")))
            return False
        
        except TimeoutException:
            self.write_files.write_total_errors()
            return True




    def is_captcha_active_before_login_credentials(self) -> int:
        '''
        Checks whether a captcha challenge is active before entering login
        credentials and attempts to solve it automatically if detected.

        :Parameters: None
        :Returns: int: 0: Captcha challenge detected and solved successfully.
                       1: No captcha challenge detected.
                       2: Captcha challenge detected but failed to solve after all attempts.
        '''
        
        if("needs to review the security" in self.driver.page_source.lower()):
            self.write_files.write_number_of_captcha_challenge()
            width , height = pyautogui.size()
            
            # Coordinates for my laptop (Dell). These may vary for other laptops.
            # x = -395
            # y = -45
            
            # Coordinates for other laptop.
            x = -100
            y = 15
            
            pyautogui.FAILSAFE = False
            pyautogui.moveTo(width / 2 + x , height / 2 + y , duration=1)
            
            captcha_attempts = 10
            for _ in range(captcha_attempts):
                if("needs to review the security" in self.driver.page_source.lower()):
                    pyautogui.click()
                    time.sleep(7)
               
                else:
                    return 0
            
            if("needs to review the security" in self.driver.page_source.lower()):
                return 2
        
        else:
            return 1





    def is_captcha_active_after_login_credentials(self) -> int:
        '''
        Checks whether a captcha challenge appears after submitting login
        credentials and attempts to solve it automatically if detected.
            
        :Parameters: None
        :Returns: int: 0: Captcha challenge detected and solved successfully.
                       1: No captcha challenge detected.
                       2: Captcha challenge detected but failed to solve.
                       3: Login failed due to wrong credentials.
        '''
        
        if(self.captcha_challenge_after_login_credentials()):
            self.write_files.write_number_of_captcha_challenge()
            width , height = pyautogui.size()
            
            # Coordinates for my laptop (Dell). These may vary for other laptops.
            # x = -100
            # y = 110
            
            # Coordinates for other laptop.
            x = -100
            y = 15

            # Sleep untill CAPTCHA challenge pops up
            while(1):
                if('challenge' in self.driver.page_source.lower()):
                    break
                
                time.sleep(0.2)
                
            pyautogui.FAILSAFE = False
            pyautogui.moveTo(width / 2 + x , height / 2 + y , duration=1)

            captcha_attempts = 10
            
            for _ in range(captcha_attempts):
                if(not self.is_logged_in()):
                    pyautogui.click()
                    time.sleep(7)
                    
                if(self.is_logged_in()):
                    return 0
                
                elif(self.wrong_credentials_in_login()):
                    return 3
            
            if(not self.is_logged_in()):
                return 2
        
        else:
            return 1