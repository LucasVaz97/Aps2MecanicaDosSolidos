def checkinput():
    horas=24
    while True:
        user_input = input ()
        try:
            val = float(user_input)
            return val
        except ValueError:
            print("Por favor digite um numero")

print("Modulo de elasticidade: ")
E=checkinput()
print("Area secao transversal: ")
A=checkinput()
print("Comprimento: ")
comprimento=checkinput()
print("Carga")
P2=checkinput()
valor=(E*A)/comprimento
print("eu sou o valor")
print(valor)

u2=P2/valor
print("u2")
print(u2)
print("P1")
print(-valor*u2)
