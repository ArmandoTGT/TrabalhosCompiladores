import pickle
import sys
with open('saida_lexico.pkl', 'rb') as f:
   entradas = pickle.load(f)

tokens = []
classificacao = []
linhas = []
parenteses = 0
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

def botaParenteses():

    global parenteses
    parenteses += 1

def tiraParenteses():

    global parenteses
    parenteses -= 1

def declaraVars():

    while(True):
        if (classificacao[0] != "Identificador"):
            print("Erro de Sintaxe: indentificador esperado", linhas[0])
            sys.exit(0)

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

    retiraPrimeiroLista()  

    if (tokens[0] != ";"):
        print("Erro de Sintaxe: delimitado ; esperado", linhas[0])
        sys.exit(0)

    retiraPrimeiroLista() 

    if (classificacao[0] == "Identificador"):
        declaraVars()

def expressao_relacional():

    expressao_sinal()

def expressao_sinal():   

    if(tokens[0] == "+" or tokens[0] == "-"):
        retiraPrimeiroLista()
        expressao_termo()
    else:
        expressao_termo()

def expressao_termo():

    expressao_fator()

def expressao_fator():

    if(classificacao[0] == "Identificador"):
        retiraPrimeiroLista()
        if(tokens[0] == "("):
            retiraPrimeiroLista()
            listaParametros()

    elif(tokens[0] == "("):
        retiraPrimeiroLista()
        botaParenteses()
        expressao_relacional()
        #Faltando analisar esse caso
    
    elif(tokens[0] == "true" or tokens[0] == "false"):
        retiraPrimeiroLista()
    
    elif(tokens[0] == "not"):
        retiraPrimeiroLista()
        expressao_fator()

    elif(classificacao[0] == "Numero Inteiro" or classificacao[0] == "Numero real"):
        retiraPrimeiroLista()
    
    else:
        print("Erro de Sintaxe: expressão desconhecida", linhas[0])
        sys.exit(0)

    if(classificacao[0] == "Relacional"):
        retiraPrimeiroLista()
        expressao_relacional()

    elif(classificacao[0] == "Operacional"):
        retiraPrimeiroLista()
        expressao_sinal()
    
    elif(classificacao[0] == "Multiplicador"):
        retiraPrimeiroLista()
        expressao_termo()
    
    if(tokens[0] == ")"):
        tiraParenteses()    


def listaParametros():

    while(True):
        expressao_relacional()
        if(parenteses != 0):
            print("Erro de Sintaxe: erro nos parenteses", linhas[0])
            sys.exit(0)
        if(tokens[0] == ")"):
            break
        elif(tokens[0] == ","):
            continue
        else:
            print("Erro de Sintaxe: passagem de parametro errada", linhas[0])
            sys.exit(0)

def comando():

    if(classificacao[0] == "Identificador"):
        retiraPrimeiroLista()
        if(tokens[0] == ":="):
            retiraPrimeiroLista()
            expressao_relacional()
            if(parenteses != 0):
                print("Erro de Sintaxe: erro nos parenteses", linhas[0])
                sys.exit(0)
        if(tokens[0] == "("):
            retiraPrimeiroLista()
            listaParametros()
        
        if (tokens[0] != ";"):
            print("Erro de Sintaxe: ; esperado", linhas[0])
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
            comando()
        
    elif(tokens[0] == "while"):
        retiraPrimeiroLista()
        expressao_relacional()
        if (tokens[0] != "do"):
            print("Erro de Sintaxe: 'do' esperado depois do while", linhas[0])
            sys.exit(0)
        retiraPrimeiroLista()
        comando()#Chegar isso, de acordo com a linguagem, aqui só pode ter um comando mesmo, checar com o professor
    

def comandoComposto():  

    if (tokens[0] != "end"):
        comando()         
        comandoComposto()

def argumentos():

    while(True):
        if (classificacao[0] != "Identificador"):
            print("Erro de Sintaxe: indentificador esperado", linhas[0])
            sys.exit(0)

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

    retiraPrimeiroLista()  

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

    retiraPrimeiroLista()

    if(tokens[0] == "("):
        retiraPrimeiroLista()
        argumentos()

    if (tokens[0] != ";"):
        print("Erro de Sintaxe: ; esperado", linhas[0])
        sys.exit(0)

    retiraPrimeiroLista()
    corpoPrograma()
    
def corpoPrograma():

    while(tokens[0] != "."):
        if(tokens[0] == "var"):
            retiraPrimeiroLista()
            declaraVars()
        if(tokens[0] == "procedure"):
            retiraPrimeiroLista()
            subProgramas()
            #são realmente como de fossem programas completos, adicionando os argumentos
        if(tokens[0] == "begin"):
            retiraPrimeiroLista()            
            comandoComposto()
            retiraPrimeiroLista()
            break                
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

    retiraPrimeiroLista()

    if (tokens[0] != ";"):
        print("Erro de Sintaxe: ; esperado", linhas[0])
        sys.exit(0)

    retiraPrimeiroLista()

    corpoPrograma()

    

programa()
retiraPrimeiroLista()
print(tokens)