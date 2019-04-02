import numpy as np

restricao = np.array([[1,1], # 1
					  [2,1], # 2
					  [2,2]]) #3
grausLib = np.array([[1,2,3,4],
					 [3,4,5,6],
					 [5,6,1,2]])

matrizes = np.array([
	# [[1.59,-0.40,-0.54,3],
	# 				  [-0.40, 1.70,0.40,2],
	# 				  [-0.54,0.40,0.54,7],
	# 				  [-0.54,0.40,0.54,7]],
					[[0, 0, 0, 0],
					[0, 1.05e8, 0, -1.05e8],
					[0, 0, 0, 0],
					[0, -1.05e8, 0, 1.05e8]],

					  
					 # [[2.59,-8.40,-0.54,2],
					 #  [-7.40,1.70,2.40,7],
					 #  [-9.54,3.40,6.54,1],
					 #  [-0.54,0.40,0.54,7]],

					[[1.4e8, 0, -1.4e8, 0],
					[0, 0, 0, 0],
					[-1.4e8, 0, 1.4e8, 0],
					[0, 0, 0, 0]],
					  
					 # [[2.59,-8.40,-0.54,4],
					 #  [-7.40,1.70,2.40,6],
					 #  [-9.54,3.40,6.54,4],
					 #  [-0.54,0.40,0.54,7]]

					[[0.30e8,0.40e8,-0.30e8,-0.40e8],
					[0.40e8,0.54e8,-0.40e8,-0.54e8],
					[-0.30e8,-0.40e8,0.30e8,0.40e8],
					[-0.40e8,-0.54e8,0.40e8,0.54e8]]

					  ])

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

def retornaglobalpronta1(matrices, lib, restriction):

	lib = np.array(lib).astype(int)

	No = []

	for i in range(len(restriction)):
		No.append(restriction[i][0]*2 - 2 + restriction[i][1])

	size = len(set(list(np.concatenate(lib))))

	Global = np.zeros((size, size), dtype='float')

	for i in range(len(matrices)):
		for x in range(len(matrices[i])):
			for y in range(len(matrices[i])):
				Global[lib[i][y] - 1, lib[i][x] - 1] += matrices[i][y, x]

	_list = []
	t_list = []

	No = np.array(No)

	No -= 1

	old_global = Global
	Global = np.delete(Global, No, 0)
	Global = np.delete(Global, No, 1)

	No += 1

	for i in (list(set(list(np.concatenate(lib))))):

		if i not in No:
			t_list.append(1)
		else:
			t_list.append(0)

		if len(t_list) == 2:
			_list.append(t_list)
			t_list = []

	return old_global, Global, _list

velhinha, matrizglobal, listamatriz = (retornaglobalpronta1(matrizes,grausLib,restricao))

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

listavalores = [0,150,-100]

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