import json
import sys
import math
import os
import numpy as np
from collections import OrderedDict


def parse(opencv_out, filename):
    # takes the <opencv_out> file as a string, parse it into a JSON file,
    # and write it into file with <filename>

    with open(opencv_out, 'r') as inputfile:
        data = inputfile.read()

    tempstr = data.split("Camera #")
    tempstr = tempstr[1:]
    ks = []
    rs = []
    s = []
    for i in xrange(len(tempstr)-1):
        curr_tempstr = tempstr[i]
        slot_num = int(curr_tempstr.split("K:")[0].split(":")[0])
        curr_kstr = curr_tempstr.split("K:")[1].split("R:")[0]
        curr_kstr = curr_kstr.replace('\n','').replace('[','').replace(']','').replace(';',',').split(', ')
        curr_rstr = curr_tempstr.split("K:")[1].split("R:")[1]
        curr_rstr = curr_rstr.replace('\n','').replace('[','').replace(']','').replace(';',',').split(', ')
        curr_k = [float(i) for i in curr_kstr]
        curr_r = [float(i) for i in curr_rstr]
        ks.append(curr_k)
        rs.append(curr_r)
        s.append(slot_num)

    curr_tempstr = tempstr[-1]
    slot_num = int(curr_tempstr.split("K:")[0].split(":")[0])
    curr_kstr = curr_tempstr.split("K:")[1].split("R:")[0]
    curr_kstr = curr_kstr.replace('\n','').replace('[','').replace(']','').replace(';',',').split(', ')
    curr_rstr = curr_tempstr.split("K:")[1].split("R:")[1].split('Warping images')[0]
    curr_rstr = curr_rstr.replace('\n','').replace('[','').replace(']','').replace(';',',').split(', ')
    curr_k = [float(i) for i in curr_kstr]
    curr_r = [float(i) for i in curr_rstr]
    ks.append(curr_k)
    rs.append(curr_r)
    s.append(slot_num)

    # now we have k matrices and r matrices
    # comments are the first guesses of the angles' meanings
    yaw = []  # x
    pitch = [] # y
    roll = [] # z
    k1 = []
    offsetx = []
    offsety = []
    f = []

    for i in xrange(len(ks)):
        curr_k = ks[i]
        curr_r = rs[i]
        R = list_to_numpy_array(curr_r)
        K = list_to_numpy_array(curr_k)
        x,y,z = rotation_matrix_to_euler_angles(R)
        yaw.append(x*180.0/math.pi)
        pitch.append(y*180.0/math.pi)
        roll.append(z*180.0/math.pi)
        offsetx.append(0)
        offsety.append(9)
        k1.append(1)
        f.append(2)
        #s.append(3)

    with open("reference.json") as json_file:
        json_data = json.load(json_file, object_pairs_hook = OrderedDict)

    poly = [[0]] * 10
    alist = [1]
    poly.insert(0, alist)

    for key in json_data.keys():
        for key2 in json_data[key]:
            if key2 == "global":
                json_data[key][key2]['vig_poly_red'] = poly
                json_data[key][key2]['vig_poly_green'] = poly
                json_data[key][key2]['vig_poly_blue'] = poly
    #            json_data[key][key2]['sensorwidth'] = im.size[0]
    #            json_data[key][key2]['sensorheight'] = im.size[1]
                json_data[key][key2]['sensorwidth'] = 4912
                json_data[key][key2]['sensorheight'] = 3680
                json_data[key][key2]['pixel_size'] = .0014
                json_data[key][key2]['focal_length'] = 35
            if key2 == "microcameras":
                for i in xrange(len(json_data[key][key2])):
                    json_data[key][key2][i] = {'Slot':int(s[i]), 'Sensorcal':["1", "1", "1", "1"], 'gain':1, 'vigoffset_x':0, 'vigoffset_y':0, 'Yaw': yaw[i], 'Pitch':pitch[i], 'Roll':roll[i], 'K1':k1[i], 'OFFSET_X':offsetx[i], 'OFFSET_Y':offsety[i], 'F':float(f[i])}
                for i in xrange(len(s)):
                    json_data[key][key2].append({'Slot': int(s[i]), 'Sensorcal': ["1", "1", "1", "1"], 'gain': 1, 'vigoffset_x': 0, 'vigoffset_y': 0, 'Yaw': yaw[i], 'Pitch': pitch[i], 'Roll': roll[i], 'K1': k1[i], 'OFFSET_X': offsetx[i], 'OFFSET_Y': offsety[i], 'F': float(f[i])})

    data = json.dumps(json_data, indent=4)
    with open(filename, "w") as outfile:
        outfile.write(data)
        print data
        print "wrote above data to " + filename


def list_to_numpy_array(R):
    new_lst = []
    for i in xrange(3):
        new_lst.append([R[i*3+j] for j in xrange(3)])
    return np.array(new_lst)


def is_rotation_matrix(R):
    #input R matrix should be numpy array
    Rt = np.transpose(R)
    isIdentity = np.dot(Rt, R)
    I = np.identity(3, dtype=R.dtype)
    n = np.linalg.norm(I - isIdentity)
    return n < 1e-6


def rotation_matrix_to_euler_angles(R):
    # input R matrix should be numpy array    #TODO: expand the string to fill in these lists
    assert(is_rotation_matrix(R))
    sy = math.sqrt(R[0,0] * R[0,0] + R[1,0] * R[1,0])
    singular = sy < 1e-6
    if not singular:
        x = math.atan2(R[2,1], R[2,2])
        y = math.atan2(-R[2,0], sy)
        z = math.atan2(R[1,0], R[0,0])
    else:
        x = math.atan2(-R[1,2], R[1,1])
        y = math.atan2(-R[2,0], sy)
        z = 0
    return np.array([x,y,z])


if __name__ == "__main__":
    parse(sys.argv[1], sys.argv[2])
