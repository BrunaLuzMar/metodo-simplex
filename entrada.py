def ler_entrada(caminho="entrada.txt"):
    """
    Lê o arquivo de entrada e retorna n, m, c, A, b.
    """
    with open(caminho, "r") as f:
        linhas = f.readlines()

    n, m = map(int, linhas[0].split())
    c = list(map(float, linhas[1].split()))
    A, b = [], []

    for linha in linhas[2:2 + n]:
        valores = list(map(float, linha.split()))
        A.append(valores[:-1])
        b.append(valores[-1])

    return n, m, c, A, b

def ler_tableau(caminho_arquivo):
    """
    Lê um arquivo de texto com o formato:
        n m
        c1 c2 ... cm
        a11 a12 ... a1m b1
        ...
        an1 an2 ... anm bn
    E retorna o tableau inicial incluindo a coluna de w/z.
    """
    with open(caminho_arquivo, 'r') as f:
        linhas = [linha.strip() for linha in f if linha.strip()]

    # --- 1️⃣ Lê dimensões ---
    n, m = map(int, linhas[0].split())

    # --- 2️⃣ Lê função objetivo (coeficientes c) ---
    c = [float(x) for x in linhas[1].split()]
    # Garante que c tenha exatamente m coeficientes
    if len(c) > m:
        c = c[:m]
    elif len(c) < m:
        c = c + [0.0] * (m - len(c))

    # --- 3️⃣ Lê restrições ---
    A = []
    b = []
    for linha in linhas[2:]:
        partes = [float(x) for x in linha.split()]
        A.append(partes[:-1])
        b.append(partes[-1])

    # --- 4️⃣ Constrói o tableau ---
    tableau = []

    # Linha da função objetivo (w)
    linha_w = [1.0] + [x for x in c] + [0.0]  # w - c^T x = 0
    tableau.append(linha_w)

    # Linhas das restrições
    for i in range(n):
        linha = [0.0] + A[i] + [b[i]]
        tableau.append(linha)

    return tableau

