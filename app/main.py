from .container import configure_dependencies
from .run.run_interface import RunInterface
import inject


def main():
    '''
    Configures dependency injection and starts the main application flow.
    '''
    inject.configure_once(configure_dependencies)
    inject.instance(RunInterface).run()


if (__name__ == '__main__'):
    main()
