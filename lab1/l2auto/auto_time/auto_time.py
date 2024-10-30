#!/usr/bin/python3

import os, time, calendar, datetime, sys

from datetime import datetime
from time import process_time
from changeto_testlocation import change_to_test_location, locate_exe, get_language

from get_id import get_id
import operator

#
# Code to take timing measurements on the lab submission, using the SLOCs test set
# Runs each submission multiple times.
# Runs blocks in decreasing size, which seems to improve accuracy.
#    (seems mystical, but may be a memory hierarcy effect -- kdc)
#


#
# Configuration parameters
#

# base_name contains the path to the directory where this file tree is installed
# It should be one level above the directory that holds this code.

base_name = "/storage-home/a/as331/Comp421/lab1/l2auto/"

# These constants encode the number of points for Efficiency and
# Scalabilty. They should be checked every year to ensure that they
# agree with the grading rubric.
#
EFF_SCORE   = 10
SCALE_SCORE = 10


# Locations for test blocks (blocks) and timing blocks (timing)
# These are relative to the directory in base_name

blocks_dir = "auto_grade/blocks/"
timing_dir = "auto_time/timing_blocks/"

# Two routines used to check for correct answers on the first run of 
# each block.
#
# get_answer() finds the //OUTPUT: comment in a block & returns the answer
# check_correctness() compares the output from running the allocated block
#    against the pre-recorded answer (from get_answer)
#
def get_answer(path,block):
    # This function relies heavily on the fact that the timing blocks
    # produce a single answer -- one number.
    path = path + block
    answer = 0

    try:
        f = open(path,'r')
    except:
        print("Could not open test block",block)
        print("Indicates a configuration problem.")
        return 0

    line = f.readline()
    i = 0
    while line != "":
        position = line.find("//OUTPUT:")
        if position > -1:
            answer = int(line[position+9:])
            break
        line = f.readline()
        i += 1

    return answer

def check_correctness(out_name,answer):
    # out_name is the file of allocated ILOC code
    command = "~comp412/students/lab2/sim "+out_name+" >&out"
    os.system(command)

    try:
        out = open("./out",'r')
    except:
        print("Error reading simulator output file in check_correctness()")
        print("Autotimer exits")
        exit(-1)

    is_correct = False
    
    line = out.readline()
    llen = len(line)
    line = line[0:llen-1]
    
    while line != "":
        if line.isnumeric():
            result = int(line)
            if result == answer:
                is_correct = True
                #print("bingo! "+str(result)+" == "+str(answer))
            else:
                is_correct = False
                #print("wrongo! "+str(result)+" != "+str(answer))
            break
        line = out.readline()

    os.system("rm ./out") # clean up
    return is_correct

def run_timing_block(block_name,block_num,check):
    global correct_answers
    
    path = base_name + timing_dir
    
    if check == False:
        command_line = "timeout 60.0s ./412alloc 15 "+path+block_name+" >&/dev/null"
    else:
        tmpname = "./"+current_id+"-"+block_name
        command_line = "timeout 60.0s ./412alloc 15 "+path+block_name+" >&"+tmpname
        
    start_tic = time.perf_counter()
    os.system(command_line)
    stop_tic  = time.perf_counter()
    elapsed = stop_tic - start_tic 

    if check:
        result = check_correctness(tmpname,correct_answers[block_num])
        os.system("rm "+tmpname)

        if result == False:  # pass failure signal back up chain of calls
            print("Incorrect result for block '"+block_name+"'.")
            elapsed = -1

    return elapsed
        
