reservadas = ["program", "var", "integer", "real", "boolean", "procedure", "begin",
"end", "if", "then", "else", "while", "do", "not", "function"]
relacionais = ["=", "<", ">", "<=", ">=", "<>"]
oparecionais = ["+", "-", "or"]
multiplicativos = ["*", "/", "and"]
delemitadores = [";", ":", "(", ")", ".", ","]
pontosJuntos = [":=", "+", "-", "*", "/", "=", "<", ">", "<=", ">=", "<>", ":", "(", ")", ","]

f = open("entrada.txt", "r")
entrada = f.read()
saida = []

new_token = ""
new_point = ""
line = 1
coment = False
sinal_desconhecido = False
linha_erro_simb = 0
linha_erro_coment = 0

def ClassificaToken( new_token ):
    if new_token.isdigit():
        saida.append([ new_token, "Numero Inteiro", line])
    elif new_token.replace('.','',1).isdigit():
        saida.append([ new_token, "Numero real", line])
    elif reservadas.__contains__(new_token):
        saida.append([ new_token, "Palavra reservada", line])
    elif new_token == "and":
        saida.append([ new_token, "Multiplicador", line])
    elif new_token == "or":
        saida.append([ new_token, "Operacional", line])       
    elif new_token == "true" or new_token == "false":
        saida.append([ new_token, "Booleano", line])
    else:
        saida.append([ new_token, "Identificador", line])

def ClassificaPoint( new_point ):
    if new_point == ":=":
         saida.append([ new_point, "Atribuição", line])
    elif relacionais.__contains__(new_point):
         saida.append([ new_point, "Relacional", line])
    elif oparecionais.__contains__(new_point):
         saida.append([ new_point, "Operacional", line])
    elif multiplicativos.__contains__(new_point):
         saida.append([ new_point, "Multiplicador", line])
    elif delemitadores.__contains__(new_point):
         saida.append([ new_point, "Delimitador", line])
    else:
        sinal_desconhecido = True
        linha_erro_simb = line


for simb in entrada:

    if simb == " ":

        if new_token != "" and not(coment):
            ClassificaToken(new_token)
            new_token = ""

        if new_point != "" and not(coment):
            ClassificaPoint(new_point)
            new_point = ""


    elif simb == "\n" or simb == ";":

        if new_token != "" and not(coment):
            ClassificaToken(new_token)
            new_token = ""

        if new_point != "" and not(coment):
            ClassificaPoint(new_point)
            new_point = ""

        if simb == ";" and not(coment):
            ClassificaPoint(simb)
        elif simb == ";" and coment:
            continue
        else:
            line += 1

    elif simb == "{":

        if new_token != "" and not(coment):
            ClassificaToken(new_token)
            new_token = ""

        if new_point != "" and not(coment):
            ClassificaPoint(new_point)
            new_point = ""

        linha_erro_coment = line
        coment = True


    elif simb == "}" and coment:
        coment = False
        new_token = ""
        new_point = ""

    elif simb == "}" and not(coment):
        string_saida += "ERRO: } " + line + "\n"
        break

    elif not(simb.isalpha()) and not(simb.isdigit()) and simb != "_" and not(coment):

        if simb == "(" or simb == ")":
            if new_token != "":
                ClassificaToken(new_token)
                new_token = ""
            ClassificaPoint(new_point)
            new_point = ""

        new_point += simb

        if new_point == "(" or new_point == ")":
            if new_token != "":
                ClassificaToken(new_token)
                new_token = ""
            ClassificaPoint(new_point)
            new_point = ""

    else:
        if new_point == ".":
            if new_token == "":
                ClassificaPoint(new_point)
                new_point = ""
            new_token += new_point
            new_point = ""
        if(pontosJuntos.__contains__(new_point)):
            if new_token != "":
                ClassificaToken(new_token)
                new_token = ""
            ClassificaPoint(new_point)
            new_point = ""
        new_token += simb


if new_token != "":
    ClassificaToken(new_token)
    new_token = ""

if new_point != "":
    ClassificaPoint(new_point)
    new_point = ""

string_saida = ""
if(coment):
    string_saida += "ERRO: comentario aberto e não fechado, linha " + linha_erro_coment + "\n"
if(sinal_desconhecido):
    string_saida += "ERRO: sinal desconhecido, linha " + linha_erro_simb + "\n"
else:
    for s in saida:
       string_saida += (str(s) + "\n")

arquivo_saida = open("saida_lexico.txt","w")
arquivo_saida.write(string_saida)
arquivo_saida.close()

import pickle
with open('saida_lexico.pkl', 'wb') as f:
    pickle.dump(saida, f)
