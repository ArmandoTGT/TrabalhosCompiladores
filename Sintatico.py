import pickle
import sys
with open('saida_lexico.pkl', 'rb') as f:
   entradas = pickle.load(f)

tokens = []
classificacao = []
linhas = []
indentificadores = []
valida_tipo = []
parenteses = 0

for entrada in entradas:
    tokens.append(entrada[0])
    classificacao.append(entrada[1])
    linhas.append(entrada[2])

def tiraIndentAteMarca():
    while(indentificadores[0][0] != "$"):
        indentificadores.pop(0)
    indentificadores.pop(0)

def botaIndent(entrada):
    indentificadores.insert(0, entrada)

def checaSeIndentPodeSerDeclarado(checando):
    indents = []

    for el in indentificadores:
        if(el[0] == "$"):
            break
        else:
            indents.append(el[0])

    if(indents.__contains__(checando)):
        print("Indentificador declarada anteriormente nesse escopo", linhas[0])
        sys.exit(0)

def checaSeIndentExisteERetorna(checando):

    for el in indentificadores:
        if(el[0] == checando):
            return el

    print("Identificador não existe", linhas[0])
    sys.exit(0)

#==========================#
#====VALIDAÇÃO DE TIPOS====#
#==========================#

#Função que adiciona o token na variável valida_tipo
def addTipoNaLista(token):
    global valida_tipo

    #print("Valor:", token)
    valida_tipo.append(token)

#Função que faz a verificação dos tokens presentes na expressão criada
#na valida_tipo
def verificaTipos(expressaoArr):

    expressaoTipada = expressaoArr.copy()
    valores_to_jump = [":=", "+", "-", "*", "/", "=", "<", ">", "<=", ">=", "<>", ":", ",", "and", "or"]

    count = 0
    sizeArrInitial = len(expressaoArr)

    parentese_open = False
    parentese_expression = []

    while(count != sizeArrInitial):

        if ((parentese_open) & (expressaoTipada[count] == "(")):
            del expressaoTipada[count]
            sizeArrInitial -= 1
            continue
        else:

            if (expressaoTipada[count].isdigit()):
                value = [expressaoTipada[count], "integer"]
            elif (expressaoTipada[count].replace('.','',1).isdigit()):
                value = [expressaoTipada[count], "real"]
            elif ((expressaoTipada[count] == "true") | (expressaoTipada[count] == "false")):
                value = [expressaoTipada[count], "boolean"]
            else:

                if (expressaoTipada[count] == "("):

                    parentese_open = True
                    del expressaoTipada[count]
                    sizeArrInitial -= 1
                    continue

                elif(expressaoTipada[count] == ")"):

                    if (parentese_open):
                        parentese_open = False
                        value = validaExpressao(parentese_expression)
                        expressaoTipada[count] = value
                        parentese_expression = []
                        count += 1

                        continue
                    else:
                        del expressaoTipada[count]
                        sizeArrInitial -= 1
                        continue

                if (count >= sizeArrInitial):
                    break

                if(expressaoTipada[count] in valores_to_jump):

                    if parentese_open:
                        parentese_expression.append(expressaoTipada[count])
                        del expressaoTipada[count]
                        sizeArrInitial -= 1
                    else:
                        count += 1

                    continue

                value = checaSeIndentExisteERetorna(expressaoTipada[count])

        if parentese_open:
            parentese_expression.append(value[1])
            del expressaoTipada[count]
            sizeArrInitial -= 1
        else:
            expressaoTipada[count] = value[1]

            count += 1

    final = validaExpressao(expressaoTipada)

    return expressaoTipada, final

