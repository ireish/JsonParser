from Parser import Parser
import sys
import os

def main():
    if len(sys.argv) < 2:
        print("Please provide a filename as an argument.")
        return

    filename = sys.argv[1]
    if not os.path.isfile(filename):
        print(f"File '{filename}' does not exist.")
        return

    parser = Parser()
    try:
        with open(filename, 'r') as file:
            data = file.read()
            parsed_data = parser.parse_json(data)
            print(parsed_data)
    except Exception as e:
        print(f"Error parsing JSON: {str(e)}")

if __name__ == "__main__":
    main()
    
    
