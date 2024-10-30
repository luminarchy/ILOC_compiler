# Part of the COMP 412 Lab 2 autograder

import os

def check_output(alloc_output, correct_output):
    fa = open(alloc_output, 'r')
    fc = open(correct_output, 'r')
    line_a = ""
    line_c = ""
    is_bad = False
    while True:
        line_c = fc.readline()
        line_a = fa.readline()
        if 'cycle' in line_c:
            break
        if line_a == "":
            is_bad = True
            break
        if not line_a == line_c:
            is_bad = True
            break

    fa.close()
    fc.close()
    big_number = '100000'
    if is_bad == True:
        return big_number

    if not 'cycle' in line_a:
        return big_number

    return int(line_a.rsplit(' ', 1)[0].rsplit(' ', 1)[1])

#return number of cycles after allocation and checking the outputs
def lab2_grade(file, short_name, sim, num_regs, submission):
    #get input for simulator
    f = open(file, 'r')
    input = ""
    output = []

    while True:
        line = f.readline().strip()
        if line == "":
            break
        if '//SIM INPUT:' in line:
            input = line.split(':')[1]
            break

    f.close()

    result_file = ""
    if '/' in file:
        result_file = 'alloc_' +file.rsplit('/', 1)[1]
    else:
        result_file = 'alloc_' + file

    # get result without allocation
    correct_output = 'correct_output'
    os.system(sim + input + ' < ' + file + ' > ' + correct_output)

    # compare output with allocation to result without allocation
    # if same outputs, return number of cycles
    # if not same, return -1
    alloc_output = 'output_from_allocator'
    cycles = {} # dictionary to record num_reg to cycle mapping
    if len(short_name) > 6:
        print(short_name+":\t",end="")
    else:
        print(short_name+":\t\t",end="")
    for r in num_regs:
        #print 'checking ' + file + ' with ' + str(r) + ' registers, ',
        #
        # Run 412alloc
        os.system('timeout 300s ./412alloc ' + str(r) + ' ' + file + ' > ' + result_file)
        # Run the simulator on the allocated code
        os.system(sim + ' -r ' + str(r) + ' ' + input + ' < ' + result_file + ' > ' + alloc_output)
        # Check answers and cycles
        cycles[r] = check_output(alloc_output, correct_output)#outup comparison
        #print("k = ",r," took ",cycles[r],"cycles.")

    os.system('rm -rf ' + correct_output)
    print(cycles)
    return cycles

#=======================================================
# Code shamelessly stolen from l1ag

def check_missing_file_name(file_name):
    if not os.path.isfile(file_name):
        print("Check for missing file name produced no output")
        return 0

    o_file = open(file_name,'r');

    #look for "ERROR" in the file
    error_message_found = 0;
    while True:
        o_line = o_file.readline().strip(' ')

        if o_line == '':
            break;

        if o_line.find("Traceback") != -1:
            print("\nMissing file test produced a Traceback.")
            error_message_found = 0
            break

        if o_line.find("ERROR") != -1:
            error_message_found = 1

        o_line = o_line.lower()
        if error_message_found == 0 and o_line.find("error") != -1:
            print("\nProduced 'file not found' message, but ERROR was not in uppercase (1)")

    return error_message_found


def check_for_help_message(file_name):
    if not os.path.isfile(file_name):
        print("Check for missing help message check produced no output")
        return 0

    o_file = open(file_name,'r');

    #look for "-h" in the file
    found_h = 0
    found_x = 0

    while True:
        o_line = o_file.readline()  #.strip(' ')
        if o_line == '':
            break
        
        if o_line.find("-h") != -1:
            found_h = 1

        if o_line.find("-x") != -1:
            found_x = 1

    if found_x == 1 and found_h == 1:
        result = 1
    else:
        result = 0
        print("")
        if found_h == 0:
            print("Help message does not list '-h'")
        if found_x == 0:
            print("Help message does not list '-x'")
        
    return result

# Check to see if it handle a bad input file name gracefully
def lab_missing_file_check():
    
    # set stdin to /dev/null in case lab reads from terminal if open
    # fails. Use timeout as a hedge against other bad results from the open()
    fname = "./does_not_exist"
    command_line = 'timeout 20s ./412alloc 5 ' + fname + '.mine >& ./'+ fname+ '.output </dev/null'
    os.system(command_line)

    result = check_missing_file_name(fname+".output")
    return result

# Check to see if it prints out a complete help message
def lab_help_message_check():
    fname = "./helpmessage.output"
    command_line = './412alloc -h >& ./'+fname
    os.system(command_line)

    result = check_for_help_message(fname)
    return result