#Função que faz a validação dos tipos em relação a atribuição e parênteses
def validaExpressao(expressaoTipadaArr):

    expressaoValidada = expressaoTipadaArr.copy()
    validador = []

    variavel_atribuida = ""

    simbolos_operacionais = ["+", "-", "*", "/"]
    simb_operacional = False

    simbolos_logicos = ["=", "<", ">", "<=", ">=", "<>", "and", "or"]
    simb_logico = False

    simbolos_and_or = ["and", "or"]
    simb_and_or = False

    boolean_final = False

    count = 0
    sizeArrInitial = len(expressaoValidada)

    while(count != sizeArrInitial):

        if (expressaoValidada[count] == ":="):
            variavel_atribuida = expressaoValidada[count-1]

            validador = []
            count += 1

            continue

        else:

            if ((expressaoValidada[count] == "procedure") | (expressaoValidada[count] == "function")):
                return "procedimento"

            if ((expressaoValidada[count] in simbolos_logicos) & (not simb_logico)):
                simb_logico = True
                if (expressaoValidada[count] in simbolos_and_or):
                    simb_and_or = True

            if ((simb_logico) & (not simb_and_or)):
                validador = ["boolean"]
            else:

                if((expressaoValidada[count] in simbolos_operacionais) | (expressaoValidada[count] in simbolos_and_or)):
                    count += 1
                    continue

                validador.append(expressaoValidada[count])

        count += 1

    final_value = ""

    #Vamos fazer a verificação dos valores na tabela de valores válidos
    #Caso a variável que vai receber os valores das opeçãoes seja integer nós vamos realizar um determinado procedimento
    if (variavel_atribuida == "integer"):
        count = 0
        sizeValidador = len(validador)

        while(count != sizeValidador):
            atribuicoesValidasInteger = [["integer","integer"], ["integer","real"], ["real","real"]]

            if (validador[count] == "integer"):
                del validador[count]
                sizeValidador -= 1

                if (count >= sizeValidador):
                    final_value = "integer"
                    break

                if((validador[count] == "integer") | (validador[count] == "real")):
                    del validador[count]
                    sizeValidador -= 1

                    if (count >= sizeValidador):
                        final_value = "integer"
                        break

                    for value in validador:
                        if((validador[count] == "integer") | (validador[count] == "real")):
                            del validador[count]
                            final_value = "integer"
                            sizeValidador -= 1
                            continue
                        else:
                            print("Erro Operação Relacional possui um tipo inválido", linhas[0])
                            sys.exit(0)

            elif (validador[count] == "real"):
                del validador[count]
                sizeValidador -= 1

                if (count >= sizeValidador):
                    print("Erro Esperado 'integer' recebido 'real'", linhas[0])
                    sys.exit(0)

                if(validador[count] == "real"):
                    del validador[count]
                    sizeValidador -= 1

                    if (count >= sizeValidador):
                        final_value = "integer"
                        break

                    for value in validador:
                        if((validador[count] == "integer") | (validador[count] == "real")):
                            del validador[count]
                            final_value = "integer"
                            sizeValidador -= 1
                            continue
                        else:
                            print("Erro Operação Relacional possui um tipo inválido", linhas[0])
                            sys.exit(0)

                else:
                    print("Erro Operação não possui um tipo válido", linhas[0])
                    sys.exit(0)
            else:
                print("Erro Operação não possui um tipo válido", linhas[0])
                sys.exit(0)

            count += 1

    elif (variavel_atribuida == "real"):
        count = 0
        sizeValidador = len(validador)

        while(count != sizeValidador):
            atribuicoesValidasReal = [["integer","real"], ["real","real"]]

            if((validador[count] == "integer") | (validador[count] == "real")):
                del validador[count]
                sizeValidador -= 1

                if (count >= sizeValidador):
                    final_value = "real"
                    break

                if(validador[count] == "real"):
                    del validador[count]
                    sizeValidador -= 1

                    if (count >= sizeValidador):
                        final_value = "real"
                        break

                    for value in validador:
                        if((validador[count] == "integer") | (validador[count] == "real")):
                            del validador[count]
                            final_value = "real"
                            sizeValidador -= 1
                            continue
                        else:
                            print("Erro Operação Relacional possui um tipo inválido", linhas[0])
                            sys.exit(0)

                else:
                    print("Erro Operação não possui um tipo válido", linhas[0])
                    sys.exit(0)
            else:
                print("Erro Operação não possui um tipo válido", linhas[0])
                sys.exit(0)

            count += 1
    elif (variavel_atribuida == "boolean"):
        if (validador[0] != "boolean"):
            print("Tipo Esperado Boolean", linhas[0])
            sys.exit(0)
        else:
            final_value = "boolean"
    else:
        count = 0
        sizeValidador = len(validador)

        realIn = False
        for value in validador:

            if (simb_and_or):
                if (value != "boolean"):
                    print("Tipo esperado boolean", linhas[0])
                    sys.exit(0)
                else:
                    final_value = "boolean"

            else:
                if (value == "boolean"):

                    if ((simb_logico) | (len(validador) == 1)):
                        final_value = "boolean"
                        break
                    else:
                        print("Tipo esperado boolean", linhas[0])
                        sys.exit(0)

                if ((value == "integer") & (not realIn)):
                    final_value = "integer"
                    continue

                elif ((value == "real")):
                    final_value = "real"
                    realIn = True
                    continue
                else:
                    print("Tipo não identificado", linhas[0])
                    sys.exit(0)

    return final_value
