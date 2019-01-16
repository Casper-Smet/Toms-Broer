import math

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

def dBm2m(MHz, dBm):
	from math import log10

	FSPL = 27.55

	m = round(10**((FSPL-(20*log10(MHz))-dBm)/20), 2)

	return m

def get_dBm(APName):
	import subprocess
	subprocess.run(['sudo iwlist wlo1 scan | grep -i -B 5 {} > ./iwlist_scan.txt'.format(APName)], shell=True)

	f = open('iwlist_scan.txt')
	lines = f.readlines()

	frequency = 0
	signal = 0

	for l in range(len(lines)):
		lines[l] = lines[l].strip()
		if 'Frequency:' in lines[l]:
			freq = lines[l].split(':')
			freq = freq[1].split(' ')
			frequency = int(float(freq[0])*1000)

		if 'Signal' in lines[l]:
			sig = lines[l].split('=')
			sig = sig[-1].split(' ')
			signal = int(sig[0])

	return frequency, signal

P0 = [2,2]
P1 = [4,9]
P2 = [16,2]

dbP0 = get_dBm('V1F4AP1')
dbP1 = get_dBm('V1F4AP2')
dbP2 = get_dBm('V1F4AP3')

r0 = dBm2m(dbP0[0], dbP0[1])
r1 = dBm2m(dbP1[0], dbP1[1])
r2 = dBm2m(dbP2[0], dbP2[1])

print('Access Points: ')
print('AP1: {:>4} MHz, {:>3} dBm, distance: {:1.2f}m'.format(dbP0[0], dbP0[1], r0))
print('AP2: {:>4} MHz, {:>3} dBm, distance: {:1.2f}m'.format(dbP1[0], dbP1[1], r1))
print('AP3: {:>4} MHz, {:>3} dBm, distance: {:1.2f}m'.format(dbP2[0], dbP2[1], r2))