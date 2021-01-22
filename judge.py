"""
Build: pyinstaller.exe --onedir --noconsole --noconfirm --add-data "fae.json;." judge.py
"""
import os
import subprocess
import sys

from config import load_config
from log import logger
from util import get_extension

if __name__ == '__main__':
    try:
        logger.info(r'''
     ____.         .___                 _________ __                 __   
    |    |__ __  __| _/ ____   ____    /   _____//  |______ ________/  |_ 
    |    |  |  \/ __ | / ___\_/ __ \   \_____  \\   __\__  \\_  __ \   __\
/\__|    |  |  / /_/ |/ /_/  >  ___/   /        \|  |  / __ \|  | \/|  |  
\________|____/\____ |\___  / \___  > /_______  /|__| (____  /__|   |__|  
                    \/_____/      \/          \/           \/             
        ''')
        if len(sys.argv) != 2:
            logger.error(f'[Judge] The input judge arguments is invalid, args: {sys.argv}')
        else:
            file = os.path.abspath(sys.argv[1])
            extension = get_extension(file)
            config = load_config()

            logger.info(f'[Judge] Start judging...')
            logger.info(f'[Judge] File: {file}')
            for rule in config['rules']:
                try:
                    if rule["folder"] in file:
                        logger.info(f'[Judge] Match folder: {rule["folder"]}')
                        rule_command = f'{rule["app"]} "{file}"'
                        logger.info(f'[Judge] run rule command: {rule_command}')
                        subprocess.run(rule_command)
                except Exception as e:
                    logger.error('[Judge] Exception detected during runtime', e)
                    break
            else:
                rule_command = f'{config["fallback"]} "{file}"'
                logger.info(f'[Judge] run fallback command: {rule_command}')
                subprocess.run(rule_command)
    except Exception as e:
        logger.error(f'[Judge] Exception detected during judge', e)
