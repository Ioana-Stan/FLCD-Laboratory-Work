import re

from Scanner.FileProcessing import get_tokens
from Scanner. SymbolTable import SymbolTable
from Scanner.ProgramInternalForm import PIF
from Scanner.regex import INT_CONSTANT_REGEX, STRING_CONSTANT_REGEX, IDENTIFIER_REGEX


class Scanner:
    def __init__(self):
        self._operators = ['+', '-', '*', '/', '>', '<', '=', '<=', '>=', '==', '!=', '%']
        self._separators = ['[', ']', '{', '}', ';', ':', '(', ')', '\'', '"']
        self._reserved_words = ['start', 'finish', 'def', 'int', 'char', 'string', 'log', 'read', 'if', 'then', 'else',
                                'while', 'execute', 'break', 'exit']
        self._reserved_tokens = get_tokens(
            "/Users/ioana/OneDrive/Desktop/FLCD-Laboratory-Work/Scanner/inputFiles/token.in")

    def needs_look_ahead(self, token):
        return token in ['>', '<', '=', '!']

    def is_reserved_token(self, token):
        return token in self._reserved_tokens

    def is_nr_const(self, token):
        result = INT_CONSTANT_REGEX.search(token)

        return result is not None

    def is_str_const(self, token):
        result = STRING_CONSTANT_REGEX.search(token)

        return result is not None

    def is_identifier_const(self, token):
        result = IDENTIFIER_REGEX.search(token)

        return result is not None

    def scan_by_line(self, file_name):
        symbol_table = SymbolTable()
        program_internal_form = PIF()

        # open file and read all lines
        program_file = open(file_name, 'r')
        lines = program_file.readlines()

        line_count = 0

        for line in lines:
            line_count += 1
            # get all word from file
            line_data = re.split('("[^a-zA-Z0-9\"\']")|([^a-zA-Z0-9\"\'])', line)

            # filter words and eliminate spaces
            line_data = list(filter(None, line_data))
            line_data = map(lambda e: e.strip(), line_data)
            line_data = list(filter(None, line_data))

            omit_next = False

            for i in range(len(line_data)):
                token = line_data[i]
                if not omit_next:
                    if self.needs_look_ahead(token) and line_data[i + 1] == '=':
                        program_internal_form.add(token + line_data[i + 1], 0)
                        omit_next = True
                    elif self.is_reserved_token(token):
                        program_internal_form.add(token, 0)
                    elif self.is_nr_const(token) or self.is_str_const(token) or self.is_identifier_const(token):
                        position = symbol_table.add(token)
                        program_internal_form.add(token, position)
                    else:
                        raise ValueError('Lexical error on token ' + token + ' at line: ' + str(line_count) + ' column: ' + str(i))
                else:
                    omit_next = False

        with open("/Users/ioana/OneDrive/Desktop/FLCD-Laboratory-Work/Scanner/outputFiles/ST.out", 'w') as file:
            file.write(str(symbol_table))

        with open("/Users/ioana/OneDrive/Desktop/FLCD-Laboratory-Work/Scanner/outputFiles/PIF.out", 'w') as file:
            file.write(str(program_internal_form))

        return symbol_table, program_internal_form, "Lexically correct"
