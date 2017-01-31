



def parse(opencv_out, filename):
    # takes the <opencv_out> file as a string, parse it into a JSON file,
    # and write it into file with <filename>

    with open(opencv_out, 'r') as inputfile:
        data = inputfile.read()

    tempstr = data.split("Camera #")
    tempstr = tempstr[1:]
    ks = []
    rs = []
    for i in xrange(len(tempstr)-1):
        curr_tempstr = tempstr[i]
        curr_kstr = curr_tempstr.split("K:")[1].split("R:")[0]
        curr_kstr = curr_kstr.replace('\n','').replace('[','').replace(']','').replace(';',',').split(', ')
        curr_rstr = curr_tempstr.split("K:")[1].split("R:")[1]
        curr_rstr = curr_rstr.replace('\n','').replace('[','').replace(']','').replace(';',',').split(', ')
        curr_k = [float(i) for i in curr_kstr]
        curr_r = [float(i) for i in curr_rstr]
        ks.append(curr_k)
        rs.append(curr_r)

    curr_tempstr = tempstr[i]
    curr_kstr = curr_tempstr.split("K:")[1].split("R:")[0]
    curr_kstr = curr_kstr.replace('\n','').replace('[','').replace(']','').replace(';',',').split(', ')
    curr_rstr = curr_tempstr.split("K:")[1].split("R:")[1].split('Warping images')[0]
    curr_rstr = curr_rstr.replace('\n','').replace('[','').replace(']','').replace(';',',').split(', ')
    curr_k = [float(i) for i in curr_kstr]
    curr_r = [float(i) for i in curr_rstr]

    x = 0
    yaw = []
    pitch = []
    roll = []
    k1 = []
    offsetx = []
    offsety = []
    f = []
    s = []



    #TODO: expand the string to fill in these lists

    with open("reference.json") as json_File:
        json_data = json.load(json_file, object_pairs_hook = OrderedDict)

    poly = [[0]] * 10
    alist = [1]
    poly.insert(0, alist)

    for key in json_data.keys():
        for key2 inf json_data[key]:
            if key2 == "global":
                json_data[key][key2]['vig_poly_red'] = poly
                json_data[key][key2]['vig_poly_green'] = poly
                json_data[key][key2]['vig_poly_blue'] = poly
                json_data[key][key2]['sensorwidth'] = im.size[0]
                json_data[key][key2]['sensorheight'] = im.size[1]
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



if __name__ == "__main__":
    parse(sys.argv[1], sys.argv[2])