#==========================#

def retiraPrimeiroLista():

    global tokens
    global classificacao
    global linhas
    tokens = tokens[1:]
    classificacao = classificacao[1:]
    linhas = linhas[1:]

def botaParenteses():

    global parenteses
    parenteses += 1

def tiraParenteses():

    global parenteses
    parenteses -= 1

def declaraVars():
    aux = []
    while(True):
        if (classificacao[0] != "Identificador"):
            print("Erro de Sintaxe: indentificador esperado", linhas[0])
            sys.exit(0)

        if (aux.__contains__(tokens[0])):
            print("Indentificador ja utilizada nessa mesma linha", linhas[0])
            sys.exit(0)
        checaSeIndentPodeSerDeclarado(tokens[0])

        aux.append(tokens[0])
        retiraPrimeiroLista()

        if(tokens[0] == ","):
            retiraPrimeiroLista()
            continue
        break

    if (tokens[0] != ":"):
        print("Erro de Sintaxe: delimitador : esperado", linhas[0])
        sys.exit(0)

    retiraPrimeiroLista()

    if (tokens[0] != "integer" and tokens[0] != "real" and tokens[0] != "boolean"):
        print("Erro de Sintaxe: declaração de tipo esperado", linhas[0])
        sys.exit(0)

    for indet in aux:
        botaIndent([indet, tokens[0]])

    retiraPrimeiroLista()

    if (tokens[0] != ";"):
        print("Erro de Sintaxe: delimitado ; esperado cod:1", linhas[0])
        sys.exit(0)

    aux = []
    retiraPrimeiroLista()

    if (classificacao[0] == "Identificador"):
        declaraVars()

def expressao_relacional():

    expressao_sinal()

def expressao_sinal():
    if(tokens[0] == "+" or tokens[0] == "-"):
        #Token para Validação
        addTipoNaLista(tokens[0])
        #-------------------

        retiraPrimeiroLista()
        expressao_termo()
    else:
        expressao_termo()

def expressao_termo():

    expressao_fator()

