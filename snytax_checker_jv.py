# JOANNA VEILLEUX
# the purpose of this program is to evaluate the correctness of the syntax of a Java program

import re

# PURPOSE: turn program file into a string containing program contents
def get_program_string():
    # file_name = input("What is the name of the file you would like to syntax check?(file_name.java): ") ADD BACK
    file_name = "ALevel.java"
    input_file = open(file_name, "r")

    string = ""
    for line in input_file:
        string += line

    return string


# PURPOSE: cause program to stop and display the error
def compile_error(string):
    print("ERROR:", string)
    exit()


# PURPOSE: return the contents of the code block it is passed
def get_contents(string):
    pattern_contents = r'(?<=\{).*(?=\})'
    string = re.search(pattern_contents, string).group()

    return string


# PURPOSE: print the current route the program is at
def print_route(route):
    print("\n**********************************************\n")
    print("\tVERIFYING", route)
    print("\n**********************************************\n")


# calls methods that remove comments, imports, and extra spaces
def sanitize(string):
    print("\n**********************************************\n")
    print("\tRAW PROGRAM STRING\n")
    print("\n**********************************************\n")
    print(string)
    print("\n**********************************************\n")
    print("\tCOMMENTS REMOVED\n")
    print("\n**********************************************\n")
    string = remove_comments(string)
    print(string)
    print("\n**********************************************\n")
    print("\tIMPORTS REMOVED\n")
    print("\n**********************************************\n")
    string = remove_imports(string)
    print(string)
    print("\n**********************************************\n")
    print("\tEXTRA SPACES REMOVED\n")
    print("\n**********************************************\n")
    string = remove_spaces(string)
    print(string)
    return string


# PURPOSE: returns program with comments removed
def remove_comments(string):
    pattern_multi = r'\/[*]\s*.*\n.*\s*[*]\/'
    string = re.sub(pattern_multi, "", string)

    pattern_single = r'\/\/.*'
    string = re.sub(pattern_single, "", string)

    return string


# PURPOSE: returns program with imports removed
def remove_imports(string):
    pattern_import = r'\bimport\b\s\bjava\b[.]\S*[.]\S*[;]\s*'
    string = re.sub(pattern_import, "", string)

    return string


# PURPOSE: returns program with extra spaces removed (program on one line)
def remove_spaces(string):
    pattern_spaces = r'\s+'
    string = re.sub(pattern_spaces, " ", string)

    return string


# PURPOSE: verify class declaration and code block
def verify_class(string):
    route = "CLASS"

    # finds class keyword
    pattern_find_class = r'\s*\bclass\b\s*'
    if re.search(pattern_find_class, string):
        while re.search(pattern_find_class, string):
            print_route(route)
            # finds class declaration and corresponding code block
            pattern_get_class = r'\s*\bclass\b\s*([a-z]*[A-Z]*)*\s*\{\s*.*\}.*((?=\bclass\b))|' \
                                r'\s*\bclass\b\s*([a-z]*[A-Z]*)*\s*\{\s*.*\}.*'
            if re.search(pattern_get_class, string):
                class_string = re.search(pattern_get_class, string).group()
                class_string_contents = get_contents(class_string)
                verify_main_str = verify_main(class_string_contents, route)
                verify_method_str = verify_method(verify_main_str, route)
                verify_conditional_str = verify_conditional(verify_method_str, route)
                print_route(route)
                print("BEFORE:", string)
                string = string.replace(class_string, "")
                print("AFTER:", string)
            else:
                compile_error("incorrect class declaration")
    else:
        return string
    return string


# PURPOSE: verify main declaration and code block
def verify_main(string, route):
    route += "-->MAIN"
    print_route(route)

    # finds main{
    pattern_find_main =  r'\s\bmain\b\s[(]'
    if re.search(pattern_find_main, string):
        # finds main declaration and code block
        pattern_get_main = r'\bpublic\b\s\bstatic\b\s\bvoid\b\s\bmain\b\s[(]\bString\b\s[[]]\s\bargs\b[)]\s*[{].*[}]'
        if re.search(pattern_get_main, string):
            main_string = re.search(pattern_get_main, string).group()
            main_string_contents = get_contents(main_string)
            verify_conditional_str = verify_conditional(main_string_contents, route)
            print_route(route)
            print("BEFORE:", string)
            string = re.sub(pattern_get_main, "", string)
            print("AFTER:", string)
        else:
            compile_error("incorrect main declaration")
    else:
        return string

    return string


