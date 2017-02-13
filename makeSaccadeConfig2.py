import json
import sys
import math
import os
import numpy as np
from collections import OrderedDict
import eulerangles


def parse(opencv_out, filename):
    # takes the <opencv_out> file as a string, parse it into a JSON file,
    # and write it into file with <filename>

    with open(opencv_out, 'r') as inputfile:
        data = inputfile.read()

    tempstr = data.split("Camera #")
    tempstr = tempstr[1:]
    tempstr2 = data.split("last place: ")
    tempstr2 = tempstr2[1:]
    ks = []
    rs = []
    s = []
    for i in xrange(len(tempstr)-1):
        curr_tempstr = tempstr[i]
        curr_tempstr2 = tempstr2[i]
        slot_num = int(curr_tempstr.split("K:")[0].split(":")[0])
        curr_kstr = curr_tempstr.split("K:")[1].split("R:")[0]
        curr_kstr = curr_kstr.replace('\n','').replace('[','').replace(']','').replace(';',',').split(', ')
        #curr_rstr = curr_tempstr.split("K:")[1].split("R:")[1]
        #curr_rstr = curr_rstr.replace('\n','').replace('[','').replace(']','').replace(';',',').split(', ')
        curr_rstr = curr_tempstr2.split("R:")[1].split("Multi-band blender")[0].split("Compositing")[0]
        curr_rstr = curr_rstr.replace('\n','').replace('[','').replace(']','').replace(';',',').split(', ')
        curr_k = [float(i) for i in curr_kstr]
        curr_r = [float(i) for i in curr_rstr]
        ks.append(curr_k)
        rs.append(curr_r)
        s.append(slot_num)
    print "Ks length: "
    print len(ks)

    curr_tempstr = tempstr[-1]
    curr_tempstr2 = tempstr2[-1].split("Finished")[0].split("Warping images")[0].split("Multi-band blender")[0].split("Compositing")[0]
    slot_num = int(curr_tempstr.split("K:")[0].split(":")[0])
    curr_kstr = curr_tempstr.split("K:")[1].split("R:")[0]
    curr_kstr = curr_kstr.replace('\n','').replace('[','').replace(']','').replace(';',',').split(', ')
#    curr_rstr = curr_tempstr.split("K:")[1].split("R:")[1].split('Warping images')[0]
    curr_rstr = curr_tempstr2.split("R:")[1]
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
        # print out the first rotation matrix
        if i == 0:
            print "R: "
            print R
#        x,y,z = eulerangles.mat2euler(R)
#        if i == 0:
            #print "x, y, z:"
            #print x * 180.0 / math.pi
            #print y* 180.0 / math.pi
            #print z* 180.0 / math.pi
    #    if i == 0:
        #    x,y,z = rotation_matrix_to_euler_angles(R, True)
    #    x,y,z = rotation_matrix_to_euler_angles(R, True)
    #    x,y,z = rotation_matrix_to_euler_angles_xzy(R, True)
    #    x,y,z = rotation_matrix_to_euler_angles_yxz(R, True)
    #    x,y,z = rotation_matrix_to_euler_angles_yzx(R, True)
        x,y,z = rotation_matrix_to_euler_angles_zxy(R, True)

    #    else:
        #    x,y,z = rotation_matrix_to_euler_angles(R, False)
    #        x,y,z = rotation_matrix_to_euler_angles_xyz(R, True)
        print "xyz: "
        print x, y, z
        yaw.append(y*180.0/math.pi)
        pitch.append(x*180.0/math.pi)
        roll.append(z*180.0/math.pi)
        offsetx.append(0)
        offsety.append(9)
        k1.append(0)
        f.append(19500)
        #s.append(3)

    with open("reference.json") as json_file:
        json_data = json.load(json_file, object_pairs_hook = OrderedDict)

    poly = [[0]] * 10
    alist = [1]
    poly.insert(len(poly), alist)

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
                print "key2 len: "
                print len(json_data[key][key2])
                for i in xrange(len(json_data[key][key2])):
                    json_data[key][key2][i] = {'Slot':int(s[i]), 'Sensorcal':["1", "1", "1", "1"], 'gain':1, 'vigoffset_x':0, 'vigoffset_y':0, 'Yaw': yaw[i], 'Pitch':pitch[i], 'Roll':roll[i], 'K1':k1[i], 'OFFSET_X':offsetx[i], 'OFFSET_Y':offsety[i], 'F':float(f[i])}
                offset = len(json_data[key][key2])
                print offset
                for i in xrange(len(s)-len(json_data[key][key2])):
                    print "i+offset:"
                    print i + offset
                    json_data[key][key2].append({'Slot': int(s[i+offset]), 'Sensorcal': ["1", "1", "1", "1"], 'gain': 1, 'vigoffset_x': 0, 'vigoffset_y': 0, 'Yaw': yaw[i+offset], 'Pitch': pitch[i+offset], 'Roll': roll[i+offset], 'K1': k1[i+offset], 'OFFSET_X': offsetx[i+offset], 'OFFSET_Y': offsety[i+offset], 'F': float(f[i+offset])})

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


