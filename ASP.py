class Asp:
    # grammar rules in a form of string:
    #   - @ denotes epsilon
    #   - . denotes empty item = error
    def __init__(self):
        pass

    f = open('input', 'r')
    GRAMMAR = f.read()
    FINAL_RULES = []

    # parse table structure:
    #      REQUIRED IMPLIED FIXED CDATA NMTOKEN IDREF ATTLIST ELEMENT EMPTY ANY PCDATA WORD , | \" ( ) < > ? * + $
    #   A
    #   B
    #   C
    #   D
    #   E
    #   F
    #   G
    #
    #   parse table is represented as a hash table of parse table row indexes
    #   (non terminals + terminals) where each of the hash values is another
    #   hash table with the column indexes as keys and set of terminas and
    #   nonterminals delimited by space for the given rule
    #
    PARSE_TABLE = {}
    ERROR_COUNT = 0
    START = ""

    def initializeParseTable(self):
        rows = filter(None, self.GRAMMAR.split('\n'))
        columns_indexes = filter(None, rows[0].split(' '))
        self.START = rows[1].split(' ')[0]
        for row in rows[1:]:
            columns = row[0:].split(' ')
            self.PARSE_TABLE[columns[0]] = {}
            for idx, column in enumerate(columns[1:]):
                # print(columns[0], columns_indexes[idx], column)
                self.PARSE_TABLE[columns[0]][columns_indexes[idx]] = column

    def analyzeTokens(self, tokens):
        stack = []
        stack.append('$')
        stack.append(self.START)
        position = 0
        token = tokens[position]
        pop = stack[len(stack) - 1]
        while pop is not "$":
            pop = stack[len(stack) - 1]
            print "\n--------------------"
            print "Stack: " + str(stack)
            print "Top of Stack: " + pop
            token = tokens[position]

            if pop not in self.PARSE_TABLE.keys() or pop is "$":
                if token == pop:
                    stack.pop()
                    position += 1
                    print("Top Of Stack equals Token, so we pop Top of Stack and move to another token.")
                elif pop == "@":
                    stack.pop()
                else:
                    print("***** ERROR: No match in Parse Table. *******")
                    self.ERROR_COUNT += 1
                    position, stack = self.recovery(tokens, position, stack)
            else:
                if self.PARSE_TABLE[pop][token] != ".":
                    rules = self.PARSE_TABLE[pop][token].split(';')
                    stack.pop()
                    rule_str = pop + " -> " + self.printRules(rules)
                    self.FINAL_RULES.append(rule_str)
                    print("Match found. Applying rules: " + rule_str)
                    for rule in reversed(rules):
                        stack.append(rule)
                else:
                    print("***** ERROR: No match in Parse Table. *******")
                    self.ERROR_COUNT += 1
                    position, stack = self.recovery(tokens, position, stack)

        print("\nDONE")
        print("\t" + str(self.ERROR_COUNT) + " errors found.")
        if self.ERROR_COUNT == 0:
            print("Las acciones finales son:")
            for rule in self.FINAL_RULES:
                print(rule)

    def recovery(self, tokens, position, stack):
        print("***** RECOVERY:")
        print("Skipping tokens:")
        while tokens[position] != ">" and tokens[position] != "<":
            position += 1
            print("\t" + tokens[position])
        if tokens[position] != "<":
            position += 1

        print("Poping out of stack:")
        topOfStack = stack[len(stack) - 1]
        while topOfStack != 'L':
            print("\t'" + stack.pop())
            topOfStack = stack[len(stack) - 1]

        return position, stack

    def printRules(self, rules):
        line = ""
        for rule in rules:
            line = line + " " + rule
        return line


a = Asp()
a.initializeParseTable()
a.analyzeTokens(['id', '+', 'id', '*', 'id', '$'])