# PURPOSE: verify method declaration and code block
def verify_method(string, route):
    route += "-->METHOD"
    print_route(route)

    # finds method declaration(
    pattern_find_methods = r'(\bpublic\b|\bprivate\b|\bprotected\b)*\s+(\bint\b|\bString\b|\bvoid\b|([A-Z]+[a-z]*)*)' \
                           r'+\s*([A-Z]*[a-z])*\s*\('
    if re.search(pattern_find_methods, string):
        while re.search(pattern_find_methods, string):
            # finds method declaration and corresponding code block
            pattern_get_method = r'(\bpublic\b|\bprivate\b|\bprotected\b)*\s+(\bint\b|\bString\b|\bvoid\b|([A-Z]+[a-z]*)' \
                                 r'*)+\s*([A-Z]*[a-z])*\s*\(.*?\)\s*\{.*?\}'
            if re.search(pattern_get_method, string):
                method_string = re.search(pattern_get_method, string).group()
                method_string_contents = get_contents(method_string)
                verify_conditional_str = verify_conditional(method_string_contents, route)
                print_route(route)
                print("BEFORE:", string)
                string = string.replace(method_string, "")
                print("AFTER:", string)
            else:
                compileError("incorrect method declaration")
    else:
        return string

    return string


# PURPOSE: class methods that verify conditional statements
def verify_conditional(string, route):
    string = verify_while(string, route)
    string = verify_else_if(string, route) # need to verify else if first (if catches else if)
    string = verify_if(string, route)
    string = verify_else(string, route)
    verify_statement(string, route)
    return string


# PURPOSE: verify while declaration and code block
def verify_while(string, route):
    route += "-->WHILE"
    print_route(route)

    # finds while(
    pattern_find_while = r'\s*\bwhile\b\s*\('
    if re.search(pattern_find_while, string):
        while re.search(pattern_find_while, string):
            # finds all while declarations and corresponding code blocks
            pattern_get_while = r'\s*\bwhile\b\s*\((([a-z]*[A-Z]*)*|\d*)\s*([<]|[>]|\<\=|\>\=|\=\=|\!\=)\s*' \
                            r'(\d*|([a-z]*[A-Z]*)*)\s*\)\s*[{].*?[}]|' \
                            r'(\s*\bwhile\b\s*\(\s*([a-z]*[A-Z]*)*\d*\s*([<]|[>]|\<\+|\>\=|\=\=|\!\=)\s*' \
                            r'([a-z]*[A-Z]*)*\d*\s*(\&\&|\|\|)\s*([a-z]*[A-Z]*)*\d*\s*([<]|[>]|\<\+|\>\=|\=\=|\!\=)' \
                            r'\s*([a-z]*[A-Z]*)*\d*\s*\)\{.*?\})'
            if re.search(pattern_get_while, string):
                while_string = re.search(pattern_get_while, string).group()
                while_string_contents = get_contents(while_string) #works?
                verify_statement_str = verify_statement(while_string_contents, route)
                print_route(route)
                print("BEFORE:", string)
                string = re.sub(pattern_get_while, "", string)
                print("AFTER:", string)
            else:
                compile_error("incorrect while declaration")
    else:
        return string
    return string


