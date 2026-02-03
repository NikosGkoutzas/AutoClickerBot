from .read_email_interface import ReadEmailInterface
import imaplib , os , email
from email.utils import parsedate_to_datetime
from .process_emails_interface import ProcessEmailsInterface
from .send_email_interface import SendEmailInterface
from ..files.read_files_interface import ReadFilesInterface
from ..files.write_files_interface import WriteFilesInterface
from ..driver.driver_interface import DriverInterface
from ..action.action_interface import ActionInterface
from dotenv import load_dotenv
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
        '''
        Connects to the configured Gmail inbox and processes the most recent emails.

        The function retrieves the last N emails from the inbox (as defined in the
        environment configuration) and inspects their subjects and contents to
        detect supported commands, such as: - adding or removing links,
                                            - requesting application progress,
                                            - updating login credentials,
                                            - triggering a new version update,
                                            - starting or stopping a TeamViewer connection.

        For each supported command type, only the most recent relevant email is
        processed to avoid duplicate or conflicting actions.

        :Parameters: None
        :Returns: None
        '''
        self.SMTP_SERVER = 'imap.gmail.com'                                         # server domain
        self.SMTP_PORT = 993                                                        # port
        mail = imaplib.IMAP4_SSL(self.SMTP_SERVER)                                  # connect to gmail server
        load_dotenv(override=True)
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
        emails_start_teamviewer_list = []
        emails_stop_teamviewer_list = []
        emails_credentials_found = False
        emails_progress_found = False
        emails_new_version_found = False
        emails_start_teamviewer_found = False
        emails_stop_teamviewer_found = False
        
        for i in range(len(first_x_recent_ids)):    
            status , email_data = mail.fetch(first_x_recent_ids[i] , '(RFC822)')
            
            if(status != 'OK'):
                continue
            
            for response_part in email_data:
                if isinstance(response_part , tuple):
                    msg = email.message_from_bytes(response_part[1])
                    email_date = str(parsedate_to_datetime(msg['Date']).strftime('%b %d, %Y - %H:%M:%S'))
                    email_subject = msg['subject'].lower().strip() if msg['subject'] else 'No subject'
                    
                    self.read_insert_subject(body_list_added , email_subject , msg , email_date , number_of_recent_emails , i , emails_add_list)     
                    self.read_remove_subject(body_list_removed , email_subject , msg , email_date , number_of_recent_emails , i , emails_delete_list)
                    
                    if(not emails_start_teamviewer_found):
                        emails_start_teamviewer_found = True
                        self.read_connect_via_teamviewer_email(email_subject , email_date , emails_start_teamviewer_list)
                        
                    if(not emails_stop_teamviewer_found):
                        emails_stop_teamviewer_found = True
                        self.read_disconnect_from_teamviewer_email(email_subject , email_date , emails_stop_teamviewer_list)
                        
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
                           subject: str ,
                           body_list: list[str] ,
                           email_subject: str ,
                           msg: email.message.Message ,
                           email_date: str ,
                           email_content_list: list[str]
                           ) -> tuple[list[str] , list[str]]:
        '''
        Processes an email with a specific subject and extracts its plain text content.

        The function checks whether the email subject matches the expected subject
        and ensures that the email has not been processed before (based on its date).
        If valid, the email body is parsed and its non-empty lines are collected.

        Additionally, the function tracks whether at least one supported command
        email was found, allowing further actions to be triggered after all emails
        are processed.

        Supported subjects include: - add
                                    - delete
                                    - progress
                                    - update
                                    - credentials
                                    - start teamviewer
                                    - stop teamviewer

        :Parameters: subject (str): The expected email subject to match.
                     body_list (list[str]): A list where extracted email body lines will be appended.
                     email_subject (str): The subject of the current email being processed.
                     msg (email.message.Message): The email message object.
                     email_date (str): The formatted date of the email.
                     email_content_list (list[str]): A list used to indicate that a valid
                                                     command email was detected.
        :Returns: tuple[list[str], list[str]]: - The updated list containing extracted email body lines.
                                               - The updated list indicating detected command emails.
        '''
        try:
            if(email_subject.strip().lower() == subject.strip().lower() and email_date not in self.read_files.read_email_dates()):
                self.write_files.write_email_dates(email_date)
                                
                # This list is to check if at least one email contains an 'add', 'delete', etc. subject.
                # If so, at the end of all emails that we read, we send an email, otherwise we don't.
                subjects_list = ['add' , 'delete' , 'progress' , 'update' , 'credentials' , 'start teamviewer' , 'stop teamviewer']

                if(subject.strip().lower() in subjects_list):
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
        '''
        Processes emails with the "Add" subject and handles link insertion requests.

        The function collects links from email bodies whose subject matches "Add"
        and ensures that each email is processed only once. After all recent emails
        have been examined, the collected links are validated and categorized into
        valid and invalid entries.

        If at least one valid "Add" command email was detected, a notification email
        is sent summarizing the successfully added links and those that were rejected.

        :Parameters: body_list (list[str]): A list used to accumulate link entries extracted from email bodies.
                     email_subject (str): The subject of the current email being processed.
                     msg (email.message.Message): The email message object.
                     email_date (str): The formatted date of the email.
                     number_of_recent_emails (int): The total number of recent emails being processed.
                     current_number_read_email (int): The index of the currently processed email.
                     emails_add_list (list[str]): A list used to indicate that at least one "Add" command email was found.
        :Returns: None
        '''
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
        '''
        Processes emails with the "Delete" subject and handles link removal requests.

        The function collects links from email bodies whose subject matches "Delete"
        and ensures that each email is processed only once. After all recent emails
        have been examined, the collected links are validated and categorized into
        successfully removed and invalid entries.

        If at least one valid "Delete" command email was detected, a notification
        email is sent summarizing the links that were removed and those that could
        not be processed.

        :Parameters: body_list (list[str]): A list used to accumulate link entries extracted from email bodies.
                     email_subject (str): The subject of the current email being processed.
                     msg (email.message.Message): The email message object.
                     email_date (str): The formatted date of the email.
                     number_of_recent_emails (int): The total number of recent emails being processed.
                     current_number_read_email (int): The index of the currently processed email.
                     emails_delete_list (list[str]): A list used to indicate that at least one "Delete" command email was found.
        :Returns:None
        '''
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
        '''
        Processes emails with the "Progress" subject and handles progress requests.

        The function checks whether an email with the subject "Progress" has been
        received and ensures that it has not been processed before. If at least one
        valid progress request email is detected, a response email is sent containing
        the current application progress information.

        Only the most recent relevant email is considered to prevent duplicate
        progress notifications.

        :Parameters: email_subject (str): The subject of the current email being processed.
                     email_date (str): The formatted date of the email.
                     emails_progress_list (list[str]): A list used to indicate that a "Progress" command email was found.
        :Returns:None
        '''
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
        '''
        Processes emails with the "Update" subject and handles application
        version update requests.

        The function extracts semantic versioning instructions (major, minor, patch)
        from the email body and validates the requested update type. If a valid update
        request is detected, the latest version of the application is downloaded from
        GitHub, installed, and the application is restarted.

        If the update process fails, an error notification is sent and a TeamViewer
        session is opened to allow manual intervention. If the update request is
        missing or invalid, an appropriate error email is sent.

        :Parameters: body_list (list[str]): A list used to accumulate semantic versioning
                                            instructions from the email body.
                     email_subject (str): The subject of the current email being processed.
                     msg (email.message.Message): The email message object.
                     email_date (str): The formatted date of the email.
                     emails_new_version_list (list[str]): A list used to indicate that an "Update" command email was found.
        :Returns: None
        '''
        semantic_versioning , emails_new_version_list = self.read_email_subject('Update' , body_list , email_subject , msg , email_date , emails_new_version_list)
        success , semantic_input = self.process_emails.process_new_version_email(semantic_versioning)
        
        if(body_list):
            body_list.clear()
            
        if(len(emails_new_version_list) > 0): 
            if(success):                   
                if(not self.process_emails.process_download_new_version_from_github(semantic_input)):
                    self.send_email.send_email_new_version_failed_to_update()
                    self.action.open_teamviewer()

            else:
                self.send_email.send_email_error_installing_new_version_missing_type()

    
    
        
        
        
    
    def read_credentials_subject(self ,
                                 body_list: list[str] ,
                                 email_subject: str ,
                                 msg: email.message.Message ,
                                 email_date: str ,
                                 emails_credentials_list: list[str]
                                 ) -> None:
        '''
        Processes emails with the "Credentials" subject and handles
        username and/or password update requests.

        The function extracts credential change instructions from the email
        body, validates the requested updates, and applies them to the
        application's environment configuration. Only one or two updates
        (username and/or password) are allowed per request.

        If the credentials are successfully updated, the user is logged out
        and a new login attempt is performed using the updated credentials.
        In all cases where a credentials-related email is detected, a
        notification email is sent describing the outcome of the request.

        :Parameters: body_list (list[str]): A list used to accumulate credential update instructions
                                            extracted from the email body.
                     email_subject (str): The subject of the current email being processed.
                     msg (email.message.Message): The email message object.
                     email_date (str): The formatted date of the email.
                     emails_credentials_list (list[str]): A list used to indicate that a "Credentials"
                                                         command email was found.

        :Returns: None
        '''
        list_changed_credentials , emails_credentials_list = self.read_email_subject('Credentials' , body_list , email_subject , msg , email_date , emails_credentials_list)
        credential_messages = self.process_emails.process_change_credentials_email(list_changed_credentials)
        
        if(len(emails_credentials_list) > 0):
            if(credential_messages.strip().lower() == 'ok'):
                self.driver.logout()
                self.action.check_login()
                
            self.send_email.send_email_credentials_updated(credential_messages)
            
            
            
            
            
    
    def read_connect_via_teamviewer_email(self ,
                                        email_subject: str ,
                                        email_date: str ,
                                        emails_start_teamviewer_list: list[str]
                                        ) -> None:
        '''
        Processes emails with the "Start TeamViewer" subject and initiates
        a remote access session via TeamViewer.

        The function checks whether the email subject matches the
        "start teamviewer" command and ensures that the email has not been
        processed before. If at least one valid command email is detected,
        the TeamViewer service and GUI are launched to enable remote access.

        :Parameters: email_subject (str): The subject of the current email being processed.
            email_date (str): The formatted date of the email.
            emails_start_teamviewer_list (list[str]): A list used to indicate that a "Start TeamViewer"
                                                      command email was found.
        :Returns: None
        '''
        _ , emails_start_teamviewer_list = self.read_email_subject('start teamviewer' , None , email_subject , None , email_date , emails_start_teamviewer_list)
        
        if(len(emails_start_teamviewer_list) > 0):
            self.action.open_teamviewer()
            
            
            
            
            
    def read_disconnect_from_teamviewer_email(self ,
                                        email_subject: str ,
                                        email_date: str ,
                                        emails_stop_teamviewer_list: list[str]
                                        ) -> None:
        '''
        Processes emails with the "Stop TeamViewer" subject and terminates
        an active TeamViewer remote access session.

        The function verifies whether the email subject matches the
        "stop teamviewer" command and ensures that the email has not been
        processed before. If at least one valid command email is detected,
        the TeamViewer application and service are stopped to disable
        remote access.

        :Parameters: email_subject (str): The subject of the current email being processed.
            email_date (str): The formatted date of the email.
            emails_stop_teamviewer_list (list[str]): A list used to indicate that a "Stop TeamViewer"
                                                     command email was found.
        :Returns: None
        '''
        _ , emails_stop_teamviewer_list = self.read_email_subject('stop teamviewer' , None , email_subject , None , email_date , emails_stop_teamviewer_list)
        
        if(len(emails_stop_teamviewer_list) > 0):
            self.action.close_teamviewer()