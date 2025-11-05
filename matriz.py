def produto_matricial(A, B):
    n = len(A)
    m_b = len(B[0])

    C = [[0 for _ in range(m_b)] for _ in range(n)]

    for i in range(len(A)):
        for j in range(len(B[0])):
            soma = 0
            for k in range(len(B)):
                soma += A[i][k] * B[k][j]
            C[i][j] = soma
    return C

def transposta(M):
    n = len(M)
    m = len(M[0])
    C = [[0 for _ in range(m)] for _ in range(n)]

    for i in range(n):
        for j in range(m):
            C[j][i] = M[i][j]
    return C

def contem_matriz_identidade(A):
    """
    Verifica se existe uma submatriz identidade dentro de A (n x m).
    Retorna True se sim, False caso contrário.
    """
    n = len(A)
    m = len(A[0])
    colunas_identidade = []

    # Para cada coluna de A, verifica se ela é um vetor unitário (1 em uma posição, 0 nas demais)
    for j in range(m):
        coluna = [A[i][j] for i in range(n)]
        if coluna.count(1) == 1 and coluna.count(0) == n - 1:
            colunas_identidade.append(j)

    # Se o número de colunas unitárias for igual ao número de linhas, temos uma identidade
    if len(colunas_identidade) >= n:
        # Checar se cada linha tem exatamente um "1" em posições diferentes
        linhas_com_1 = set()
        for j in colunas_identidade:
            for i in range(n):
                if A[i][j] == 1:
                    linhas_com_1.add(i)
                    break
        if len(linhas_com_1) == n:
            return colunas_identidade

    return False

def inversa(A):
    # Cria a matriz aumentada [A|b]
    n = len(A)
    for i in range(n):
        A[i] = A[i] + [b[i]]
    
    # Eliminação Gauss-Jordan
    for i in range(n):
        # 1. Pivô diferente de zero — se for zero, troca linha
        if A[i][i] == 0:
            for j in range(i+1, n):
                if A[j][i] != 0:
                    A[i], A[j] = A[j], A[i]
                    break
        
        # 2. Normaliza a linha para que o pivô seja 1
        pivot = A[i][i]
        A[i] = [a / pivot for a in A[i]]
        
        # 3. Zera os elementos acima e abaixo do pivô
        for j in range(n):
            if j != i:
                fator = A[j][i]
                A[j] = [A[j][k] - fator * A[i][k] for k in range(n + 1)]
    
    # A solução é a última coluna
    X = [A[i][-1] for i in range(n)]
    return X

def calcula_determinante(A, n=None):
    # Se o tamanho não for fornecido, deduz automaticamente
    if n is None:
        n = len(A)

    # Caso base: 1x1
    if n == 1:
        return A[0][0]

    # Caso base: 2x2
    if n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]

    # Caso base: 3x3 (fórmula direta — mais rápida)
    if n == 3:
        return (A[0][0] * A[1][1] * A[2][2] +
                A[0][1] * A[1][2] * A[2][0] +
                A[0][2] * A[1][0] * A[2][1] -
                A[0][2] * A[1][1] * A[2][0] -
                A[0][0] * A[1][2] * A[2][1] -
                A[0][1] * A[1][0] * A[2][2])

    # Caso geral: expansão por cofatores na primeira linha
    det = 0
    for j in range(n):
        # Construir a submatriz (remover linha 0 e coluna j)
        submatriz = [linha[:j] + linha[j+1:] for linha in A[1:]]
        cofator = ((-1) ** j) * A[0][j] * determinante(submatriz, n - 1)
        det += cofator

    return det





    

