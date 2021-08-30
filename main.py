import sys
import yaml
import re
import argparse
import os

from typing import Optional, List, cast

from sigmaF.repl import start_repl, read_module
from sigmaF.executor import execute_sigmaf

import sys

sys.setrecursionlimit(10000)

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
    print("-" * 106)
    print(
        f"\n\nWelcome to SigmaF v{version}, the Program Language of the future for the Programming Functional and a lot more\n\n{_SIGMAF_}"
    )
    print("-" * 106)


def show_head(version):
    print(f"SigmaF v{version} | Exit: exit() | Update: update()")


def get_configs():
    with open("configs.yaml", "r") as fin:
        configs = yaml.load(fin, Loader=yaml.FullLoader)
    return dict(configs)

def main(configs, args, input_path):
    if args.version:
        version = "SigmaF v{}".format(configs["version"])
        print(version)
        return
    
    if input_path is not None and not os.path.isfile(input_path):
        print(f"The path {input_path} does not exist")
        sys.exit()

    if input_path is not None and not re.match(r"^\S+?\.sf$", input_path):
        print(f"The path {input_path} is not a SigmaF file")
        sys.exit()

    if args.cover:
        show_cover(configs["version"])

    else:
        show_head(configs["version"])

    if args.repl:
        try:
            if input_path is not None:
                src = read_module(input_path)

                start_repl(source=src, _path=input_path)
            else:
                start_repl(_path=input_path)
        except KeyboardInterrupt:
            print("\n↳ Good bye \n")

    elif input_path is not None:
        execute_sigmaf(input_path)

    else:
        start_repl(_path=input_path)


if __name__ == "__main__":
    configs = get_configs()

    console_parser = argparse.ArgumentParser(prog="SigmaF")

    console_parser.add_argument(
        "Path", metavar="path", type=str, nargs="?", help="Path to the SigmaF file"
    )

    console_parser.add_argument(
        "-v", "--version", action="store_true", help="Show the version of SigmaF"
    )

    console_parser.add_argument("-r", "--repl", action="store_true", help="Start the repl")

    cover_parse = console_parser.add_mutually_exclusive_group()
    cover_parse.add_argument("-c", "--cover", action="store_true", help="Show the cover of SigmaF")
    cover_parse.add_argument(
        "-n", "--ncover", action="store_true", help="Don't show the cover of SigmaF"
    )

    args = console_parser.parse_args()
    input_path = args.Path

    main(configs, args, input_path)
    