class Asp:
    # Reglas de la gramatica:
    #   - @ denota epsilon
    #   - . denotes item vacio = error
    def __init__(self):
        pass

    f = open('table_sinc', 'r')
    TABLA = f.read()
    FINAL_RULES = []

    TABLA_PARSEADA = {}
    ERRORES_CONT = 0
    INICIO = ""

    def parsearTabla(self):
        filas = filter(None, self.TABLA.split('\n'))
        columnas_indexadas = filter(None, filas[0].split(' '))
        self.INICIO = filas[1].split(' ')[0]
        for fila in filas[1:]:
            columnas = fila[0:].split(' ')
            self.TABLA_PARSEADA[columnas[0]] = {}
            for idx, column in enumerate(columnas[1:]):
                self.TABLA_PARSEADA[columnas[0]][columnas_indexadas[idx]] = column

    def analizarTokens(self, tokens):
        pila = []
        pila.append('$')
        pila.append(self.INICIO)
        posicion = 0
        token = tokens[posicion]
        pop = pila[-1]
        while pop is not "$":
            pop = pila[-1]
            print "\n--------------------"
            print "Pila: " + str(pila)
            print "Top de la Pila: " + pop
            token = tokens[posicion]

            if pop not in self.TABLA_PARSEADA.keys() or pop is "$":
                if token == pop:
                    pila.pop()
                    posicion += 1
                    print(
                        "Top de la Pila igual al Token, asi que sacamos la parte superior de la pila y pasamos a otro Token.")
                elif pop == "@":
                    pila.pop()
                else:
                    print("***** ERROR: Ningun match en la Tabla Parseada. *******")
                    self.ERRORES_CONT += 1
                    posicion, pila = self.recuperacion(tokens, posicion, pila)
            else:
                if self.TABLA_PARSEADA[pop][token] != "." and self.TABLA_PARSEADA[pop][token] != 'sinc':
                    reglas = self.TABLA_PARSEADA[pop][token].split(';')
                    pila.pop()
                    regla_str = pop + " -> " + self.printRules(reglas)
                    self.FINAL_RULES.append(regla_str)
                    print("Match encontrado. Aplicando reglas: " + regla_str)
                    for regla in reversed(reglas):
                        pila.append(regla)
                else:
                    print("***** ERROR: Ningun match en la Tabla Parseada. *******")
                    self.ERRORES_CONT += 1
                    posicion, pila = self.recuperacion(tokens, posicion, pila)

        print("\nFINALIZADO:")
        print("\t" + str(self.ERRORES_CONT) + " errores encontrados.")
        if self.ERRORES_CONT == 0:
            print("\nLas acciones finales son:")
            for regla in self.FINAL_RULES:
                print(regla)

    def recuperacion(self, tokens, position, stack):
        print("***** RECUPERACION:")
        if (self.TABLA_PARSEADA[stack[-1]][tokens[position]] == '.' or (
                            self.TABLA_PARSEADA[stack[-1]][tokens[position]] == 'sinc' and stack[-1] == self.INICIO and
                        tokens[
                            position] != "$")):
            print "Omitir: " + tokens[position]
            self.tokensEsperados(stack[-1])
            position += 1
        elif (self.TABLA_PARSEADA[stack[-1]][tokens[position]] == 'sinc'):
            print("Sacar de la pila: \t" + stack[-1])
            self.tokensEsperados(stack[-1])
            stack.pop()
        elif ((self.TABLA_PARSEADA[stack[-1]][tokens[position]] != tokens[position])):
            print("Sacar de la pila: \t" + stack[-1])
            self.tokensEsperados(stack[-1])
            stack.pop()
        return position, stack

    def printRules(self, rules):
        line = ""
        for rule in rules:
            line = line + " " + rule
        return line

    def tokensEsperados(self, item):
        print "Se espera uno de estos tokens: "
        for key, value in self.TABLA_PARSEADA[item].iteritems():
            if (value != 'sinc' and value != '.'):
                print "\t\t" + key


entrada = raw_input("Ingrese la cadena de entrada, separando los tokens por espacio: ")
arrayEntrada = entrada.split(" ")
a = Asp()
try:
    a.parsearTabla()
except IndexError as ie:
    print "No se pueden tener una tabla multivalor para un LL(1)"
else:
    a.analizarTokens(arrayEntrada)
# a.analyzeTokens(['id', '+', 'id', '*', 'id', '$'])
# a.analyzeTokens([')', 'id', '*', '+', 'id', '$'])
