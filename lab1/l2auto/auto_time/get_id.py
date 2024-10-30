# Part of the COMP 412 autograder

import os

def get_id():  # rewritten, December 2023

    tmp_file = 'tmpdump'
    name = ""
    netid = ""
    
    # find the README file
    # Note that the expression in the find command also discovers README.md
    # for those github users who end up with a Markdown file.
    # It should be transparent

    os.system("find . -iname \"README*\" > " + tmp_file)
    f = open(tmp_file, 'r')
    line = f.readline()

    # check for missing README
    if line == "":
        f.close()
        os.system('rm ' + tmp_file)
        print("\n***\tNo README file found, -50% on conformance\n")
        return "", "", -50, True # loss of 50% conformance points

    first_line = line.rstrip()
    
    line_ct = 0
    while line != "":
        line_ct += 1
        line = f.readline()

    if line_ct > 1:
        print("\n***\tThe submission contains multiple README files")
        print("\tPlease correct the submission so that it only includes")
        print("\tthe material for the current programming assignment.")
        print("\t(not, for example, the simulator, autograder, or other stuff)")
        print("\nSubmission rejected on conformance grounds.\n")
        return "", "", -100, False

    readme = open(first_line, 'r') # shouldn't need a try since 'find' found it

    line = readme.readline()
    while line != "":
        if line.find("NAME:") >= 0:
            name = line.rsplit(':', 1)[1].strip()
        elif line.find("NETID") >= 0:
            netid = line.rsplit(':', 1)[1].strip()

        line = readme.readline()        

    if name == "":
        no_name = -20
    else:
        no_name = 0
        
    if netid == "":
        no_id = -20
    else:
        no_id = 0
        
    if name != "" and  name[0] == '<':
        name = name[1: len(name)-1]
    if netid != "" and netid[0] == '<':
        netid = netid[1: len(netid)-1]

    deduct = no_name + no_id
    if deduct != 0:
        print("\n\tProblem determining NAME and/or NETID")
        print("\tDeduct "+str(deduct)+"% of conformance points\n")

    return name, netid, deduct, True
