from .container import configure_dependencies
from .run.run_interface import RunInterface
import inject

from .email.process_emails_interface import ProcessEmailsInterface

def main():
    inject.configure_once(configure_dependencies)
    inject.instance(ProcessEmailsInterface).download_new_version_from_github()
    
    

if(__name__ == '__main__'):
    main()
    