# PURPOSE: verify else if declaration and code block
def verify_else_if(string, route):
    route += "-->ELSE IF"
    print_route(route)

    # finds else if(
    pattern_find_else_if = r'\s*\belse\b\s*\bif\b\s*\('

    while re.search(pattern_find_else_if, string):
        #finds all else if declarations and corresponding code block
        pattern_get_else_if = r'\s*\belse\b\s*\bif\b\s*\((([a-z]*[A-Z]*)*|\d*)\s*([<]|[>]|\<\+|\>\=|\=\=|\!\=)\s*' \
                            r'(\d*|([a-z]*[A-Z]*)*)\s*\)\s*[{].*?[}]|' \
                            r'\s*\belse\b\s*\bif\b\s*\(\s*([a-z]*[A-Z]*)*\d*\s*([<]|[>]|\<\+|\>\=|\=\=|\!\=)\s*' \
                            r'([a-z]*[A-Z]*)*\d*\s*(\&\&|\|\|)\s*([a-z]*[A-Z]*)*\d*\s*([<]|[>]|\<\+|\>\=|\=\=|\!\=)' \
                            r'\s*([a-z]*[A-Z]*)*\d*\s*\)\{.*?\}'
        if re.search(pattern_get_else_if, string):
            else_if_str = re.search(pattern_get_else_if, string).group()
            else_if_contents = get_contents(else_if_str)
            verifiy_statement_str = verify_statement(else_if_contents, route)
            print_route(route)
            print("BEFORE:", string)
            string = re.sub(pattern_get_else_if, "", string)
            print("AFTER:", string)
        else:
            compile_error("incorrect else if declaration")

    return string


# PURPOSE: verify if declaration and code block
def verify_if(string, route):
    route += "-->IF"
    print_route(route)

    # finds if(
    pattern_find_if = r'\s*\bif\b\s*\('
    while re.search(pattern_find_if, string):
        # finds all if declarations and corresponding code block
        pattern_get_if = r'\s*\bif\b\s*\((([a-z]*[A-Z]*)*|\d*)\s*([<]|[>]|\<\+|\>\=|\=\=|\!\=)\s*' \
                        r'(\d*|([a-z]*[A-Z]*)*)\s*\)\s*[{].*?[}]|' \
                        r'\s*\bif\b\s*\(\s*([a-z]*[A-Z]*)*\d*\s*([<]|[>]|\<\+|\>\=|\=\=|\!\=)\s*' \
                        r'([a-z]*[A-Z]*)*\d*\s*(\&\&|\|\|)\s*([a-z]*[A-Z]*)*\d*\s*([<]|[>]|\<\+|\>\=|\=\=|\!\=)' \
                        r'\s*([a-z]*[A-Z]*)*\d*\s*\)\{.*?\}'
        if re.search(pattern_get_if, string):
            if_str = re.search(pattern_get_if, string).group()
            if_contents = get_contents(if_str)
            verify_statement_str = verify_statement(if_contents, route)
            print_route(route)
            print("BEFORE:", string)
            string = re.sub(pattern_get_if, "", string)
            print("AFTER:", string)
        else:
            compile_error("incorrect if declaration")
    return string


# PURPOSE: verify else declaration and code block
def verify_else(string, route):
    route += "-->ELSE"
    print_route(route)

    # finds else{
    pattern_find_else = r'\s*\belse\b\s*{'
    while re.search(pattern_find_else, string):
        # finds else declaration and corresponding code block
        pattern_get_else = r'\s*\belse\b\s*{.*?}'
        if re.search(pattern_get_else, string):
            else_str = re.search(pattern_get_else, string).group()
            else_contents = get_contents(else_str)
            verify_statement_str = verify_statement(else_contents, route)
            print_route(route)
            print("BEFORE:", string)
            string = re.sub(pattern_get_else, "", string)
            print("AFTER:", string)
        else:
            compile_error("incorrect else declaration")

    return string


# PURPOSE: calls methods that verify statements
def verify_statement(string, route):
    string = remove_keys(string)
    string = verify_boolean(string, route)
    string = verify_integer(string, route)
    string = verify_string(string, route)
    string = verify_print(string, route)
    string = verify_scanner(string, route)
    string = verify_object(string, route)

    return string


# PURPOSE: checks for keywords as variable names
def remove_keys(string):
    pattern_keys = r'(\bString\b|\bint\b|\bboolean\b)\s*(\bString\b|\bint\b|\bboolean\b)\;'
    if re.search(pattern_keys, string):
        compile_error("you cannot have key words as variable names")
    else:
        return string


