import sys

from typing import (
    Optional,
    List
)

from sigmaF.repl import start_repl

SIGMAF: str = """ 
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


def main(arg=None) -> None:
    global SIGMAF
    print('-'*106)
    print(
        f'\n\nWelcome to SigmaF, the Program Language of the future for the Programming Functional and a lot more\n\n{SIGMAF}')
    print('-'*106)
    if arg is None:
        start_repl()
    else:
        with open(arg, mode='r', encoding='utf-8') as fin:
            lines = fin.readlines()
        start_repl('\n'.join(lines))


if __name__ == '__main__':
    args: List[str] = sys.argv
    arg: Optional[str]

    if len(args) > 1:
        arg = args[1]
    else:
        arg = None

    main(arg)
