import matriz
from entrada import ler_entrada

# ------------------------------------------------
# Variáveis e funções básicas
# ------------------------------------------------
def problema_auxiliar(A, b):
    """
    Constrói o problema auxiliar para o método simplex e escolhe uma base inicial viável.
    Retorna:
      - A_aux: matriz expandida [A | I]
      - c_aux: vetor de custos (min sum(a_i))
      - base: índices das variáveis básicas (as artificiais)
    """
    n = len(A)       # número de restrições
    m = len(A[0])    # número de variáveis originais

    # Corrige sinais de b negativos (multiplica linha toda por -1)
    for i in range(n):
        if b[i] < 0:
            A[i] = [-x for x in A[i]]
            b[i] = -b[i]

    # Cria matriz identidade I_n
    I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]

    # Matriz aumentada [A | I]
    A_aux = [A[i] + I[i] for i in range(n)]

    # Vetor de custos do problema auxiliar (min sum a_i)
    # c = [0, 0, ..., 0, 1, 1, ..., 1]  (para variáveis artificiais)
    c_aux = [0]*m + [1]*n

    # As variáveis básicas iniciais são as artificiais
    base = list(range(m, m+n))

    return A_aux, c_aux, base, b

def confere_x(x):
    return all(v >= 0 for v in x) 

def imprime(n, m, A, c, base, b):
    print("n, m", n, m)
    print("Vetor de custos c:", c)
    print("Matriz A:")
    for linha in A:
        print(linha)
    print("Vetor b:", b)
    print("\nBase inicial (índices):", base)

# ------------------------------------------------
# Fase 1 do Método simplex

# Objetivo: Encontrar uma Solução Básica Viável (SBV) para o problema original (P). Se o problema for inviável, ela prova isso. 
# Resultado Desejado: Um valor mínimo de custo artificial w igual a zero.

# FAZER:
# A primeira solução viável é o próprio b
# Preciso maximizar as variáveis da nova função de custo que é equivalente a max(-c)
# 

# LEMBRAR:
# Na fase 1 o vetor de custo original é ignorado
# max(-c) = w
# b não pode ser negativo se for, multiplica a linha toda por -1 (incluindo a restrição daquele b_i)
# ------------------------------------------------



# ------------------------------------------------
# Fase 2 do Método simplex
# ------------------------------------------------
def submatriz_base(A, base):
    return [[A[i][j] for j in base] for i in range(len(A))]

def main():
    n, m, c, A, b = ler_entrada("entrada.txt")

    if(matriz.contem_matriz_identidade(A) == False):
        A, c, base, b = problema_auxiliar(A, b)
    else:
        base = matriz.contem_matriz_identidade(A)

    imprime(n, m, A, c, base, b)

    x_completo_inicial = [0.0] * (len(A[0]) - len(b)) + b
    print("Solução básica inicial x:", x_completo_inicial)

    # Fim da Fase 1



if __name__ == "__main__":
    main()
