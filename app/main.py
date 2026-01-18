from .container import configure_dependencies
from .run.run_interface import RunInterface
import inject


def main():
    inject.configure_once(configure_dependencies)
    inject.instance(RunInterface).run()
    

if(__name__ == '__main__'):
    main()