



def parse(opencv_out, filename):
    # takes the <opencv_out> file as a string, parse it into a JSON file,
    # and write it into file with <filename>

    with open("reference.json") as json_File:
        json_data = json.load(json_file, object_pairs_hook = OrderedDict)
        


    data = json.dumps(json_data, indent=4)
    with open(filename, "w") as outfile:
        outfile.write(data)
        print data
        print "wrote above data to " + filename



if __name__ == "__main__":
    parse(sys.argv[1], sys.argv[2])
