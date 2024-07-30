from Tokenizer import Token, get_tokens

class Parser:
    def __init__(self):
        self.curr_pos = 0

    def parse_json(self, input: str):
        tokens = get_tokens(input)
        return self.__parse_tokens(tokens)

    def __parse_tokens(self, tokens: list):
        if (tokens[self.curr_pos].token_type == "CURLY_BRACE_START"):
            self.curr_pos += 1
            parsed_data = self.__parse_object(tokens)
        elif (tokens[self.curr_pos].token_type == "ARRAY_START"):
            self.curr_pos += 1
            parsed_data = self.__parse_array(tokens)
        else:
            raise Exception("Json string should start with '{' or '['")
        
        if (self.curr_pos == len(tokens)):
            return parsed_data
        else:
            raise Exception(f"Expected END_OF_INPUT token at pos: {self.curr_pos} but got {tokens[self.curr_pos]}")

    def __parse_array(self, tokens):
        j_array = []
        while (self.curr_pos < len(tokens) and tokens[self.curr_pos].token_type != "ARRAY_END"):
            j_array.append(self.__parse_value(tokens))
            self.__advance_to_next_or_stop(tokens, "COMMA", "ARRAY_END")

        if (self.curr_pos == len(tokens)):
            raise Exception(f"Expected ARRAY_END at pos: {self.curr_pos} but got END_OF_INPUT")

        self.curr_pos += 1
        return j_array

    def __parse_object(self, tokens):
        j_object = {}
        while (self.curr_pos < len(tokens) and tokens[self.curr_pos].token_type != "CURLY_BRACE_END"):
            key = self.__parse_key(tokens)
            self.__advance_to_next_or_stop(tokens, "COLON")
            value = self.__parse_value(tokens)
            j_object[key] = value

            self.__advance_to_next_or_stop(tokens, "COMMA", "CURLY_BRACE_END")


        if (self.curr_pos == len(tokens)):
            raise Exception(f"Expected CURLY_BRACE_END at pos: {self.curr_pos} but got END_OF_INPUT")

        self.curr_pos += 1
        return j_object

    def __parse_key(self, tokens):
        if (self.curr_pos >= len(tokens)):
            raise Exception(f"Expected STRING Token at pos: {self.curr_pos} but got END_OF_INPUT")

        if (tokens[self.curr_pos].token_type == "STRING"):
            key = tokens[self.curr_pos].value
            self.curr_pos += 1
            return key
        
        raise Exception(f"Expected STRING Token at pos: {self.curr_pos} but got {tokens[self.curr_pos].token_type}")
    
    def __parse_value(self, tokens):
        if (tokens[self.curr_pos].token_type in ["STRING", "NUMBER", "BOOLEAN_TRUE", "BOOLEAN_FALSE", "NULL"]):
            j_value = tokens[self.curr_pos].value
            self.curr_pos += 1
        elif (tokens[self.curr_pos].token_type == "ARRAY_START"):
            self.curr_pos += 1
            j_value = self.__parse_array(tokens)
        elif (tokens[self.curr_pos].token_type == "CURLY_BRACE_START"):
            self.curr_pos += 1
            j_value = self.__parse_object(tokens)
        else:
            raise Exception(f"Encountered unexpected token at pos: {self.curr_pos}")
        
        return j_value

    def __advance_to_next_or_stop(self, tokens, expected_token_type, stop_token = None):
        if (tokens[self.curr_pos].token_type == expected_token_type):
            self.curr_pos += 1
            return
        elif (tokens[self.curr_pos].token_type == stop_token):
            return

        raise Exception(f"Expected {expected_token_type} at pos: {self.curr_pos}")
