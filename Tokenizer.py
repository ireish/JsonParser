from Token import Token

def get_tokens(input: str) -> list:
    tokens = []
    pos = 0
    while pos < len(input):
        ch = input[pos]
        match ch:
            case ' ' | '\n':
                for i in tokens: print(i)
                pos += 1
            case ":":
                tokens.append(Token("COLON", pos, pos))
                pos += 1
            case "{":
                tokens.append(Token("CURLY_BRACE_START", pos, pos))
                pos += 1
            case "}":
                tokens.append(Token("CURLY_BRACE_END", pos, pos))
                pos += 1
            case "[":
                tokens.append(Token("ARRAY_START", pos, pos))
                pos += 1
            case "]":
                tokens.append(Token("ARRAY_END", pos, pos))
                pos += 1
            case '"':
                # skip the first quote
                string_val, length = __parse_string(input, pos + 1)
                tokens.append(Token("STRING", pos, pos + length + 1, string_val))
                pos = (pos + len(string_val) + 1) + 1
            case ',':
                tokens.append(Token("COMMA", pos, pos))
                pos += 1
            case d if str.isdigit(d) or d == '.' or d == "-":
                number, length = __parse_number(input, pos)
                tokens.append(Token("NUMBER", pos, pos + length - 1, number))
                pos += length
            case "t" | "f":
                boolean_val, length = __parse_boolean(input, pos)
                token_name = "BOOLEAN_TRUE" if boolean_val == True else "BOOLEAN_FALSE"
                tokens.append(Token(token_name, pos, pos + length, boolean_val))
                pos += length
            case _:
                null_value, length = __parse_null(input, pos)
                if (null_value == "null"):
                    tokens.append(Token("NULL", pos, pos + 3, None))
                    pos += len("null")
                else:
                    raise Exception(f"Encountered unexpected token at {pos}: {input[pos: pos + 10]}")

    return tokens


def __parse_string(input: str, pos: int):
    string_val = ""
    while (pos < len(input) and input[pos] != '"'):
        string_val += input[pos]
        pos += 1

    if (pos == len(input)):
        raise Exception('Expected STRING_END (") to indicate end of string but found END_OF_INPUT')
    
    return (string_val, len(string_val))

def __parse_boolean(input: str, pos: int):
    if (input[pos: pos + len("True")].casefold() == "true".casefold()):
        return (True, len("True")) 
    
    if (input[pos: pos + len("False")].casefold() == "false".casefold()):
        return (False, len("False"))
    
    raise Exception(f"Found unexpected character at pos: {pos}")

def __parse_number(input: str, pos: int):
    num, decimal, exponent = 0, 0, 0
    num_digits = 0
    sign = 1

    if (input[pos] == '-'):
        sign = -1
        pos += 1
        num_digits += 1

    
    
    while (pos < len(input) and str.isdigit(input[pos])):
        num = num * 10 + int(input[pos])
        num_digits += 1
        pos += 1

    if (pos < len(input) and input[pos] == '.'):
        num_digits += 1
        pos += 1
        cnt = 0
        while (pos < len(input) and str.isdigit(input[pos])):
            decimal = decimal * 10 + int(input[pos])
            pos += 1
            cnt += 1
            num_digits += 1

        decimal = decimal / (10 ** cnt)

    if (pos < len(input) and input[pos] == 'e'):
        num_digits += 1
        pos += 1
        cnt = 0
        while (pos < len(input) and str.isdigit(input[pos])):
            exponent = exponent * 10 + int(input[pos])
            pos += 1
            cnt += 1
            num_digits += 1

    return (sign * (num + decimal) * (10 ** exponent), num_digits)

def __parse_null(input: str, pos: int):
    if (input[pos: pos + len("null")].casefold() == "null".casefold()):
        return ("null", 4)
    else: 
        return (None, 0)

