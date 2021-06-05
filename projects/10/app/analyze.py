import os
from glob import glob
from typing import TextIO, Tuple
from .tokenizer import Tokenizer
from .parser import CompileEngine
from threading import Thread

JACK_FILE_EXT = ".jack"
XML_FILE_EXT = "T1.xml"


def analyze_one_file(jack_file_name: str):
    xml_file_name = jack_file_name.replace(JACK_FILE_EXT, XML_FILE_EXT, -1)
    with open(jack_file_name, 'r') as jack_file, open(xml_file_name, 'w') as xml_file:
        tokenizer = Tokenizer(jack_file)
        tokenizer.tokenize()
        compiler = CompileEngine(tokenizer, xml_file)
        compiler.compile()


def analyze(jack_file_or_directory_name: str) -> None:
    if os.path.isdir(jack_file_or_directory_name):
        # get all .jack files
        path_to_jack_files = glob(
            os.path.join(jack_file_or_directory_name, "*" + JACK_FILE_EXT)
        )
    else:
        path_to_jack_files = [jack_file_or_directory_name]

    analyzers = []
    for jack_file_name in path_to_jack_files:
        worker = Thread(target=analyze_one_file, args=(jack_file_name,))
        worker.start()
        analyzers.append(worker)

    for analyzer in analyzers:
        analyzer.join()
