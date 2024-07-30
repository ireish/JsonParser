tokens = [
    ("CURLY_BRACE_START", "{"),
    ("CURLY_BRACE_END", "}"),
    ("ARRAY_START", "["),
    ("ARRAY_END", "["),
    ("STRING", r'"([^"\\]|\\.)*"'),
    ("NUMBER", r"-?(0|[1-9]\d*)(\.\d+)?([eE][+-]?\d+)?"),
    ("BOOLEAN_TRUE", "true"),
    ("BOOLEAN_FALSE", "false"),
    ("NULL", "null"),
    ("COLON", ":"),
    ("COMMA", ","),
]