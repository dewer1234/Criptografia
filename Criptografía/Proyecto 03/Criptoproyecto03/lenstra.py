import sys
from math import *
from random import randint

#Funcion que nos dice el maximo comun divisor de dos numeros
def mcd(a, b):
	while b != 0:
		a, b = b, a % b
	return a

# Obtiene todos los primos antes del numero num
def primos(num):
	num2 = num+1
	normal = set()
	primos = []

	for i in range(2, num2):
		if i in normal:
			continue

		for f in range(i*2, num2, i):
			normal.add(f)

		primos.append(i)

	return primos


# regresa el inverso multiplicativo de a en el modulo b
#y es el inverso y z es el mcd de a y b
def inverso(a, b):
	if b == 0:
		return 1, 0, a
	q, m = divmod(a, b)
	x, y, z = inverso(b, m)
	return y, x - q * y, z


# Suma de puntos elipticos
# p, q son los puntos a sumar
# a, b son los a y b de la curva
# m es el modulo
def suma_puntos(p, q, a, b, m):
	xp = p[0]
	yp = p[1]
	xq = q[0]
	yq = q[1]
	if p[2] == 0: return q
	if q[2] == 0: return p
	if xp == xq:
		if (yp + yq) % m == 0:
			return 0, 1, 0  # Infinity
		numerador = (3 * int(pow(xp,2)) + a) 
		denominador = (2 * yp) 
		inv, _, gcd = inverso(denominador, m)
		lamb = numerador*inv % m
		#print(lamb)
		newx = (lamb*lamb - 2*xp) % m
		#print("x ", newx)
		newy = (lamb*(xp - newx) - yp) % m
		#print("y ", newy)

		
		if gcd > 1:
			print(gcd, "puede ser un factor")
			return 0, 0, denominador
		return newx, newy, 1

	else:
		numerador = (yq - yp) 
		denominador = (xq - xp) 
		inv, _, gcd = inverso(denominador, m)
		lamb = numerador*inv % m
		newx = (int(pow(lamb,2)) - xp - xq) % m
		newy = (lamb*(xp - newx) - yp) % m
		if gcd > 1:
			print(gcd, "puede ser un factor")
			return 0, 0, denominador
		return newx, newy, 1
	


#Algoritmo double and add para multplicación de puntos
#n es el escalar a multiplicar
#a, b son los a y b de la curva eliptica
#m es el modulo
#p es el punto a multiplicar
def double_add(n, a, b, m, p):
	k = str(bin(n))
	k = k[2:]
	q = (0,1,0)
	#print(k)
	for i in k :
		q = suma_puntos(q, q, a, b, m)
		#print(q)
		if i == '1' :
			#print(i)
			q = suma_puntos(q, p, a, b, m)
			#print(q)

	return q


#Algoritmo de Lenstra para fortorización de curvas elípticas, tendrá como limite hasta 9999 iteraciones
def lenstra(n):
	if is_prime(n):
		return  "numero primo"
	g = n
	limite = 9999
	#se genera una curva eliptica aleatoria
	while g == n:
		q = randint(0, n - 1), randint(0, n - 1), 1 
		a = randint(0, n - 1)
		b = (q[1] * q[1] - q[0] * q[0] * q[0] - a * q[0]) % n
		g = mcd(3 * a * a * a + 20 * b * b, n)  
	if g > 1: # Si el g es mayor a 1, entonces regresamos el factor
		return g
	# se repite k veces con k igual tamaño del limite
	for p in primos(limite):
		x = p
		while x < limite:
			q = double_add(p, a, b, n, q)
			if q[2] > 1:
				return mcd(q[2], n)
			x = p * x
	return 0

#checa si el numero a es primo
def is_prime(a):
	return all(a % i for i in range(2, a))

def main():
	print("Proyecto 03 - Algoritmo de Lenstra")
	print("Diana Valeria Gomez Lopez, número de cuenta: 312338479")
	print("Brandon Padilla Ruiz: número de cuenta: 312139805")
	n = input('Ingresa un número no primo:')  
	factor = int(lenstra(int(n)))
	if factor == 0:
		print("no se encontro un factor, vuelve a intentarlo")
		sys.exit(0)
	factor2 = int(int(n)/factor)
	print(n, "se descompone en ",factor, " y ", factor2 )


if __name__ == '__main__':
	main()



