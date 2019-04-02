import numpy as np

restricao = np.array([[1,1], 
					  [2,1], 
					  [2,2]])
grausLib = np.array([[1,2,3,4],
					 [3,4,5,6],
					 [5,6,1,2]])

matrizes = np.array([[[1.59,-0.40,-0.54,3],
					  [-0.40, 1.70,0.40,2],
					  [-0.54,0.40,0.54,7],
					  [-0.54,0.40,0.54,7]],
					  
					 [[2.59,-8.40,-0.54,2],
					  [-7.40,1.70,2.40,7],
					  [-9.54,3.40,6.54,1],
					  [-0.54,0.40,0.54,7]],
					  
					 [[2.59,-8.40,-0.54,4],
					  [-7.40,1.70,2.40,6],
					  [-9.54,3.40,6.54,4],
					  [-0.54,0.40,0.54,7]]])

def retornaglobalpronta(matrizes,grausLib,restricao):

	NoX = []
	NoY = []

	for i in range(len(grausLib)):
		for j in range(len(restricao)):
			if restricao[j][0] in grausLib[i]:
				if restricao[j][1] == 1:
					if restricao[j][0] not in NoX:
						NoX.append(restricao[j][0])
				else:
					if restricao[j][0] not in NoY:
						NoY.append(restricao[j][0])

	tamanho = len(set(list(np.concatenate(grausLib))))

	Global = np.zeros((tamanho, tamanho), dtype='float')

	for i in range(len(matrizes)):
		for x in range(len(matrizes[i])):
			for y in range(len(matrizes[i])):
				Global[grausLib[i][y] - 1, grausLib[i][x] - 1] += matrizes[i][y,x]

	global_velha = Global

	NoX = np.array(NoX)
	NoX -= 1
	NoY = np.array(NoY)
	NoY -= 1

	lista = []
	lista_temporaria = []
	NoX += 1
	NoY += 1

	No = list(set(np.concatenate([NoX,NoY])))
	Global = np.delete(Global, No, 0)
	Global = np.delete(Global, No, 1)

	for i in (list(set(list(np.concatenate(grausLib))))):

		if i not in NoX:
			lista_temporaria.append(1)
		else:
			lista_temporaria.append(0)

		if len(lista_temporaria) == 2:
			lista.append(lista_temporaria)
			lista_temporaria = []

	return global_velha, Global, lista

velhinha, matrizglobal, listamatriz = (retornaglobalpronta(matrizes,grausLib,restricao))

print("Criando Matriz Global")
print("Entradas (matrizes, lib, restricao):")
print("Matrizes:")
print(matrizes)
print("Lib:")
print(grausLib)
print("Restricao:")
print(restricao)
print("-"*40)
print("Saidas (global não cortada, global cortada, lista de 1s e 0s):")
print("Global não cortada:")
print(velhinha)
print("Global cortada:")
print(matrizglobal)
print("lista de 1s e 0s")
print(listamatriz)
print("\n"*2)

listavalores = [2,3,1,4]

def calcula(vetor, matriz):
	v = np.array(vetor)
	m = np.array(matriz)
	return m.dot(v)

def criaVetor(lista_de_valores, lista_de_zeros_e_uns):
	listaReturn = []

	for i in range(len(lista_de_zeros_e_uns)):
		for j in range(len(lista_de_zeros_e_uns[i])):
			if lista_de_zeros_e_uns[i][j] == 0:
				listaReturn.append(0)
			else:
				listaReturn.append(lista_de_valores[0])
				del lista_de_valores[0]

	return listaReturn

print("Criando a lista pra multiplicar a Matriz:")
print("Entradas (valores de deslocamento do gauss (lista), lista de 1s e 0s (lista de listas)):")
print("Valores de deslocamento do gauss (lista)")
print(listavalores)
print("Lista de 1s e 0s (lista de listas):")
print(listamatriz)
print("-"*40)
vetorzin = (criaVetor(listavalores, listamatriz))
print("Saidas (lista de forcas (lista)):")
print("Lista gauss modificada (lista):")
print(vetorzin)
print("\n"*2)

print("Criando a lista de forcas:")
print("Entradas (lista gauss modificada, matriz nao cortada)")
print("Lista de forcas/lista gauss modificada")
print(vetorzin)
print("Matriz nao cortada")
print(velhinha)
print("-"*40)
print("Saidas (Lista de forcas):")
print(calcula(vetorzin, velhinha))
print("\n"*2)