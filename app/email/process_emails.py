from .process_emails_interface import ProcessEmailsInterface
from ..files.read_files_interface import ReadFilesInterface
from ..files.write_files_interface import WriteFilesInterface
from ..driver.driver_interface import DriverInterface
from dotenv import load_dotenv
import inject , os , shutil , sys



class ProcessEmails(ProcessEmailsInterface):
    @inject.autoparams()
    def __init__(self ,
                 read_files_interface: ReadFilesInterface ,
                 write_files_interface: WriteFilesInterface ,
                 driver_interface: DriverInterface):
        
        self.read_files = read_files_interface
        self.write_files = write_files_interface
        self.driver = driver_interface


    def process_add_link_email(self , list_added_links: list[str]) -> tuple[list[str] , list[str]]:
        '''
        Processes a list of links received via email and categorizes them
        into valid and invalid links.

        A link is considered invalid if: - it already exists in the stored URLs, or
                                         - it does not start with the expected car.gr base URL.
                                         
        Valid links are stored and returned separately.

        :Parameters: list_added_links (list[str]): A list of links extracted from the email.
        :Returns: tuple[list[str], list[str]]: - A list of valid links that were successfully stored.
                                               - A list of invalid links that were rejected.
        '''
        invalid_links = []
        valid_links = []

        for link in list_added_links:
            if(link in self.read_files.read_every_url() or (not link.startswith('https://www.car.gr/xyma/view/'))):
                invalid_links.append(link)
            
            else:
                self.write_files.add_machine(link)
                valid_links.append(link)
        
        return valid_links , invalid_links
                
                
                
                

    
    def process_remove_link_email(self , list_removed_links: list[str]) -> tuple[list[str] , list[str]]:
        '''
        Processes a list of links received via email and categorizes them
        into removable (valid) and invalid links.

        A link is considered invalid if: - it does not exist in the stored URLs, or
                                         - it does not start with the expected car.gr base URL.
                                         
        Valid links are removed from storage and returned separately.

        :Parameters: list_removed_links (list[str]): A list of links extracted from the email that
                                                     are requested to be removed.
        :Returns: tuple[list[str], list[str]]: - A list of successfully removed links.
                                               - A list of invalid links that could not be removed.
        '''
        invalid_links = []
        valid_links = []

        for link in list_removed_links:
            if(link not in self.read_files.read_every_url() or (
                not link.startswith('https://www.car.gr/xyma/view/'))):
                    invalid_links.append(link)
            
            else:
                self.write_files.remove_machine(link)
                valid_links.append(link)
        
        return valid_links , invalid_links
    
    
    
    
    
    def process_change_credentials_email(self , list_changed_credentials: list[str]) -> str:
        '''
        Processes a request received via email to update login credentials
        (username and/or password).

        The request must contain either one or two credential entries, formatted as:
            - "username:<new_username>"
            - "password:<new_password>"

        Validation rules: - Only one username and one password may be provided.
                          - The new username or password must differ from the existing values.
                          - At least one valid credential update must be included.
                          - Requests with invalid structure or duplicate fields are rejected.

        If the validation succeeds, the credentials are updated in the environment
        configuration file.

        :Parameters: list_changed_credentials (list[str]): A list of credential update strings
                                                           extracted from the email.
        :Returns: str: - 'Ok' if the credentials were successfully updated.
                       - An explanatory error message if the request is invalid
                         or cannot be applied.
        '''
        try:
            if(not (len(list_changed_credentials) == 1 or len(list_changed_credentials) == 2) ):
                return 'Please ensure your request includes one or two credential updates: username or password.'    
                
            load_dotenv(override=True)
            old_username = os.getenv('site_username')
            old_password = os.getenv('site_password')
            new_username = None
            new_password = None
            
            for cred in list_changed_credentials:
                name , value = cred.split(':' , 1)
                name = name.strip().lower()
                value = value.strip()
                
                if(name == 'username'):
                    if(old_username == value):
                        return 'The new username matches the existing username and cannot be applied.'
                    
                    if(new_username is not None):
                        return 'The username was provided more than once in the request.'
                        
                    else:
                        new_username = value               
                    
                if(name == 'password'):
                    if(old_password == value):
                        return 'The new password matches the existing username and cannot be applied.'
                    
                    if(new_password is not None):
                        return 'The password was provided more than once in the request.'
                        
                    else:
                        new_password = value 
                                
            if(new_username is None and new_password is None): 
                return 'Your request does not include a username or password update.'
                
            
            # change credentials in .env file
            self.write_files.update_credentials_from_env(new_username if new_username is not None else None ,
                                                        new_password if new_password is not None else None)
            return 'Ok'
        
        except Exception as e:
            print(f'An error occured: {str(e)}')
            self.write_files.write_total_errors()
        
        return 'fail'
    
    
    
    
    def process_new_version_email(self , list_semantic_versioning: list[str]) -> tuple[bool , str]:
        '''
        Processes a request received via email to determine the type of
        semantic version increment to apply.

        The function expects a list containing a single value indicating
        the desired version change. Supported values are: - "major"
                                                          - "minor"
                                                          - "patch"

        The comparison is case-insensitive and ignores leading/trailing whitespace.

        :Parameters: list_semantic_versioning (list[str]): A list of versioning instructions
                                                           extracted from the email.
        :Returns: tuple[bool, str]: - True and the normalized version type ("major", "minor", or "patch")
                                      if the request is valid.
                                    - False and None if the request is invalid or unsupported.
        '''
        if(list_semantic_versioning and list_semantic_versioning[0].strip().lower() in ['major' , 'minor' , 'patch']):
            return True , list_semantic_versioning[0].strip().lower()
        
        return False , None
    
    
    
    
    def process_download_new_version_from_github(self , semantic_input: str) -> bool:
        '''
        Downloads and installs a new version of the application from GitHub.

        The function clones the latest version of the repository into a temporary
        directory, replaces the existing application files while preserving
        critical configuration and data directories, updates the application
        version, and restarts the application.

        Certain files and folders (such as environment files and stored data)
        are excluded from deletion to ensure continuity.

        :Parameters: semantic_input (str): The semantic version update type
                                           applied (e.g. "major", "minor", "patch").
        :Returns: bool: - True if the new version was successfully downloaded, installed,
                          and the application was restarted.
                        - False if an error occurred during the update process.
        '''
        try:
            tmp_folder_dir = os.path.join(os.getcwd() , 'NewVersionTmpFolder')
            
            if(os.path.isdir(tmp_folder_dir)):
                shutil.rmtree(tmp_folder_dir)
           
            os.makedirs(tmp_folder_dir)
            os.chdir('NewVersionTmpFolder/')
            os.system('git clone https://github.com/NikosGkoutzas/AutoClickerBot.git')
                
            source_dir = f'{os.getcwd()}/AutoClickerBot/app'
            
            home_folder_path = os.path.expanduser("~")
            load_dotenv(override=True)
            autoClickerBot_folder_path = f'{home_folder_path}/{os.getenv('folder_path_to_app')}/AutoClickerBot'
            
            app_destination_dir = os.path.join(autoClickerBot_folder_path , 'app')
            files_destination_path = os.path.join(app_destination_dir , 'files')

            excluded_files_and_folders_list = ['__init__.py' , 'selenium-profile' , '.env_example' ,
                                               '.env' , '__pycache__' , 'requirements.txt']
            
            os.chdir('AutoClickerBot/app/')
            for item in os.listdir(app_destination_dir):
                if(item not in excluded_files_and_folders_list):
                    deleted_file_folder_dir = os.path.join(app_destination_dir , item)  

                    if(item == 'files'):
                        os.chdir('files/')
                        files_path = os.getcwd()

                        for inner_item in os.listdir(files_path):
                            if(os.path.isfile(inner_item)):
                                os.remove(inner_item)
                                
                            else:
                                if(os.path.isdir(inner_item) and inner_item != 'all_files'):
                                    shutil.rmtree(inner_item)
                                    
                        os.chdir('..')
                        
                    else:
                        if(os.path.isfile(deleted_file_folder_dir)):
                            os.remove(deleted_file_folder_dir) 
                        
                        elif(os.path.isdir(deleted_file_folder_dir)):
                            shutil.rmtree(deleted_file_folder_dir)
                    
                         
            for item in os.listdir(source_dir):
                if(item not in excluded_files_and_folders_list):
                    if(item == 'files'):
                        os.chdir('files/')
                        files_path = os.getcwd()

                        for inner_item in os.listdir(files_path):
                            if(os.path.isdir(inner_item) and inner_item == 'all_files'):
                                shutil.rmtree(inner_item)
                        
                        for inner_item in os.listdir(files_path):
                            shutil.move(os.path.join(os.getcwd() , inner_item) , files_destination_path)
                            
                        os.chdir('..')
                    
                    else:
                        shutil.move(os.path.join(source_dir , item) , app_destination_dir)

            os.chdir(autoClickerBot_folder_path)
            self.write_files.write_app_version(semantic_input)
            self.write_files.write_new_version_update_flag(1)
            self.driver.quit_driver()
            print('The new version has been downloaded, installed and files have been replaced successfully.')
            os.execv(sys.executable , [sys.executable, "-m", "app.main"])
        
        except Exception as e:
            print(f'An error occured while trying to install the latest version from github: {str(e)}')
            return False