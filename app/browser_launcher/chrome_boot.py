from .chrome_boot_interface import ChromeBootInterface
from ..files.write_files_interface import WriteFilesInterface
from dotenv import load_dotenv
from ..paths.paths import chrome_path , user_data_dir , port
import subprocess , inject


load_dotenv()


class ChromeBoot(ChromeBootInterface):
    @inject.autoparams()
    def __init__(self , write_files_interface: WriteFilesInterface):
        self.write_files = write_files_interface
        
        
    def boot(self) -> None:
        try:
            subprocess.Popen(
                                [
                                    chrome_path,
                                    '--window-size=1920,1080',
                                    '--window-position=0,0',
                                    f'--remote-debugging-port={port}',
                                    f'--user-data-dir={user_data_dir}'
                                ] ,
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL,
                            )
            
        except Exception as e:
            print(f'An error occured trying to boot chrome: {str(e)}')
            self.write_files.write_total_errors()