# PURPOSE: verufy boolean statements
def verify_boolean(string, route):
    route += "-->BOOLEAN"
    print_route(route)

    # finds boolean statements
    pattern_get_bool = r'\s*\bboolean\b\s([A-Z]*[a-z]*)*\s*=\s*(\bfalse\b|\btrue\b)\s*\;|' \
                       r' ([A-Z]*[a-z]*)*\s=\s*(\btrue\b|\bfalse\b)\s*\;'
    if re.search(pattern_get_bool, string):
        print("BEFORE:", string)
        string = re.sub(pattern_get_bool, "", string)
        print("AFTER:", string)

    return string


# PURPOSE: verify integer statements
def verify_integer(string, route):
    route += "-->INTEGER"
    print_route(route)

    # all of these get the various types of integer statements
    pattern_get_int_1 = r'(\bpublic\b|\bprivate\b|\bprotected\b)*\s+\bint\b\s*([a-z]*[A-Z]*)*\s*\;|' \
                        r'(\bpublic\b|\bprivate\b|\bprotected\b)*\s+\bint\b\s*([a-z]*[A-Z]*)*\s*\=\s*\d*\;|' \
                        r'(\bpublic\b|\bprivate\b|\bprotected\b)*\s+\bint\b\s*([a-z]*[A-Z]*)*\s*\=\s*([a-z]*[A-Z]*)*\;'

    pattern_get_int_2 = r'(\bpublic\b|\bprivate\b|\bprotected\b)*\s+\bint\b\s*([a-z]*[A-Z]*)*\s*\=\s*([a-z]*[A-Z]*)*\s*(\+|\-|\*|\\)\s*([a-z]*[A-Z]*)*\;|' \
                        r'(\bpublic\b|\bprivate\b|\bprotected\b)*\s+\bint\b\s*(\d*([a-z]*[A-Z]*)*)\s*\=\s*\d*\s*(\+|\-|\*|\\)\s*(\d*([a-z]*[A-Z]*)*)\;|' \
                        r'(\bpublic\b|\bprivate\b|\bprotected\b)*\s+\bint\b\s*([a-z]*[A-Z]*)*\s*\=\s*(\d*|([a-z]*[A-Z]*)*)\s*(\+|\-|\*|\\)\s*(\d*|([a-z]*[A-Z]*)*)\;'

    pattern_get_int_3 = r'([a-z]*[A-Z]*)*\s*\=\s*\d*\s*(\+|\-|\*|\\)\s*\d*\;|' \
                        r'([a-z]*[A-Z]*)*\s*\=\s*([a-z]*[A-Z]*)*\;|' \
                        r'([a-z]*[A-Z]*)*\s*\=\s*([a-z]*[A-Z]*)*\s*(\-|\=|\*|\\)\s*([a-z]*[A-Z]*)*\;|' \
                        r'([a-z]*[A-Z]*)*\s*\=\s*([a-z]*[A-Z]*)*\s*(\-|\+|\*|\\)\s*\d*\;|' \
                        r'([A-Z]*[a-z]*)*\s*(\+\+|\-\-)\;|' \
                        r'([a-z]*[A-Z]*)*\s*\=\s*\d*\;'
    if re.search(pattern_get_int_1, string) or re.search(pattern_get_int_2, string) or re.search(pattern_get_int_3, string):
        print("BEFORE:", string)
        string = re.sub(pattern_get_int_1, "", string)
        string = re.sub(pattern_get_int_2, "", string)
        string = re.sub(pattern_get_int_3, "", string)
        print("AFTER:", string)

    return string