def run_test(submission):
    global scaling
    global t_names
    global t_sizes

    # have already found and built the executable
    #record name and netid in result file
    result_file.write(current_id + '\t' + current_name)

    # Scalability testing
    scales = True

    t_times =  [1000000, 1000000, 1000000, 1000000,  1000000,  1000000,  1000000,  1000000]
    timeout = [False, False, False, False, False, False, False, False]

    n_trials = 5
    print("Testing Scalability:\t(minimum time of "+str(n_trials)+" runs)\n")

    # To change the number of repeats of each file, adjust n_trials, above
    for i in range(0,n_trials):
        n = 7
        while n > -1:
            if timeout[n] == False:
                if i == 0:   # check correctness on 1st run of big block
                    seconds = run_timing_block(t_names[n],n,True)
                else:
                    seconds = run_timing_block(t_names[n],n,False)
            else:
                seconds = 60

            if seconds == -1: # failed correctness check
                t_times[n] = 60
                timeout[n] = True
                scales = False
                    
            elif seconds < t_times[n]:
                t_times[n] = seconds

            elif seconds > 59 and timeout[n] == False:  # timeout
                timeout[n] = True
                print("\n\tTimed out on block "+t_names[n])
                scales = False


            n = n -1

    for i in range(0,8):
        print("\t"+t_names[i]+":  \t"+str(t_times[i])[0:6]+" seconds")
        result_file.write("\t"+str(t_times[i])[0:6])

    print(" ")  # pretty up the output

    if scales == False:
        failed_file.write(current_id+"\t"+current_name+"\n")
        result_file.write("\t--\t--\t0\t0\n")
        # quick exit (didn't want to indent all that code for the else)
        return 0  

    # analyze scaling
    linear_ct = 0
    noninc_ct = 0
    quad_ct   = 0
    timed_out = 0

    scaling   = ""
    language  = "\t"
    
    for i in range(0,7):
        if t_times[i] == 60:
            timed_out = 1
        ratio = t_times[i+1]/t_times[i]
        if ratio < 1:
            noninc_ct +=1
        if ratio < 2.3:
            linear_ct += 1
        elif ratio > 3.6:
            quad_ct   += 1
        else:
           noninc_ct  += 1

    if timed_out == 1:
        scaling       = " timed-out "
        language      = "timed-out"
        scale_points  = 0
        eff_points    = 0

    elif noninc_ct == 0:
        scaling      += " linear"
        scale_points  = 100
    elif noninc_ct == 1:
        scaling      += " linear-w-1-jump"
        scale_points  = 100
    elif quad_ct > 2: 
        scaling       = " quadratic"
        scale_points  = 0
    else:
        scaling       = " anomaly"
        scale_points  = 0

    if timed_out == 0:
        # analyze efficiency

        time = t_times[7] 
        language = get_language()

        if language.find("python") > -1:
            if time <= 8.0:
                eff_points = 100
            elif time >20.0:
                eff_points = 0
            else:  # 0.12 is (20 - 8) / 100
                eff_points = 100 - (time - 8.0) / 0.12  

        elif language.find("java") > -1:
            if time <= 4.75:
                eff_points = 100
            elif time > 12.0:
                eff_points = 0
            else:  # 0.0725 is (12 - 4.75) / 100    
                eff_points = 100 - (time - 4.75) / 0.0725
            
        elif language.find("c++") > -1:
            if time <= 2.0:
                eff_points = 100
            elif time > 4.0:
                eff_points = 0
            else:  # 0.02 is (4 -2) / 100
                eff_points = 100 - (time - 2) / 0.02
        else: # all others are between 1 and 2 seconds
            if time <= 1.0:
                eff_points = 100
            elif time > 2.0:
                eff_points = 0
            else:  # 0.01 is (2 - 1) / 100
                eff_points = 100 - (time - 1) / 0.01    

    # make zeros print as 0.0
    scale_points = round(scale_points * SCALE_SCORE / 100.0,2)
    eff_points   = round(eff_points * EFF_SCORE / 100.0,2)

    if len(str(scale_points)) > 6:
        print("Scaling score is \t"+str(scale_points)[0:5])
    else:
        print("Scaling score is \t"+str(scale_points))

    if scale_points == 0.0:
        print("\tTiming results need to be examined manually.\n")
        
    if len(str(eff_points)) > 6:
        print("Efficiency score is \t"+str(eff_points)[0:5]+"\t( "+language+")")
    else:
        print("Efficiency score is \t"+str(eff_points)+"\t( "+language+")")

    # record scaling and efficiency points in results file
    if noninc_ct > 0:
        scaling += " anomaly"
        print("\n\tAnomalous behavior: "+str(noninc_ct)+" inputs showed no growth")
        result_file.write("\t"+language+"\t"+scaling+"\t"+str(scale_points)+"\t"+str(eff_points)+"\t*\n")
    else:
        result_file.write("\t"+language+"\t"+scaling+"\t"+str(scale_points)+"\t"+str(eff_points)+"\n")
    
    return 0


