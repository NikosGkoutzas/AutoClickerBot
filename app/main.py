from .container import configure_dependencies
from .run.run_interface import RunInterface
import inject

from .files.reset_files_interface import ResetFilesInterface
def main():
    inject.configure_once(configure_dependencies)
    #inject.instance(ResetFilesInterface).reset_all_files()
    inject.instance(RunInterface).run()
    

if(__name__ == '__main__'):
    main()