# PURPOSE: verify String statements
def verify_string(string, route):
    route += "-->STRING"
    print_route(route)

    # finds all of teh various String statements
    pattern_get_string_1 = r'(\bpublic\b|\bprivate\b|\bprotected\b)*\s+(\bString\b)*\s*([A-Z]*[a-z]*)*\s=\s*\".*\"\s*\;|' \
                           r'(\bpublic\b|\bprivate\b|\bprotected\b)*\s+(\bString\b)*\s*([A-Z]*[a-z]*)*\;'
    pattern_get_string_2 = r'(\bpublic\b|\bprivate\b|\bprotected\b)*\s+(\bString\b)*\s*([A-Z]*[a-z]*)*\s\=\s*(\".*\"|([A-Z]*[a-z]*)*)' \
                           r'\s*\+\s*(\".*\"|([A-Z]*[a-z]*))\s+\+\s+(\".*\"|([A-Z]*[a-z]*)*)\;|' \
                           r'(\bpublic\b|\bprivate\b|\bprotected\b)*\s+(\bString\b)*\s*([A-Z]*[a-z]*)*\s=\s*([A-Z]*[a-z]*)*\s*\+\s*\".*\"\;' \
                           r'(\bpublic\b|\bprivate\b|\bprotected\b)*\s+(\bString\b)*\s*([A-Z]*[a-z]*)*\s*\=\s*\d*\s*\+\s*\".*\"\;|' \
                           r'(\bpublic\b|\bprivate\b|\bprotected\b)*\s+(\bString\b)*\s*([A-Z]*[a-z]*)*\s=\s*\".*\"\s*\+\s*\d*\;'
    if re.search(pattern_get_string_1, string) or re.search(pattern_get_string_2, string):
        print("BEFORE:", string)
        string = re.sub(pattern_get_string_1, "", string)
        string = re.sub(pattern_get_string_2, "", string)
        print("AFTER:", string)

    return string


# PURPOSE: verify print statements
def verify_print(string, route):
    route += "-->PRINT"
    print_route(route)

    # gets print statements
    pattern_get_print = r'\s*\bSystem\b[.]\bout\b[.](\bprint\b|\bprintln\b)\s*\(.*?\)\;'
    if re.search(pattern_get_print, string):
        print("BEFORE:", string)
        string = re.sub(pattern_get_print, " ", string)
        print("AFTER:", string)

    return string


# PURPOSE: rverify Scanner statements
def verify_scanner(string, route):
    route += "-->SCANNER"
    print_route(route)

    # gets create Scanner object
    pattern_get_scan = r'\s*\bScanner\b\s+([a-z]*[A-Z]*)*\s+\=\s+\bnew\b\s+\bScanner\b\(\bSystem\.in\b\)\;'
    # gets assigning input using Scanner object
    pattern_get_scan_2 = r'\s*(\bString\b|\bint\b)\s+([a-z]*[A-Z]*)*\s+\=\s+\bsc\b\.(\bnext\b|\bnextInt\b)\(\)\;'
    if re.search(pattern_get_scan, string) or re.search(pattern_get_scan_2, string):
        print("BEFORE:", string)
        string = re.sub(pattern_get_scan_2, "", string)
        string = re.sub(pattern_get_scan, " ", string)
        print("AFTER:", string)

    return string


# PURPOSE: verify object statments
def verify_object(string, route):
    route += "-->OBJECT"
    print_route(route)

    # gets creating new object
    pattern_get_class_decl = r'\s*(\bpublic\b|\bprivate\b|\bprotected\b)*\s*[A-Z]+[a-z]*\s+([a-z]*[A-Z]*)*\s+\=\s+\bnew\b\s+[A-Z]+[a-z]*\((([a-z]*[A-Z]*)*\s*\,*)*\)\;'

    # gets calling object method
    pattern_get_class_decl_2 = r'\s*(\bpublic\b|\bprivate\b|\bprotected\b)*\s*([a-z]*[A-Z]*)*\.([a-z]*[A-Z]*)*\((([a-z]*[A-Z]*)*\s*\,*)*\)\;'
    if re.search(pattern_get_class_decl, string) or re.search(pattern_get_class_decl_2, string):
        print("BEFORE:", string)
        string = re.sub(pattern_get_class_decl, "", string)
        string = re.sub(pattern_get_class_decl_2, "", string)
        print("AFTER:", string)

    return string


def main():
    program_str = get_program_string()
    sanitized_program_str = sanitize(program_str)
    verified_porgram_str = verify_class(sanitized_program_str)
    if verified_porgram_str == "":
        print("\n**********************************************\n")
        print("\tprogram VERIFIED")
        print("\n**********************************************\n")
    else:
        compile_error("program NOT VERIFIED")

main()