def expressao_fator():

    if(classificacao[0] == "Identificador"):

        #Token para Validação
        addTipoNaLista(tokens[0])
        #-------------------

        retiraPrimeiroLista()
        if(tokens[0] == "("):
            retiraPrimeiroLista()
            listaParametros()

    elif(tokens[0] == "("):

        #Token para Validação
        addTipoNaLista(tokens[0])
        #-------------------

        retiraPrimeiroLista()
        botaParenteses()
        expressao_relacional()


    elif(tokens[0] == "true" or tokens[0] == "false"):

        #Token para Validação
        addTipoNaLista(tokens[0])
        #-------------------

        retiraPrimeiroLista()

    elif(tokens[0] == "not"):

        #Token para Validação
        addTipoNaLista(tokens[0])
        #-------------------

        retiraPrimeiroLista()
        expressao_fator()

    elif(classificacao[0] == "Numero Inteiro" or classificacao[0] == "Numero real"):

        #Token para Validação
        addTipoNaLista(tokens[0])
        #-------------------

        retiraPrimeiroLista()

    else:
        print("Erro de Sintaxe: expressão desconhecida", linhas[0])
        sys.exit(0)

    if(classificacao[0] == "Relacional"):

        #Token para Validação
        addTipoNaLista(tokens[0])
        #-------------------

        retiraPrimeiroLista()
        expressao_relacional()

    elif(classificacao[0] == "Operacional"):

        #Token para Validação
        addTipoNaLista(tokens[0])
        #-------------------

        retiraPrimeiroLista()
        expressao_sinal()

    elif(classificacao[0] == "Multiplicador"):

        #Token para Validação
        addTipoNaLista(tokens[0])
        #-------------------

        retiraPrimeiroLista()
        expressao_termo()

    if(tokens[0] == ")" and parenteses > 0):

        #Token para Validação
        addTipoNaLista(tokens[0])
        #-------------------

        retiraPrimeiroLista()
        tiraParenteses()

def listaParametros():

    while(True):
        expressao_relacional()

        if(parenteses != 0):
            print("Erro de Sintaxe: erro nos parenteses", linhas[0])
            sys.exit(0)
        if(tokens[0] == ")"):
            retiraPrimeiroLista()
            break
        elif(tokens[0] == ","):
            retiraPrimeiroLista()
            continue
        else:
            print("Erro de Sintaxe: passagem de parametro errada", linhas[0])
            sys.exit(0)

def comando():
    global valida_tipo

    expressaoTipadaFinal, final = verificaTipos(valida_tipo)

    #Validação da Recursão para casos em Branco
    if (len(valida_tipo) != 0):
        print("\n\n\n===========================================")
        print("Expressao Inicial:", valida_tipo, "\n")
        print("Expressao Tipada Final:", expressaoTipadaFinal, "\n")
        print("Resultado:", final)
        print("===========================================\n\n\n")

    valida_tipo = []

    if(classificacao[0] == "Identificador"):

        #Token para Validação
        addTipoNaLista(tokens[0])
        #-------------------

        retiraPrimeiroLista()
        if(tokens[0] == ":="):

            #Token para Validação
            addTipoNaLista(tokens[0])
            #-------------------

            retiraPrimeiroLista()
            expressao_relacional()
            if(parenteses != 0):
                print("Erro de Sintaxe: erro nos parenteses cod:1", linhas[0])
                sys.exit(0)
        elif(tokens[0] == "("):

            #Token para Validação
            addTipoNaLista(tokens[0])
            #-------------------

            retiraPrimeiroLista()
            listaParametros()

        if (tokens[0] != ";"):
            print("Erro de Sintaxe: ; esperado cod:2", linhas[0])
            sys.exit(0)

        retiraPrimeiroLista()

    #Estou assumindo qu o begin filho, o if e o while não precisam de ; no final

    elif(tokens[0] == "begin"):
        retiraPrimeiroLista()

        comandoComposto()

        retiraPrimeiroLista()

    elif(tokens[0] == "if"):
        retiraPrimeiroLista()

        expressao_relacional()

        if (tokens[0] != "then"):
            print("Erro de Sintaxe: 'then' esperado depois do if", linhas[0])
            sys.exit(0)
        retiraPrimeiroLista()

        comando()#Chegar isso, de acordo com a linguagem, aqui só pode ter um comando mesmo, checar com o professor

        if(tokens[0] == "else"):
            retiraPrimeiroLista()

            comando()

    elif(tokens[0] == "while"):
        retiraPrimeiroLista()

        expressao_relacional()
        if (tokens[0] != "do"):
            print("Erro de Sintaxe: 'do' esperado depois do while", linhas[0])
            sys.exit(0)
        retiraPrimeiroLista()

        comando()#Chegar isso, de acordo com a linguagem, aqui só pode ter um comando mesmo, checar com o professor

    expressaoTipadaFinal, final = verificaTipos(valida_tipo)

    #Validação da Recursão para casos em Branco
    if (len(valida_tipo) != 0):
        print("\n\n\n===========================================")
        print("Expressao Inicial:", valida_tipo, "\n")
        print("Expressao Tipada Final:", expressaoTipadaFinal, "\n")
        print("Resultado:", final)
        print("===========================================\n\n\n")

    valida_tipo = []

