import pickle
import sys
with open('saida_lexico.pkl', 'rb') as f:
   entradas = pickle.load(f)

tokens = []
classificacao = []
linhas = []
for entrada in entradas:
    tokens.append(entrada[0])
    classificacao.append(entrada[1])
    linhas.append(entrada[2])

def retiraPrimeiroLista():
    global tokens
    global classificacao
    global linhas 
    tokens = tokens[1:]
    classificacao = classificacao[1:]
    linhas = linhas[1:]

def declaraVars():
    if (classificacao[0] != "Identificador"):
        print("Erro de Sintaxe: indentificador esperado", linhas[0])
        sys.exit(0)

    retiraPrimeiroLista()

    if (tokens[0] != ":"):
        print("Erro de Sintaxe: delimitado : esperado", linhas[0])
        sys.exit(0)

    retiraPrimeiroLista()        

    if (tokens[0] != "integer" and tokens[0] != "real" and tokens[0] != "boolean"):
        print("Erro de Sintaxe: declaração de tipo esperado", linhas[0])
        sys.exit(0)

    retiraPrimeiroLista()  

    if (tokens[0] != ";"):
        print("Erro de Sintaxe: delimitado ; esperado", linhas[0])
        sys.exit(0)

    retiraPrimeiroLista() 

    if (classificacao[0] == "Identificador"):
        declaraVars()

def expressao_relacional():


def expressao_sinal():
    if(tokens[0] == "+" or tokens[0] == "-"):
        retiraPrimeiroLista()
        expressao_termo()

def expressao_termo():
    

def expressao_fator():
    if(classificacao[0] == "Identificador"):
        retiraPrimeiroLista()
        if(tokens[0] == "("):

    elif(tokens[0] == "("):
        retiraPrimeiroLista()
    
    elif(tokens[0] == "true" or tokens[0] == "false"):
        retiraPrimeiroLista()
    
    elif(tokens[0] == "not"):
        retiraPrimeiroLista()
        expressao_simples()

    elif(classificacao[0] == "Numero Inteiro" or classificacao[0] == "Numero real"):
        retiraPrimeiroLista()
    
    else:
        print("Erro de Sintaxe: expressão desconhecida", linhas[0])
        sys.exit(0)


def listaParametros():


def comando():
    if(classificacao[0] == "Identificador"):
        retiraPrimeiroLista()
        if(tokens[0] == ":="):
            retiraPrimeiroLista()
            expressao()
        if(tokens[0] == "("):
            retiraPrimeiroLista()
            listaParametros()


def comandoComposto():
    
    comando()

    if (tokens[0] != "end"):       
        comandoComposto()


def programa():
    if (tokens[0] != "program"):
        print("Erro de Sintaxe: 'program' deve se a primeira palavra", linhas[0])
        sys.exit(0)

    retiraPrimeiroLista()

    if (classificacao[0] != "Identificador"):
        print("Erro de Sintaxe: depois de 'program' deve vim um indentificador", linhas[0])
        sys.exit(0)

    retiraPrimeiroLista()

    if (tokens[0] != ";"):
        print("Erro de Sintaxe: depois de 'program' deve vim um indentificador", linhas[0])
        sys.exit(0)

    retiraPrimeiroLista()

    while(tokens[0] != "."):
        if(tokens[0] == "var"):
            retiraPrimeiroLista()
            declaraVars()
        if(tokens[0] == "procedure"):
            retiraPrimeiroLista()
            #subProgramas()
        if(tokens[0] == "begin"):
            retiraPrimeiroLista()
            print("Chegou")
            comandoComposto()
        else:
            print("Erro de Sintaxe: comando não reconhecido", linhas[0])
            sys.exit(0)

programa()
print(tokens)