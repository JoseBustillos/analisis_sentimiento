def reputacion(positivo, negativo):
    # para el calculo sumamos los cantidad de tweets posit, negativos
    total = positivo + negativo
    # buscar el porcentaje
    prPos = (positivo * 100) / total
    prNeg = 100 - prPos
    # retornar porcentajes de los tweets sentimientos
    return "%.2f" % prPos, "%.2f" % prNeg