def comandoComposto():
    global valida_tipo

    valida_tipo = []
    #print(tokens)

    if (tokens[0] != "end"):
        comando()
        #print("Valor:", tokens[0])
        #valida_tipo.append(tokens[0])
        comandoComposto()

def argumentos():

    auxArg = []
    while(True):
        if (classificacao[0] != "Identificador"):
            print("Erro de Sintaxe: indentificador esperado", linhas[0])
            sys.exit(0)



        if (auxArg.__contains__(tokens[0])):
            print("Indentificador ja utilizada nessa mesma linha", linhas[0])
            sys.exit(0)
        checaSeIndentPodeSerDeclarado(tokens[0])

        auxArg.append(tokens[0])
        retiraPrimeiroLista()

        if(tokens[0] == ","):
            retiraPrimeiroLista()
            continue
        break

    if (tokens[0] != ":"):
        print("Erro de Sintaxe: delimitado : esperado", linhas[0])
        sys.exit(0)

    retiraPrimeiroLista()

    if (tokens[0] != "integer" and tokens[0] != "real" and tokens[0] != "boolean"):
        print("Erro de Sintaxe: declaração de tipo esperado", linhas[0])
        sys.exit(0)

    for indet in auxArg:
        botaIndent([indet, tokens[0]])

    retiraPrimeiroLista()

    auxArg = []
    if (tokens[0] == ";"):
        retiraPrimeiroLista()
        argumentos()

    if(tokens[0] != ")"):
        print("Erro de Sintaxe: parenteses aberto de não fechado", linhas[0])
        sys.exit(0)

    retiraPrimeiroLista()

def subProgramas():

    if (classificacao[0] != "Identificador"):
        print("Erro de Sintaxe: depois de 'procedure' deve vim um indentificador", linhas[0])
        sys.exit(0)

    checaSeIndentPodeSerDeclarado(tokens[0])

    botaIndent([tokens[0], "procedure"])
    botaIndent(["$", "mark"])
    retiraPrimeiroLista()

    if(tokens[0] == "("):
        retiraPrimeiroLista()
        argumentos()

    if (tokens[0] != ";"):
        print("Erro de Sintaxe: ; esperado cod:3", linhas[0])
        sys.exit(0)

    retiraPrimeiroLista()
    corpoPrograma()
    tiraIndentAteMarca()

def corpoPrograma():
    #Caso queria deixar com declaração de vars em todo lugar só voltar pra forma de shile de antes, procure nas versões do git
    if(tokens[0] == "var"):
        retiraPrimeiroLista()
        declaraVars()
    while(True):
        if(tokens[0] == "procedure"):
            retiraPrimeiroLista()
            subProgramas()
            #são realmente como de fossem programas completos, adicionando os argumentos
        else:
            break
    if(tokens[0] == "begin"):
        retiraPrimeiroLista()
        comandoComposto()
        retiraPrimeiroLista()
    else:
        print("Erro de Sintaxe: comando não reconhecido", linhas[0])
        sys.exit(0)

def programa():

    if (tokens[0] != "program"):
        print("Erro de Sintaxe: 'program' deve se a primeira palavra", linhas[0])
        sys.exit(0)

    retiraPrimeiroLista()

    if (classificacao[0] != "Identificador"):
        print("Erro de Sintaxe: depois de 'program' deve vim um indentificador", linhas[0])
        sys.exit(0)

    botaIndent([tokens[0], "program"])
    retiraPrimeiroLista()

    if (tokens[0] != ";"):
        print("Erro de Sintaxe: ; esperado cod:3", linhas[0])
        sys.exit(0)

    retiraPrimeiroLista()

    corpoPrograma()


programa()
retiraPrimeiroLista()
print(tokens)
print(indentificadores)
