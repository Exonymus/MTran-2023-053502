import re
from itertools import groupby

# Define regular expressions for each token category
keywords = ['break', 'case', 'const', 'continue', 'default', 'endl',
            'do', 'else', 'enum', 'extern', 'for', 'goto',
            'if', 'register', 'return', 'namespace', 'cin', 'cout',
            'sizeof', 'static', 'struct', 'switch', 'typedef', 'union',
            'volatile', 'while', 'include', 'using', 'std', 'std::']

var_types = ['bool', 'char', 'double', 'float', 'int', 'long', 'short', 'signed', 'unsigned', 'void', 'string']

operators = ['>>=', '<<=', '++', '--', '==', '!=', '<=', '>', '>=', '*=', '/=', '%=', '&=', '|='
             '&&', '||', '&', '|', '^', '~', '<<', '>>', '+=',
             '-=', '^=', '<', '*', '/', '%', '+', '-', '!']

delimiters = ['(', ')', '[', ']', '{', '}', ',', ';', ':']

identifiers = r'[a-zA-Z_][a-zA-Z0-9_]*'
int_numbers = r'\d+(\.\d*)?([Ee][+-]?\d+)?'
float_numbers = r'\d+\.\d+([Ee][+-]?\d+)?'
strings = r'"([^"\\]|\\.)*"|\'([^\'\\]|\\.)*\''

# Define a regular expression for matching all tokens
token_pattern = re.compile('|'.join([re.escape(var_type) for var_type in var_types] +
                                    [re.escape(keyword) for keyword in keywords] +
                                    [re.escape(operator) for operator in operators] +
                                    [re.escape(delimiter) for delimiter in delimiters] +
                                    [identifiers, int_numbers, float_numbers, strings]))

# Read the input C++ file
with open('main.cpp', 'r') as file:
    code = file.readlines()

# Initialize dictionary to hold tokens for each category
token_categories = {
    'Keywords': [],
    'Variable Types': [],
    'Operators': [],
    'Delimiters': [],
    'Identifiers': [],
    'Integer Numbers': [],
    'Float/Double Numbers': [],
    'Strings': [],
    'Errors': []
}

# Find all tokens in the code and categorize them
for line_no, line in enumerate(code, 1):
    line_end = False

    for match in token_pattern.finditer(line):
        token = match.group(0)
        col_start = match.start() + 1
        col_end = match.end()
        if token in keywords and line_end is False:
            category = 'Keywords'
        elif token in var_types and line_end is False:
            category = 'Variable Types'
        elif token in operators and line_end is False:
            category = 'Operators'
        elif token in delimiters and line_end is False:
            category = 'Delimiters'
            if token == ';' and line.__contains__('for') is False and line[(col_end + 1):].__contains__(';') is False:
                line_end = True
        elif re.match(identifiers, token) and line_end is False:
            category = 'Identifiers'
        elif re.match(float_numbers, token) and line_end is False:
            category = 'Float/Double Numbers'
            # Bad float/double errors detect
            if line[col_end] not in (',', ';', ' ', '+', '-', '*', '=', '/', '%', '(', ')', '[', ']', '}'):
                token_categories['Errors'].append(("Unknown symbol after float number: " + line[col_end], line_no, col_end, col_end))
                break
        elif re.match(int_numbers, token) and line_end is False:
            category = 'Integer Numbers'
            if line[col_start - 2] == '.':
                category = 'Errors'
            # Bad integer errors detect
            if line[col_end] not in (',', ';', ' ', '+', '-', '*', '=', '/', '%', '(', ')', '[', ']', '}'):
                token_categories['Errors'].append(("Unknown symbol after integer number: " + line[col_end], line_no, col_end, col_end))
                break
        elif re.match(strings, token) and line_end is False:
            category = 'Strings'
        else:
            category = 'Errors'
        token_categories[category].append((token, line_no, col_start, col_end))

    # Quotes errors detect
    if line.count("'") % 2 != 0:
        token_categories['Errors'].append(("Single quotes unclosed - '", line_no, line.rfind("'"), line.rfind("'")))
        for item in token_categories['Strings']:
            if item[1] == line_no and item[2] == line.rfind("'") - 1:
                token_categories['Strings'].pop(token_categories['Strings'].index(item))
        break
    if line.count('"') % 2 != 0:
        token_categories['Errors'].append(('Double quotes unclosed - "', line_no, line.rfind('"'), line.rfind('"')))
        for item in token_categories['Strings']:
            if item[1] == line_no and item[2] == line.rfind('"') - 1:
                token_categories['Strings'].pop(token_categories['Strings'].index(item))
        break

    # Semicolon errors detect
    if re.match('^(?! *#)(?:(?!for\b|while\b|if\b|else\b|'
                'do\b|switch\b|case\b|default\b|struct\b|'
                'class\b|namespace\b|typedef\b|return\b)'
                '[^;{}]*;|.*\{.*\}.*|.*\}.*|.*\{.*)', line) is None\
            and re.match('^(?:\s*|.*//.*)$|^\s*#\s*include\s+<.*>\s*$', line) is None\
            and re.match('^\s*if\s*\([^;]+?\)[^{;]*$', line) is None\
            and re.match('^\s*[a-zA-Z_]+\s+[a-zA-Z_]+'
                         '\s*\(\s*([a-zA-Z_]+\s+[*&]*'
                         '\s*[a-zA-Z_]+[\[\]]*\s*,'
                         '\s*)*([a-zA-Z_]+\s+[*&]*'
                         '\s*[a-zA-Z_]+[\[\]]*)?\s*\)\s*$', line) is None\
            and line.__contains__(';') is False\
            and line.__contains__('while') is False:
        token_categories['Errors'].append(('; was expected at end of the line',
                                           line_no, str.__len__(line) - 1, str.__len__(line) - 1))
        break

print("<----------------------------->")
for category, tokens in token_categories.items():
    print(f'{category}:')
    if category != "Errors":
        printed_tokens = set()
        for token in tokens:
            if token[0] not in printed_tokens:
                print(f'\tToken: | {token[0]} | Coordinates: [{token[1]}:{token[2]}]')
                printed_tokens.add(token[0])
    else:
        for token in tokens:
            print(f'\tInvalid Token: | {token[0]} | Coordinates: [{token[1]}:{token[2]}]')

    print("<----------------------------->")
