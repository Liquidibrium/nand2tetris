# Your code starts here:

import os
from glob import glob
from threading import Thread

from app.engine import CompileEngine
from app.tokenizer import Tokenizer

JACK_FILE_EXT = ".jack"
VM_FILE_EXT = ".vm"


def compile_one_file(path_to_jack_file: str) -> None:
    path_to_vm_file = path_to_jack_file.replace(JACK_FILE_EXT, VM_FILE_EXT, -1)
    file_name = os.path.basename(path_to_vm_file).split(VM_FILE_EXT)[0]
    with open(path_to_jack_file, "r") as jack_file, open(path_to_vm_file, "w") as vm_file:
        tokenizer = Tokenizer(jack_file)
        tokenizer.tokenize()
        compiler = CompileEngine(tokenizer, vm_file, file_name)
        compiler.compile()


def compile(jack_file_or_directory_name: str) -> None:
    if os.path.isdir(jack_file_or_directory_name):
        # get all .jack files
        path_to_jack_files = glob(
            os.path.join(jack_file_or_directory_name, "*" + JACK_FILE_EXT)
        )
    else:
        path_to_jack_files = [jack_file_or_directory_name]

    compilers = []
    i = 0
    for jack_file_name in path_to_jack_files:
        worker = Thread(target=compile_one_file, args=(jack_file_name,))
        worker.start()
        compilers.append(worker)
        i += 1
        # if i == 2:
        # break

    for compiler in compilers:
        compiler.join()
