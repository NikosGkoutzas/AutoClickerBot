from .read_email_interface import ReadEmailInterface
import imaplib , os , email
from email.utils import parsedate_to_datetime
from .process_emails_interface import ProcessEmailsInterface
from .send_email_interface import SendEmailInterface
from ..files.read_files_interface import ReadFilesInterface
from ..files.write_files_interface import WriteFilesInterface
from ..driver.driver_interface import DriverInterface
from ..action.action_interface import ActionInterface
import email.message , inject




class ReadEmail(ReadEmailInterface):
    @inject.autoparams()
    def __init__(self ,
                 process_emails_interface: ProcessEmailsInterface ,
                 send_email_interface: SendEmailInterface ,
                 read_files_interface: ReadFilesInterface ,
                 write_files_interface: WriteFilesInterface ,
                 driver_interface: DriverInterface ,
                 action_interface: ActionInterface):
        
        self.process_emails = process_emails_interface
        self.send_email = send_email_interface
        self.read_files = read_files_interface
        self.write_files = write_files_interface
        self.driver = driver_interface
        self.action = action_interface
    
    
    
    def fetch_last_emails(self) -> None:
        self.SMTP_SERVER = 'imap.gmail.com'                                         # server domain
        self.SMTP_PORT = 993                                                        # port
        mail = imaplib.IMAP4_SSL(self.SMTP_SERVER)                                  # connect to gmail server
        mail.login(os.getenv('email_sender') , os.getenv('email_sender_password'))  # login to gmail with credentials
        mail.select('inbox')                                                        # select inbox
        data = mail.search(None , 'ALL')                                            # ('OK', [b'1 2 3 4 5 6'])
        ids_list = data[1][0].split()                                               # id_list = [b'1', b'2', b'3', b'4', ...., b'20']
        number_of_recent_emails = int(os.getenv('read_number_of_recent_emails'))    # get the last X recent emails
        first_x_recent_ids = ids_list[-number_of_recent_emails:][::-1]              # first 20 email ids
        body_list_added = []
        body_list_removed = []
        body_list_credentials = []
        body_list_new_version = []
        emails_add_list = []
        emails_delete_list = []
        emails_progress_list = []
        emails_new_version_list = []
        emails_credentials_list = []
        emails_teamviewer_list = []
        emails_credentials_found = False
        emails_progress_found = False
        emails_new_version_found = False
        emails_teamviewer_found = False
        
        for i in range(len(first_x_recent_ids)):    
            _ ,email_data = mail.fetch(first_x_recent_ids[i] , '(RFC822)')
            for response_part in email_data:
                if isinstance(response_part , tuple):
                    msg = email.message_from_bytes(response_part[1])
                    email_date = str(parsedate_to_datetime(msg['Date']).strftime('%b %d, %Y - %H:%M:%S'))
                    email_subject = msg['subject'].lower().strip() if msg['subject'] else 'No subject'
                    
                    self.read_insert_subject(body_list_added , email_subject , msg , email_date , number_of_recent_emails , i , emails_add_list)     
                    self.read_remove_subject(body_list_removed , email_subject , msg , email_date , number_of_recent_emails , i , emails_delete_list)
                    
                    if(not emails_teamviewer_found):
                        emails_teamviewer_found = True
                        self.read_connect_with_teamviewer_email(email_subject , email_date , emails_teamviewer_list)
                        
                    if(not emails_new_version_found):
                        emails_new_version_found = True
                        self.read_new_version_email(body_list_new_version , email_subject , msg , email_date , emails_new_version_list)
                    
                    if(not emails_progress_found):
                        emails_progress_found = True
                        self.read_progress_email(email_subject , email_date , emails_progress_list)
                    
                    if(not emails_credentials_found): # retrieve only the first one from emails (which is the last one user has sent / last change)
                        emails_credentials_found = True
                        self.read_credentials_subject(body_list_credentials , email_subject , msg , email_date , emails_credentials_list)
    
    

    
    def read_email_subject(self ,
                           title: str ,
                           body_list: list[str] ,
                           email_subject: str ,
                           msg: email.message.Message ,
                           email_date: str ,
                           email_content_list: list[str]
                           ) -> tuple[list[str] , list[str]]:
        try:
            if(email_subject.strip().lower() == title.strip().lower() and email_date not in self.read_files.read_email_dates()):
                self.write_files.write_email_dates(email_date)
                                
                if(title.strip().lower() == 'add'):
                    email_content_list.append('OK')     # this list is to check if at least one email contains an 'add', 'delete', etc. title.
                                                        # If so, at the end of all emails that we read, we send an email, otherwise we don't.
                    
                elif(title.strip().lower() == 'delete'):
                    email_content_list.append('OK')
                    
                elif(title.strip().lower() == 'progress'):
                    email_content_list.append('OK')
                
                elif(title.strip().lower() == 'update'):
                    email_content_list.append('OK')
                    
                elif(title.strip().lower() == 'credentials'):
                    email_content_list.append('OK')
                    
                elif(title.strip().lower() == 'teamviewer'):
                    email_content_list.append('OK')
                
                if(msg is not None):
                    for part in msg.walk():
                        content_type = part.get_content_type()

                        if(content_type == 'text/plain'):
                            body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                            lines = body.splitlines()
                            body = [line.strip() for line in lines if line.strip()]
                            body_list.extend(body)

            return body_list , email_content_list
                        
        except Exception as e:
            print(f'An error occured: {str(e)}')
            self.write_files.write_total_errors()
        
        



        
            
    def read_insert_subject(self ,
                            body_list: list[str] ,
                            email_subject: str ,
                            msg: email.message.Message ,
                            email_date: str ,
                            number_of_recent_emails: int ,
                            current_number_read_email: int ,
                            emails_add_list: list[str]
                            ) -> None:

        list_added_links , emails_add_list = self.read_email_subject('Add' , body_list , email_subject , msg , email_date , emails_add_list)
        
        if(current_number_read_email == number_of_recent_emails - 1):
            valid_links , invalid_added_links = self.process_emails.process_add_link_email(list_added_links)
            
            if(len(emails_add_list) > 0):
                self.send_email.send_email_link_inserted(valid_links , invalid_added_links)
                
                


                
                
    
    def read_remove_subject(self ,
                            body_list: list[str] ,
                            email_subject: str ,
                            msg: email.message.Message ,
                            email_date: str ,
                            number_of_recent_emails: int ,
                            current_number_read_email: int ,
                            emails_delete_list: list[str]
                            ) -> None:
        
        list_removed_links , emails_delete_list = self.read_email_subject('Delete' , body_list , email_subject , msg , email_date , emails_delete_list)
        
        if(current_number_read_email == number_of_recent_emails - 1):
            valid_links , invalid_removed_links = self.process_emails.process_remove_link_email(list_removed_links)

            if(len(emails_delete_list) > 0):
                self.send_email.send_email_link_removed(valid_links , invalid_removed_links)
        
        
        
        
        
    def read_progress_email(self ,
                            email_subject: str ,
                            email_date: str ,
                            emails_progress_list: list[str]
                            ) -> None:
        
        _ , emails_progress_list = self.read_email_subject('Progress' , None , email_subject , None , email_date , emails_progress_list)
        
        if(len(emails_progress_list) > 0):  
            self.send_email.send_email_progress()
                
                
                
                
                
    def read_new_version_email(self ,
                               body_list: list[str] ,
                               email_subject: str ,
                               msg: email.message.Message ,
                               email_date: str ,
                               emails_new_version_list: list[str]
                               ) -> None:
        
        semantic_versioning , emails_new_version_list = self.read_email_subject('Update' , body_list , email_subject , msg , email_date , emails_new_version_list)
        success , semantic_input = self.process_emails.process_new_version_email(semantic_versioning)
        
        if(body_list):
            body_list.clear()
            
        if(len(emails_new_version_list) > 0): 
            if(success):                   
                if(not self.process_emails.download_new_version_from_github(semantic_input)):
                    self.send_email.send_email_new_version_failed_to_update()

            else:
                self.send_email.send_email_error_installing_new_version_missing_type()

    
    
        
        
        
    
    def read_credentials_subject(self ,
                                 body_list: list[str] ,
                                 email_subject: str ,
                                 msg: email.message.Message ,
                                 email_date: str ,
                                 emails_credentials_list: list[str]
                                 ) -> None:
        
        list_changed_credentials , emails_credentials_list = self.read_email_subject('Credentials' , body_list , email_subject , msg , email_date , emails_credentials_list)
        credential_messages = self.process_emails.process_change_credentials_email(list_changed_credentials)
        
        if(len(emails_credentials_list) > 0):
            if(credential_messages.strip().lower() == 'ok'):
                self.driver.logout()
                self.action.check_login()
                
            self.send_email.send_email_credentials_updated(credential_messages)
            
            
            
            
            
    
    def read_connect_with_teamviewer_email(self ,
                                        email_subject: str ,
                                        email_date: str ,
                                        emails_teamviewer_list: list[str]
                                        ) -> None:
        
        _ , emails_teamviewer_list = self.read_email_subject('TeamViewer' , None , email_subject , None , email_date , emails_teamviewer_list)
        
        if(len(emails_teamviewer_list) > 0):
            self.send_email.send_email_connect_via_teamviewer()