import math

P0 = [2,2]
P1 = [4,9]
P2 = [16,2]

r0 = math.sqrt(37)
r1 = math.sqrt(52)
r2 = math.sqrt(65)

def cc_intersection(P0, P1, r0, r1):

	P2 = [None,None]
	P3_1 = [None,None]
	P3_2 = [None,None]

	d = math.sqrt((P0[0]-P1[0])**2+(P0[1]-P1[1])**2)

	a = (r0**2-r1**2+d**2)/(2*d)

	h = math.sqrt(r0**2-a**2)

	P2[0] = P0[0]+a*(P1[0]-P0[0])/d
	P2[1] = P0[1]+a*(P1[1]-P0[1])/d

	P3_1[0] = P2[0]+h*(P1[1]-P0[1])/d
	P3_1[1] = P2[1]-h*(P1[0]-P0[0])/d

	P3_2[0] = P2[0]-h*(P1[1]-P0[1])/d
	P3_2[1] = P2[1]+h*(P1[0]-P0[0])/d

	return P3_1, P3_2

def location(P0, P1, P2, r0, r1, r2):

	p0 = cc_intersection(P0, P1, r0, r1)
	p1 = cc_intersection(P1, P2, r1, r2)
	p2 = cc_intersection(P2, P0, r2, r0)

	p = [p0, p1, p2]

	for i in range(3):
		for j in range(2):
			for k in range(2):
				p[i][j][k] = round(p[i][j][k])

	for i in range(2):
		for j in range(2):
			for k in range(2):
				if p[0][i] == p[1][0] == p[2][k]:
					return p[0][i]

def dBm2m():
	from math import log10

	MHz = int(input('WiFi Frequency in MHz (2412, 5180, ...): '))
	dBm = int(input('Detected signal strength in dBm (-53, -78, ...): '))

	FSPL = 27.55 # de factor voor het verlies van signaalsterkte

	m = round(10**((FSPL-(20*log10(MHz))-dBm)/20), 2)

	return m

print(dBm2m())