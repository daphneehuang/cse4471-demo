''' __main__ module. '''
from arg_parsing.arg_parsing import setup_argparse

setup_argparse()

def display_results(results):
    """Prints the results of vulnerability searches to the terminal
    
        [:param `results`] a dictionary of key/value pairs, where the key is a file path string, and the value is a list of strings representing vulnerabilities in that file. The vulnerability string is formatted as "type:line_num"
    """
    if results:
        print('The following vulnerabilities were found:')

        for file, v_list in results.items():
            if  v_list:
                print(file)
                for v in v_list:
                    type, _, line = v.partition(':')
                    print(f' * {type} at line {line}')
    else:
        print('No vulnerabilities were found')

    return

def save_results(results, file_name):
    """Saves the results of vulnerability searches to a file
    
        [:param `results`] a dictionary of key/value pairs, where the key is a file path string, and the value is a list of strings representing vulnerabilities in that file. The vulnerability string is formatted as "type:line_num"

        [:param `file_name`] a string representing the file path where the results will be written
    """

    with open(file_name, mode='x') as fp:

        if results:
            fp.write('The following vulnerabilities were found:\n')

            for file, v_list in results.items():
                if  v_list:
                    fp.write(f'{file}\n')
                    for v in v_list:
                        type, _, line = v.partition(':')
                        fp.write(f' * {type} at line {line}\n')
        else:
            fp.write('No vulnerabilities were found\n')

# for testing purposes
# results = {
#     'cool/file/path.py': ['API key:29', 'Password:12', 'email:59'],
#     'neat/file/path.java': ['Password:32', 'email:99'],
# }

# display_results(results)
# save_results(results, 'test.txt')