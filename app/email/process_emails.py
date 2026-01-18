from .process_emails_interface import ProcessEmailsInterface
from ..files.read_files_interface import ReadFilesInterface
from ..files.write_files_interface import WriteFilesInterface
from ..driver.driver_interface import DriverInterface
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
        invalid_links = []
        valid_links = []

        for link in list_added_links:
            if(link in self.read_files.read_every_url() or (
                not link.startswith('https://www.car.gr/xyma/view/') or not link.endswith('electronord-gr'))):
                    invalid_links.append(link)
            
            else:
                self.write_files.add_machine(link)
                valid_links.append(link)
        
        return valid_links , invalid_links
                
                
                
                

    
    def process_remove_link_email(self , list_removed_links: list[str]) -> tuple[list[str] , list[str]]:
        invalid_links = []
        valid_links = []

        for link in list_removed_links:
            if(link not in self.read_files.read_every_url() or (
                not link.startswith('https://www.car.gr/xyma/view/') or not link.endswith('electronord-gr'))):
                    invalid_links.append(link)
            
            else:
                self.write_files.remove_machine(link)
                valid_links.append(link)
        
        return valid_links , invalid_links
    
    
    
    
    
    def process_change_credentials_email(self , list_changed_credentials: list[str]) -> str:        
        if(not (len(list_changed_credentials) == 1 or len(list_changed_credentials) == 2) ):
            return 'Please ensure your request includes one or two credential updates: username or password.'    
            
            
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
    
    
    
    
    
    def process_new_version_email(self , list_semantic_versioning: list[str]) -> tuple[bool , str]:
        
        if(list_semantic_versioning and list_semantic_versioning[0].strip().lower() in ['major' , 'minor' , 'patch']):
            return True , list_semantic_versioning[0].strip().lower()
        
        return False , None
    
    
    
    def download_new_version_from_github(self , semantic_input: str) -> bool:
        try:
            tmp_folder_dir = os.path.join(os.getcwd() , 'NewVersionTmpFolder')
            
            if(os.path.isdir(tmp_folder_dir)):
                shutil.rmtree(tmp_folder_dir)
           
            os.makedirs(tmp_folder_dir)
            os.chdir('NewVersionTmpFolder/')
            os.system('git clone https://github.com/NikosGkoutzas/AutoClickerBot.git')
                
            source_dir = f'{os.getcwd()}/AutoClickerBot/app'
            
            home_folder_path = os.path.expanduser("~")
            autoClickerBot_folder_path = None
            
            for root , dirs , _ in os.walk(home_folder_path):
                if('AutoClickerBot' in dirs):
                    autoClickerBot_folder_path = os.path.join(root , dirs)
            
            
            app_destination_dir = os.path.join(autoClickerBot_folder_path , 'app')
            files_destination_path = os.path.join(app_destination_dir , 'files')

            excluded_files_and_folders_list = ['__init__.py' , '.env' , 'selenium-profile' , '.env_example' , 
                                               '__pycache__' , 'requirements.txt']
            
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

            BASE_DIR = f'{os.path.expanduser("~")}/Music/AutoClickerBot/'

            os.chdir(BASE_DIR)
            self.write_files.write_app_version(semantic_input)
            self.write_files.write_new_version_update_flag(1)
            self.driver.quit_driver()
            print('The new version has been downloaded, installed and files have been replaced successfully.')
            os.execv(sys.executable , [sys.executable, "-m", "app.main"])
        
        except Exception as e:
            print(f'An error occured while trying to install the latest version from github: {str(e)}')
            return False