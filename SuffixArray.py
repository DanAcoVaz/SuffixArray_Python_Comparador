import os
import re

#Funcion para construir el suffix array
def build_suffix_array(text):
    suffixes = [(text[i:], i) for i in range(len(text))]
    suffixes.sort() #Ordenacion lexografica
    suffix_array = [s[1] for s in suffixes]
    return suffix_array

#Funcion para construir el LCP Array (Longest Common Prefix) usando Algoritmo de Kasai
def build_lcp_array(text, suffix_array):
    n = len(text)
    rank = [0] * n
    lcp = [0] * n

    for i in range(n):
        rank[suffix_array[i]] = i
    
    k = 0
    for i in range (n):
        if rank[i] == 0:
            k = 0
            continue

        j = suffix_array[rank[i] - 1]
        while i + k < n and j + k < n and text[i + k] == text[j + k]:
            k += 1
        
        lcp[rank[i]] = k

        if k:
            k -= 1

    return lcp

#Funcion para conseguir los substrings comunes entre los dos codigos
def extract_common_substrings(text, suffix_array, lcp_array, sep_index, min_length = 10):
    common_substrings = set() #Uso de sets en Python, evitando datos duplicados

    for i in range(1, len(text)): #Ignoramos el primer valor del LCP pues sabemos sera 0
        lcp_len = lcp_array[i]
        if lcp_len < min_length:
            continue

        start1 = suffix_array[i]
        start2 = suffix_array[i - 1]

        in_first = start1 < sep_index
        in_second = start2 < sep_index

        if in_first != in_second:
            base_start = start1 if in_first else start2
            for length in range(min_length, lcp_len + 1): #Obtenemos todos los substrings que encontremos
                substring = text[base_start:base_start + length]
                common_substrings.add(substring)
        
    filtered = set() #Filtramos para obtener las cadenas mas largas unicas que se repitan
    common_substrings = sorted(common_substrings, key=lambda s: (-len(s), s))
    for s in common_substrings:
        if not any(s in other and s != other for other in filtered):
            filtered.add(s)
        
    return sorted(filtered, key=lambda x: (-len(x), x))

#Calculamos porcentaje de similaridad.
def similarity_score(common_substrings, len_prog1, len_prog2):
    total_common = sum(len(s) for s in common_substrings)
    return (total_common / min(len_prog1, len_prog2)) * 100

#Generamos el reporte en archivo txt
def generate_report(common_substrings, score, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("=== Subcadenas comunes encontradas ===\n\n")
        for s in common_substrings:
            f.write(f"- '{s}' (longitud {len(s)})\n")
        f.write(f"\n=== Porcentaje de similitud: {score:.2f}% ===\n")

#Preprocesamos codigo para compara codigos mas limpios sin tener en cuenta comentarios o formato.
def preprocesar_codigo(codigo):
    #Comentarios de linea (//, #)
    codigo = re.sub(r'#.*', '', codigo)
    codigo = re.sub(r'//.*', '', codigo)

    #Comentarios multilinea (/* */)
    codigo = re.sub(r'/\*[\s\S]*?\*/', '', codigo)

    #Espacios y lineas vacias
    codigo = "\n".join(line.strip() for line in codigo.splitlines() if line.strip())

    #Multiples espacios por uno solo
    codigo = re.sub(r'\s+', ' ', codigo)

    return codigo

#Pedimos los archivos a comparar, el archivo a escribir el output y la opcion de hacer preprocesamiento o no.
def comparar_codigos(archivo1, archivo2, output_file, preprocesamiento):
    #Verificamos que existan los archivos
    if not os.path.exists(archivo1):
        print(f"Error: El archivo '{archivo1}' no existe.")
        return
    if not os.path.exists(archivo2):
        print(f"Error: El archivo '{archivo2}' no existe.")
        return
    
    #Leemos los archivos
    with open(archivo1, "r", encoding="utf-8") as f1:
        codigo1 = f1.read()
    with open(archivo2, "r", encoding="utf-8") as f2:
        codigo2 = f2.read()
    
    #Si se pidio preprocesamiento, lo hacemos
    if preprocesamiento:
        codigo1 = preprocesar_codigo(codigo1)
        codigo2 = preprocesar_codigo(codigo2)

    combined = codigo1 + "#" + codigo2 + "$"
    sep_index = len(codigo1)

    suffix_array = build_suffix_array(combined)
    lcp_array = build_lcp_array(combined, suffix_array)
    comunes = extract_common_substrings(combined, suffix_array, lcp_array, sep_index)
    score = similarity_score(comunes, len(codigo1), len(codigo2))
    generate_report(comunes, score, output_file)
    print(f"Comparacion completada. Resultado guardado en '{output_file}'.")



text1 ="notes_manager.py"
text2 = "journal_handler.py"

comparar_codigos(text1, text2, "output.txt", True)