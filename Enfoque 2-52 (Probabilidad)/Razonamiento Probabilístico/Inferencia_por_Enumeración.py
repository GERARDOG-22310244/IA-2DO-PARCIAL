# Definimos las probabilidades base
P_Smoke = {True: 0.2, False: 0.8}
P_LungCancer_given_Smoke = {
    True: {True: 0.1, False: 0.9},
    False: {True: 0.01, False: 0.99}
}
P_XRay_given_LungCancer = {
    True: {True: 0.9, False: 0.1},
    False: {True: 0.2, False: 0.8}
}

# Enumeración de todos los casos posibles
def enumeration_ask(query_var, evidence):
    probs = {}
    for value in [True, False]:
        extended_evidence = evidence.copy()
        extended_evidence[query_var] = value
        probs[value] = enumerate_all(["Smoke", "LungCancer", "XRay"], extended_evidence)
    # Normalizar
    total = sum(probs.values())
    for key in probs:
        probs[key] /= total
    return probs

def enumerate_all(vars, evidence):
    if not vars:
        return 1.0
    Y = vars[0]
    rest = vars[1:]
    if Y in evidence:
        return prob(Y, evidence[Y], evidence) * enumerate_all(rest, evidence)
    else:
        return sum(prob(Y, yval, evidence) * enumerate_all(rest, {**evidence, Y: yval}) for yval in [True, False])

def prob(var, value, evidence):
    if var == "Smoke":
        return P_Smoke[value]
    elif var == "LungCancer":
        return P_LungCancer_given_Smoke[evidence["Smoke"]][value]
    elif var == "XRay":
        return P_XRay_given_LungCancer[evidence["LungCancer"]][value]

# Consultamos: P(LungCancer | XRay = True)
resultado = enumeration_ask("LungCancer", {"XRay": True})

# Mostrar resultados
print("P(LungCancer | XRay = True):")
for val, prob in resultado.items():
    print(f"  {val}: {prob:.4f}")
