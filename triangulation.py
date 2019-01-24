#!/usr/bin/python3
import platform
Windows = platform.system() == 'Windows'

def cc_intersection(P0, P1, r0, r1):

	from math import sqrt, fabs

	P2   = [None,None]
	P3_1 = [None,None]
	P3_2 = [None,None]

	d = sqrt((P0[0]-P1[0])**2+(P0[1]-P1[1])**2)

	a = (r0**2-r1**2+d**2)/(2*d)

	h = sqrt(fabs(pow(r0,2)-pow(a,2)))

	P2[0]   = P0[0]+a*(P1[0]-P0[0])/d
	P2[1]   = P0[1]+a*(P1[1]-P0[1])/d

	P3_1[0] = P2[0]+h*(P1[1]-P0[1])/d
	P3_1[1] = P2[1]-h*(P1[0]-P0[0])/d

	P3_2[0] = P2[0]-h*(P1[1]-P0[1])/d
	P3_2[1] = P2[1]+h*(P1[0]-P0[0])/d

	return P3_1, P3_2

def calc_center(p):
	# lines are sets of two coordinates through which the line travels
	# eg. l1 = [[1,3],[4,6]]
	l1 = p[0]
	l2 = p[1]
	xdiff = (l1[0][0]-l1[1][0], l2[0][0]-l2[1][0])
	ydiff = (l1[0][1]-l1[1][1], l2[0][1]-l2[1][1])

	def det(a, b):
		return a[0]*b[1]-a[1]*b[0]

	div = det(xdiff, ydiff)
	if div == 0:
		raise Exception('Lines don\'t intersect')

	d = (det(*l1), det(*l2))
	x = det(d, xdiff)/div
	y = det(d, ydiff)/div

	return [int(round(21-y)), int(round(x))]

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
				if p[0][i] == p[1][j] == p[2][k]:
					return p[0][i]
				else:
					return calc_center(p)

def dBm2m(MHz, dBm):
	from math import log10

	global Windows

	if platform.system() == 'Windows':
		dBm = (dBm/2)-100

	FSPL = 27.55
	m = round((10**((FSPL-(20*log10(MHz))-dBm)/20))*0.5, 2)

	if m > 50:
		menu()

	return m

def get_dBm(APName):

	import subprocess

	global Windows

	if platform.system() == 'Windows':
		netscan = subprocess.run('netsh wlan show networks mode = bssid', shell=True, stdout=subprocess.PIPE)
		f = open('netscan.txt', 'w')
		f.write(netscan.stdout.decode('utf-8'))
		f.close()

	else:
		subprocess.run(['sudo iwlist wlo1 scan | grep -i -B 5 {} > ./netscan.txt'.format(APName)], shell=True)

	f = open('netscan.txt')
	lines = f.readlines()
	f.close()

	frequency = 0
	signal = 0

	if platform.system() == 'Windows':
		data = []
		for l in range(len(lines)):
			lines[l] = lines[l].strip()
			if 'V1F4' in l:
				data.append(l[l.index(l):l.index(l)+6])
			if 'Radio type' in lines[l]:
				freq = lines[l].split(':')
				freq = freq[1].strip()
				if freq == '802.11ac':
					frequency = 5230
				else:
					frequency = 2470

			if 'Signal' in lines[l]:
				sig = lines[l].split(':')
				sig = sig[1].strip()
				sig = sig[:-1]
				signal = int(sig)
	else:
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

def menu():

	print('======[Scanning]======')

	from termcolor import colored

	P0 = [18,16]
	P1 = [19,8]
	P2 = [0,7]

	AP0 = 'v1f4ap1'
	AP1 = 'v1f4ap2'
	AP2 = 'v1f4ap3'

	class AccessPointError(Exception):
		pass

	# print('\u001b[1mThis applet will attempt to triangulate your position based on WiFi Access Points\u001b[0m')

	def get_apNames():
		nonlocal AP0, AP1, AP2
		# print('Please enter the names for the three Access Points')
		# AP0 = input('Access Point 1: ')
		# AP1 = input('Access Point 2: ')
		# AP2 = input('Access Point 3: ')
		return get_apCoords()

	def get_apCoords():
		nonlocal AP0, AP1, AP2, P0, P1, P2
		# print('\u001b[1mNow you need to enter the coordinates for the AP\'s based on how many meters they are from you\u001b[0m')
		# print('\u001b[1mRequired format: [x,y]\u001b[0m')
		try:
			# P0 = eval(input('Access Point 1: '))
			# P1 = eval(input('Access Point 2: '))
			# P2 = eval(input('Access Point 3: '))

			if P0 == P1 or P1 == P2 or P2 == P0:
				raise AccessPointError
			# if (type(P0) or type(P1) or type(P2)) is not (list or tuple):
			# 	raise NameError
			else:

				dbP0 = get_dBm(AP0)
				dbP1 = get_dBm(AP1)
				dbP2 = get_dBm(AP2)

				r0 = dBm2m(dbP0[0], dbP0[1])
				r1 = dBm2m(dbP1[0], dbP1[1])
				r2 = dBm2m(dbP2[0], dbP2[1])

				r0 = round(r0, 2)
				r1 = round(r1, 2)
				r2 = round(r2, 2)

				print('\n======[Location Data]=======')
				print('AP1: {:>4} MHz, {:>3} dBm, distance: {:1.2f}m'.format(dbP0[0], dbP0[1], r0*2))
				print('AP2: {:>4} MHz, {:>3} dBm, distance: {:1.2f}m'.format(dbP1[0], dbP1[1], r1*2))
				print('AP3: {:>4} MHz, {:>3} dBm, distance: {:1.2f}m'.format(dbP2[0], dbP2[1], r2*2))

				l = location(P0, P1, P2, r0, r1, r2)
				print('You are at: {}'.format(l))
				return l

		except NameError:
			print(colored('Wrong format', 'red'))
			get_apCoords()

		# except ValueError as e:
		# 	print(colored(e, 'red'))
		# 	print(colored('Something went wrong, please re-enter the AP Data', 'red'))
		# 	get_apNames()

		except AccessPointError:
			print(colored('Something is wrong with the Access Points coordinates, please re-enter', 'red'))
			get_apCoords()

	return get_apNames()