def main():
    global root
    global tests
    global blocks_dir
    global base_name
    global current_name
    global current_id
    global result_file
    global failed_file
    global scaling
    global t_names, t_times, correct_answers
    

    root = os.getcwd()

    #for each submission:
    #1. make a tmp dir
    #2. cp the tar ball to the dir
    #3. extract and the tar ball
    #4. locate the makefile or the executable
    #5. ready to run with the executable

    print('Lab 2 Autotimer: using Scalability SLOCs blocks\n')

    if not os.path.isdir(base_name):
        print('\nNeed to set "base_name" in auto_time/auto_time.py\n\n')
        exit(-1)
    
    # set up the output files
    result_path = base_name + 'results/'

    try: 
        result_file = open(result_path + 'timer-points.txt','w')
        failed_file = open(result_path + 'timer-failed.txt','w')
    except:
        print("Failed to open result file.")
        print("autotimer terminates.")
        exit(-1)

    # write file headers
    result_file.write('Lab 2 Autotimer Results\n')
    result_file.write('Import into Excel with tab separators\n\n')
    result_file.write('NetId\tName\tT1k\tT2k\tT4k\tT8k\tT16k\tT32k\tT64k\tT128k\tLang.\tScaling Pts\tEff Pts %\n')

    failed_file.write('Lab 2 Autotimer Results\n')
    failed_file.write('List of NetIDs for labs that produced incorrect results\n\n')
    failed_file.write('Name\tNetId\n')

    # test-set specific initializations
    t_names =  ["T1k.i","T2k.i","T4k.i","T8k.i","T16k.i","T32k.i","T64k.i","T128k.i"]
    t_sizes =  [1, 2, 4, 8, 16, 32, 64, 128]

    # get number of lines processed by lab1_ref for each block
    print("Gathering operation counts with lab2 simulator.")
    correct_answers = [0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(0,len(correct_answers)):
        correct_answers[i] = get_answer(base_name+timing_dir,t_names[i])

    print('\n=======================================================================')
        
    for submission in sorted(os.listdir('./')):
        if os.path.isdir(submission):
            continue

        print('Testing submission: ' + submission)
        submission_date = change_to_test_location(submission)
                
        current_name, current_id, deduct, keep_processing = get_id()

        if current_id == "":
            current_id   = submission.split('_', 1)[0]
        if current_name == "":
            current_name = current_id

        if keep_processing:
            
            print('Name: ' + current_name + ', NetID: ' + current_id,end="")
            print('\tDate From Files: ' + str(submission_date) + '\n')

            if not locate_exe(submission) == -1:
                dummy = run_test(submission)
            else:
                print('submission failed to build correctly')
                print('likely a problem with tar file, make file, or script')
                failed_file.write(current_name + '\t' + current_id+"\t(failure to build)\n")
        else:
            failed_file.write(current_name + '\t' + current_id+"\t(conformance)\n")

        print('\nfinished timing run on submission ' + submission )

        print('=======================================================================')

        #clean up everything that was created during testing
        os.chdir(root)
        fixed_submission = submission.replace(" ", "\ ").replace("(", "\(").replace(")", "\)").replace("'", "\\'")
        folder = submission.split('.', 1)[0]
        fixed_folder = fixed_submission.split('.', 1)[0]
        os.system('rm -rf ' + fixed_folder)


    # close the grading files
    result_file.close()
    failed_file.close()

    print('\nTiming run complete.\n')
    exit(0)
    
if __name__ == "__main__":
    main()
