from .container import configure_dependencies
from .run.run_interface import RunInterface
import inject

from .files.reset_files_interface import ResetFilesInterface
from .email.process_emails_interface import ProcessEmailsInterface
def main():
    inject.configure_once(configure_dependencies)
    #inject.instance(ResetFilesInterface).reset_all_files()
    inject.instance(RunInterface).main()
    

if(__name__ == '__main__'):
    main()