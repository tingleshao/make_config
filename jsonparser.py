#!/usr/bin/python3
import json
import sys
from collections import OrderedDict
import xml.etree.ElementTree
import math
import os

#parses json data from .pano into the .json file
#input pano filename, textfile with ports, and new json filename in that order as arguments



def parse(pano, ports, filename):

	#opens and parses through pano file, putting values in a list
	e = xml.etree.ElementTree.parse(pano).getroot()
	x = 0
	yaw = list()
	pitch = list()
	roll = list()
	k1 = list()
	offsetx = list()
	offsety = list()
	f = list()
	s = list()
	i = 1
	for child in e:
		if(child.tag == "images"):			
			while(len(s)<len(child)):
				for child2 in child:
					for child3 in child2:
						if(child3.tag=="def"):
							fi = child3.get('filename')
							head, sep, tail = fi.partition('_')
							head2, sep2, tail2 = tail.partition('.')
							if(int(head2)==i):
								s.append(head2)
								i+=1
								for child3 in child2:
									if(child3.tag == "camera"):
										y = child3.get('yaw')
										y = float(y)
										y = (180*y)/math.pi
										yaw.append(y)
										p = child3.get('pitch')
										p = float(p)
										p = (180*p)/math.pi
										pitch.append( p)
										r = child3.get('roll')
										r = float(r)
										r = (180*r)/math.pi
										roll.append(r)
										k = child3.get('k1')
										k = float(k)
										k1.append(k)
										F = child3.get('f')
										f.append(F)
										x+=1




	#opens and parses through json file, saving new pano values
	with open('reference.json') as json_file:
		json_data = json.load(json_file, object_pairs_hook = OrderedDict)

	poly = list()
	i = 0
	while(i < 10):
		alist = list()
		alist.insert(0, 0)
		poly.insert(i, alist)
		i +=1
	alist = list()
	alist.insert(0, 1)
	poly.insert(i, alist)

	for key in json_data.keys():
		for key2 in json_data[key]:
			if(key2 == "global"):
				json_data[key][key2]['vig_poly_red'] = poly
				json_data[key][key2]['vig_poly_green'] = poly
				json_data[key][key2]['vig_poly_blue'] = poly
				json_data[key][key2]['sensorwidth'] = 1920
				json_data[key][key2]['sensorheight'] = 1080
				json_data[key][key2]['pixel_size'] = .0014
				json_data[key][key2]['focal_length'] = 35
			if(key2 == "microcameras"):
				i = 0
				while(i<len(json_data[key][key2])):
					json_data[key][key2][i] = {'Slot': int(s[i]), 'Sensorcal': ["1", "1", "1", "1"], 'gain': 1, 'vigoffset_x': 0, 'vigoffset_y': 0, 'Yaw': yaw[i], 'Pitch': pitch[i], 'Roll': roll[i], 'K1': k1[i], 'OFFSET_X': 0, 'OFFSET_Y': 0, 'F': float(f[i])}
					i +=1	
				while(i<len(s)):
					json_data[key][key2].append({'Slot': int(s[i]), 'Sensorcal': ["1", "1", "1", "1"], 'gain': 1, 'vigoffset_x': 0, 'vigoffset_y': 0, 'Yaw': yaw[i], 'Pitch': pitch[i], 'Roll': roll[i], 'K1': k1[i], 'OFFSET_X': 0, 'OFFSET_Y': 0, 'F': float(f[i])})
					i+=1


	#saves new json file
	data = json.dumps(json_data, indent=4)
	with open(filename, "w") as outfile:
		outfile.write(data)

	i = 1
	fovea = list()
	ports = open(ports, 'r')
	lines = ports.read().split('\n')
	rshall = list()
	rsh = list()
	while(i<=len(s)):
		st="mcam_" + str(i) + '@10.3.0.' + str(lines[i-1]) + ':11000\n'
		rs = "nohup ssh ubuntu@10.3.0." + str(i) + " \"$1\" & \n"
		sh = "rsh ubuntu@10.3.0." + str(lines[i-1]) + " \" python3 /bin/aci/createAciConfig.py -c mcam_" + str(i) + "\" \n"
		i+=1
		fovea.append(st)
		rshall.append(rs)
		rsh.append(sh)
	
	with open('fovea.cfg', "w") as outfile:
		j = 0
		while(j<len(fovea)):
			outfile.write(fovea[j])
			j+=1
	with open('rshall.sh', 'w') as outfile:
		j = 0
		while(j<len(rshall)):
			outfile.write(rshall[j])
			j+=1

	j = 0
	while(j<len(rsh)):
		print(rsh[j])
		os.system(rsh[j]) 
		j+=1
		print(j)



if __name__ == "__main__":
	parse(sys.argv[1], sys.argv[2], sys.argv[3])