def rotation_matrix_to_euler_angles(R, verbose):
    # input R matrix should be numpy array    #TODO: expand the string to fill in these lists
    assert(is_rotation_matrix(R))
    sy = math.sqrt(R[0,0] * R[0,0] + R[1,0] * R[1,0])
    singular = sy < 1e-6
    if not singular:
        if verbose:
            print "R21:"
            print R[2,1]
            print R[2,2]
            print R[2,0]
            print R[1,0]
            print R[0,0]
            print R[1,2]
            print R[1,1]
        x = math.atan2(R[2,1], R[2,2])
        y = math.atan2(-R[2,0], sy)
        z = math.atan2(R[1,0], R[0,0])
    else:
        x = math.atan2(-R[1,2], R[1,1])
        y = math.atan2(-R[2,0], sy)
        z = 0
    return np.array([x,y,z])

def rotation_matrix_to_euler_angles_xyz(R, verbose):
    assert(is_rotation_matrix(R))
    sy = math.sqrt(R[1,2] * R[1,2] + R[2,2] * R[2,2])
    singular = sy < 1e-6
    if not singular:
        x = math.atan2(-R[1,2], R[2,2])
        y = math.atan2(R[0,2], sy)
        z = math.atan2(-R[0,1], R[0,0])
    else:
        print "singular"
    return np.array([x,y,z])

def rotation_matrix_to_euler_angles_xzy(R, verbose):
    assert(is_rotation_matrix(R))
    sy = math.sqrt(R[1,1] * R[1,1] + R[2,1] * R[2,1])
    singular = sy < 1e-6
    if not singular:
        x = math.atan2(R[2,1], R[1,1])
        y = math.atan2(R[0,2], R[0,0])
        z = math.atan2(-R[0,1], sy)
    else:
        print "singular"
    return np.array([x,y,z])

def rotation_matrix_to_euler_angles_yxz(R, verbose):
    assert(is_rotation_matrix(R))
    sy = math.sqrt(R[1,0] * R[1,0] + R[1,1] * R[1,1])
    singular = sy < 1e-6
    if not singular:
        x = math.atan2(-R[1,2], sy)
        y = math.atan2(R[0,2], R[2,2])
        z = math.atan2(R[1,0], R[1,1])
    else:
        print "singular"
    return np.array([x,y,z])

def rotation_matrix_to_euler_angles_yzx(R, verbose):
    assert(is_rotation_matrix(R))
    sy = math.sqrt(R[1,1] * R[1,1] + R[1,2] * R[1,2])
    singular = sy < 1e-6
    if not singular:
        x = math.atan2(-R[1,2], R[1,1])
        y = math.atan2(-R[2,0], R[0,0])
        z = math.atan2(R[1,0],sy)
    else:
        print "singular"
    return np.array([x,y,z])

def rotation_matrix_to_euler_angles_zxy(R, verbose):
    assert(is_rotation_matrix(R))
    sy = math.sqrt(R[2,0] * R[2,0] + R[2,2] * R[2,2])
    singular = sy < 1e-6
    if not singular:
        x = math.atan2(R[2,1],sy)
        y = math.atan2(-R[2,0], R[2,2])
        z = math.atan2(-R[0,1], R[1,1])
    else:
        print "singular"
    return np.array([x,y,z])


if __name__ == "__main__":
    parse(sys.argv[1], sys.argv[2])
