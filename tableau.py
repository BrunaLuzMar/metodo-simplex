import matriz
import entrada

def confere_w(z):
    if z == 0:
        return True
    else:
        return False
    
def confere_c(c):
    for i in range(len(c)):
        if c[i] < 0:
            return False
    return True

def confere_b(T, B):
    for varivel_basica in B:
        if T[0][varivel_basica] != 0:
            print(f"Violação da forma canônica! Coluna {varivel_basica} = {T[0][varivel_basica]}")
            return False
    return True

def forma_canonica(T, base):
    for linha in range(1, len(T)):  # para cada restrição
        # Encontra a variável básica desta linha
        for j in base:
            if abs(T[linha][j] - 1.0) < 1e-10:
                # Zerar esta variável na linha 0
                fator = T[0][j]
                for col in range(len(T[0])):
                    T[0][col] -= fator * T[linha][col]
                break

def esolher_variavel_da_base(T):
    b = [linha[-1] for linha in T[1:]]
    for i in b:
        if i == 0:
            # Degeneração
            variavel_entrada = tratar_degeneracao(T)
            return variavel_entrada 
    
    return entrada_negativa(T)

def regra_de_dantzig(T):
    c = T[0][1:-1] 
    maior_coef = 0
    temp = 0
    for i in range(len(c)):
        if c[i] < 0:
            temp = c[i]*-1
            if temp > maior_coef:
                  maior_coef = i
        else:
            if c[i] > maior_coef:
                maior_coef = i
    
    return maior_coef+1 # +1 para ajustar ao índice do tableau

def entrada_negativa(T):
    c = T[0][1:-1]
    for i in range(len(c)):
        print("c[i]:", c[i])
        if c[i] < 0:
            return (i+1) # +1 para ajustar ao índice do tableau
    
def problema_auxiliar(T):
    n = len(T) - 1 # com exeção da primeira coluna
    m = len(T[0]) - 2 # com exeção da coluna de w/z e da coluna b

    A = [linha[1:-1] for linha in T[1:]]
    b = [linha[-1] for linha in T[1:]]

    I = [[1 if j== i else 0 for j in range(n)] for i in range(n)]
    A_aux = [A[i] + I[i] for i in range(n)]

    c_original = T[0][1:-1]
    c_aux = [0]* (m) + [-1]* (n)

    linha_w = ([1] + c_aux + [0])

    linhas_rest = []
    for i in range(n):
        linha = [0] + A_aux[i] + [b[i]]
        linhas_rest.append(linha)
    
    T = [linha_w] + linhas_rest

    # Ajustar a linha de w somando todas as linhas das restrições
    for i in range(1, len(T)):
        for j in range(len(T[0])):
            T[0][j] += T[i][j]

    base = matriz.contem_matriz_identidade(T)

    return T, base, c_original

def regra_do_menor_quociente(T, coluna):
    # Entre as restrições, escolher a coluna cuja a razão entreo o seu elemnto b e o elementa da coluna escolhida no passo anterior seja menor possível (e positiva)

    # Ele testa todas as possibilidades e retorna o menor
    menor = 1000000
    linha_saida = None
    for i in range(1, len(T)):
        if T[i][coluna] > 0:
            quociente = T[i][-1] / T[i][coluna]
            if quociente < menor:
                menor = quociente
                linha_saida = i
    print("c[i]:", menor)

    if linha_saida is None:
        return None
    
    return linha_saida

def eliminacao_gauss(T, linha_pivo, coluna_pivo):
    # Torna o elemento T[linha_pivo][coluna_pivo] = 1 e zera os outros elementos da mesma coluna. 
    n_linhas = len(T)
    n_colunas = len(T[0])
    pivo = T[linha_pivo][coluna_pivo]

    if abs(pivo) < 1e-12:
        raise ValueError("Pivô nulo — escolha outra linha!")

    # 1️⃣ Normaliza a linha do pivô (deixa o pivô = 1)
    for j in range(n_colunas):
        T[linha_pivo][j] = T[linha_pivo][j] / pivo

    # 2️⃣ Zera todos os outros elementos da coluna pivô
    for i in range(n_linhas):
        if i != linha_pivo:
            fator = T[i][coluna_pivo]
            for j in range(n_colunas):
                T[i][j] -= fator * T[linha_pivo][j]

def tratar_degeneracao(T):
    c = T[0][1:-1]
    menor = 1000000
    temp = 0
    for i in range(len(c)):
        if c[i] < 0:
            temp = c[i]*-1
            if temp < menor:
                  menor = i  

    return menor+1 # +1 para ajustar ao índice do tableau

def fase_um(T):
    # 0 - Tratar as restrições com b < 0
    n = len(T) # linhas
    m = len(T[0]) # colunas (com excessão de b)

    for linha in T:
        if linha[-1] < 0:
            for i in range(1, m):
                linha[i] = -linha[i]

    # 1 - ENCONTRAR UMA BASE INICIAL VIÁVEL
    base = matriz.contem_matriz_identidade(T) 
    print("Base inicial encontrada:", base)
    c_original = T[0][1:-1]
    if base == False:
        T, base, c_original = problema_auxiliar(T)
    
    print("\nTableau:")
    for linha in T:
        print(linha)
    print("Base inicial:", base)
    print("custo original:", c_original)

    bases_visitadas = []
    bases_visitadas.append(base.copy())

    w = T[0][-1]
    i = 0
    while(True):
        print("Iteração:", i)
        i += 1

        # VERIFICAR VIOLAÇÃO DA FORMA CANÔNICA PRIMEIRO
        if(confere_b(T, base) == False):
            forma_canonica(T, base)
            print("\ntableau na forma canônica:")
            for linha in T:
                print(linha)

        # 2 - ESCOLHER VARIÁVEL QUE ENTRA NA BASE
        coluna_entrada = esolher_variavel_da_base(T)
        print("Coluna que entra na base:", coluna_entrada)

        # 3 - ESCOLHER VARIÁVEL QUE SAI DA BASE
        linha_saida = regra_do_menor_quociente(T, coluna_entrada)
        
        if linha_saida is None:
            print("Problema ilimitado!")
            return None
        print("Coluna que sai da base:", base[linha_saida-1])
        print("Linha escolhida:", linha_saida)

        if base[linha_saida-1] not in base:
            print(f"Atenção: variável da linha {linha_saida} não está na base!")
            return None

        # 4 - REALIZAR A ELIMINAÇÃO GAUSS-JORDAN
        eliminacao_gauss(T, linha_saida, coluna_entrada)
        print("\nTableau após iteração:")
        for linha in T:
            print(linha)

        # Atualizar a base
        base = matriz.contem_matriz_identidade(T) 
        if base in bases_visitadas:
            # Apareceu uma base repetida — ciclo detectado
            print("Ciclo detectado! Terminando a execução.")
            return None
        
        c_original = T[0][1:-1]
        if base == False:
            T, base, c_original = problema_auxiliar(T)
        
        print("Base nova:", base)

        bases_visitadas.append(base.copy())

        w = T[0][-1]
        if (confere_w(w) == True):
            break
        
        c = T[0][:]
        if (confere_c(c)):
            return c

def main():
    # LEMBRAR:
    # 1. O número de variáveis é igual ao número de colunas - 2 (excluindo a coluna de z e a coluna de soluções (b))
    T = entrada.ler_tableau("entrada.txt")
    for linha in T:
        print(linha)

    funcao_objetivo = fase_um(T)
    print("\nFunção objetivo após fase 1:", funcao_objetivo)


if __name__ == "__main__":
    main()