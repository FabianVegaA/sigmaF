import sys
import yaml
import re

from typing import (
    Optional,
    List,
    cast
)

from sigmaF.repl import (
    start_repl,
    read_module    
)


_SIGMAF_: str = """ 
                                                .         .                                                
   d888888o.    8 8888     ,o888888o.          ,8.       ,8.                   .8.          8 8888888888   
 .`8888:' `88.  8 8888    8888     `88.       ,888.     ,888.                 .888.         8 8888         
 8.`8888.   Y8  8 8888 ,8 8888       `8.     .`8888.   .`8888.               :88888.        8 8888         
 `8.`8888.      8 8888 88 8888              ,8.`8888. ,8.`8888.             . `88888.       8 8888         
  `8.`8888.     8 8888 88 8888             ,8'8.`8888,8^8.`8888.           .8. `88888.      8 888888888888 
   `8.`8888.    8 8888 88 8888            ,8' `8.`8888' `8.`8888.         .8`8. `88888.     8 8888         
    `8.`8888.   8 8888 88 8888   8888888 ,8'   `8.`88'   `8.`8888.       .8' `8. `88888.    8 8888         
8b   `8.`8888.  8 8888 `8 8888       .8',8'     `8.`'     `8.`8888.     .8'   `8. `88888.   8 8888         
`8b.  ;8.`8888  8 8888    8888     ,88',8'       `8        `8.`8888.   .888888888. `88888.  8 8888         
 `Y8888P ,88P'  8 8888     `8888888P' ,8'         `         `8.`8888. .8'       `8. `88888. 8 8888         
"""



def show_cover(version):
    global _SIGMAF_
    print('-'*106)
    print(
        f'\n\nWelcome to SigmaF v{version}, the Program Language of the future for the Programming Functional and a lot more\n\n{_SIGMAF_}')
    print('-'*106)


def show_head(version):
    print(f'SigmaF v{version} | Exit: exit() | Update: update()')


def get_configs():
    with open('configs.yaml', 'r') as fin:
        configs = yaml.load(fin, Loader=yaml.FullLoader)
    return dict(configs)


def presentation_config(configs, params, exe_file=False):
    version = configs['version']
    if not params is None:
        if exe_file:
            if '-cover' in params:
                show_cover(version)
                return
            show_head(version)
        else:
            if not '-ncover' in params:
                show_cover(version)
                return
            show_head(version)
    else:
        if exe_file:
            show_head(version)
        else:
            show_cover(version)




def main(path=None, params=None) -> None:
    configs = get_configs()
    if not params is None and '-version' in params:
        version = configs['version']
        print(f'SigmaF v{version}')
        return
    if path is None:
        presentation_config(configs, params, exe_file=False)
        start_repl()
    elif not path is None:
        presentation_config(configs, params, exe_file=True)

        src = read_module(path)
        if not src is None:
            start_repl(src, path)


def filter_path_params(args):
    path = list(filter(lambda s: not re.match('(\S+?\.sf$)', s) is None, args))
    params = list(filter(lambda s: s.startswith('-'), args))
    if len(path) > 0:
        path = path[0]
    else:
        path = None

    if len(params) == 0:
        params = None

    return path, params


if __name__ == '__main__':
    args: List[str] = sys.argv

    if len(args) > 1:
        path, params = filter_path_params(args)
    else:
        path, params = None, None
    try:
        main(path, params)
    except KeyboardInterrupt:
        print('\n↳ Good bye \n')
