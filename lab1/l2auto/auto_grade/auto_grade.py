#!/usr/bin/python3

import os, time, calendar, datetime
from datetime import date, timedelta, datetime
from changeto_testlocation import change_to_test_location, locate_exe
from lab2_grade import lab2_grade, lab_missing_file_check, lab_help_message_check
from get_id import get_id
import operator

#
#  Configuration directions
#
#  1. Set the base_name to point to the directory above the current directory
#     -- that is, the directory that contains the file "Grader".
#
#  2. Set "normal_deadline", if necessary
#     -- check early_day_limit and late_day_limit
#

# base_name must end with a slash ("/")
base_name = "/storage-home/a/as331/Comp421/lab1/l2auto/"

# The on-time due date for the assignment
normal_deadline = date(2024,10,23)    # set annually

#
# Stuff after this point should be set when the lab handout changes or 
# the software changes.
#

CORR_SCORE = 30   # max points for correctness
EFF_SCORE  = 20   # max points for effectiveness

blocks_dir = "auto_grade/blocks/"

test_dir = base_name + blocks_dir

#
early_day_limit = timedelta(days=2)   # determined by the grading rubric
late_day_limit  = timedelta(days=5)   # determined by the grading rubric
archive_date    = date(2100,1,1)      # impossibly far in the future

def check_file_type(type):
    for cdir, dirs, files in os.walk('./'):
        for file in files:
            if type in file:
                return True
    return False

def manual_clean(submission):
    #remove the jar file if submitted in java
    if check_file_type('.java'):
        # change in jar file handling
        os.system('rm `find -name "*.jar"` >&/dev/null')
        
def detail_file_name(prefix,test):
    return prefix+test.split('.')[0].strip()+".txt"

def write_file_headers(prefix,k_values):
    for test in sorted_test:
        r = open(detail_file_name(prefix,test),"w")
        r.write("Comp 412, Lab 2, Results for block '"+test+"'\n")
        r.write("Import into Excel with tab separators\n")
        r.write("NetID\tName")
        for k in k_values:
            r.write("\t"+str(k))
        r.write("\n")
        r.close()

def run_test(submission,netid,name):
    global file_headers_written

    dir = test_dir
    sim = '/clear/courses/comp412/students/lab2/sim'
    num_regs = [3, 4, 5, 6, 8, 12, 16]

    prefix = base_name+"results/grader_details_"

    
    if file_headers_written == False:
        write_file_headers(prefix,num_regs)
        file_headers_written = True
    
    result = {}

    print("\nResult is a set of (k, cycle) pairs for each test block\n")
    for test in sorted(os.listdir(dir)):
        if not '.i' in test:
            continue
        result[test] = lab2_grade(dir+test,test,sim,num_regs,submission)

        # record result for this test
        r = open(detail_file_name(prefix,test),"a")  # note append mode
        r.write(netid+'\t'+name)
        for i in num_regs:
            r.write('\t'+str(result[test][i]))
        r.write("\n")
        r.close()

    return result
 
def get_input(file):
    f = open(file, 'r')
    input = ""
    while True:
        line = f.readline()
        if line == "":
            break
        if 'SIM INPUT' in line:
            input = line.split(':')[1]
            break
    return input.strip()

def get_ref_cycles():
    num_regs = [3, 4, 5, 6, 8, 12, 16]
    lab_loc = '/clear/courses/comp412/students/lab2/'
    lab_ref = lab_loc + 'lab2_ref'
    lab_sim = lab_loc + 'sim'
    dir = test_dir
    results = {}

    print ("==================================================")
    print("Running lab2_ref to establish effectiveness baselines")
    for test in sorted(os.listdir(dir)):
        results[test] = {}
    for test in sorted(os.listdir(dir)):
        test_file = dir+test
        input = get_input(test_file)
        for r in num_regs :
            os.system(lab_ref + ' -w ' + str(r) +' '+ test_file  + ' | ' + lab_sim + ' -r ' + str(r) + ' ' + input  +' | grep cycles > out')
            f = open('out', 'r')
            line = f.readline()
            f.close()
            #print("lab2_ref @ k = ",r,":\t",line[:len(line)-2])
            results[test][str(r)] = line.rsplit(' ', 2)[1]
    os.system('rm -rf out')

    return results

def average_result(result, ref_result):
    min_constant = 1
    dir = test_dir
    sum = 0.0
    count = 0
    for block in sorted(os.listdir(dir)):
        subsum= 0.0
        subcount = 0
        for test in result[block] :
            cycle = float(result[block][test])
            ref_cycle = float(ref_result[block][str(test)])
            subsum = subsum + min(min_constant, (cycle - ref_cycle)/ref_cycle)
            subcount = subcount + 1
        subsum = subsum/subcount
        sum += subsum
        count += 1
    return sum/count
    
def check_correctness(result):
    dir = test_dir
    total_test = 0
    for item in os.listdir(dir):
        total_test = total_test + 1
    total_test *= 7; # 7 is the length of num_regs
    correct_count = total_test
    for block in result.keys():
        for test in result[block]:
            if result[block][test] == '100000':
                correct_count = correct_count - 1
            #print str(block) + '===' +str(test) +'  '+ result[block][test]

    #print '======' + str(correct_count) + '======' + str(total_test)
    return 100.0 * correct_count / total_test

def main():
    global sorted_test
    global file_headers_written

    # this process runs in the directory of the submitted tar files...
    root = os.getcwd()

    # To preserve partial runs, it plays an intricate game of opening and
    # closing the detailed files of results on each test block.
    # This flag lets run_test() know when it needs to write the file headers
    # in each of the detailed files.
    file_headers_written = False
    
    if not os.path.isdir(base_name):
        print('\nNeed to set "base_name" in auto_grade/auto_grade.py\n\n')
        exit(-1)

    lab_ref = '/clear/courses/comp412/students/lab2/lab2_ref'
    sim = '/clear/courses/comp412/students/lab2/sim'
    ref_results = get_ref_cycles()
    print ("Lab 2 Autograder: Using blocks in ./auto_grade/blocks/\n")        

    # Write the headers on the Scores file
    result_dir = base_name + "results/"
    Scores = open(result_dir+"grader_points.txt", 'w')
    Scores.write("COMP 412, Lab 2 Autograder, Points by NetID\n")
    Scores.write("Import into Excel with tab separators\n\n")
    Scores.write("Netid\tName\tConforms\tCorrectness\tEffectiveness\tDate\tDays Late\n")

    # Do this once and preserve it
    sorted_test = sorted(os.listdir(test_dir))

    # Because the files are renamed by the submit scripts, this order corresponds
    # to NetID order, which makes all of the files have the same order...

    failed = []  # list of submissions that do not work
    
    for submission in sorted(os.listdir('./')):  
        if os.path.isdir(submission):
            continue

        print ("==================================================")
        # unpack the tar file and cd to directory
        archive_date = change_to_test_location(submission) 
        name, ID, conf, keep_processing = get_id()

        if ID == "":
            ID = submission.split('_')[0].strip()
        if name == "":
            name = ID

        if conf == -100: # submission rejected for multiple READMEs
            print("Submission",submission,"rejected.")
            print("NetId derived from archive name is",ID)
            
        if keep_processing:
            print("Name: "+name+"\tNetID: "+ID,end="")
            print("\tDate From Files: ",str(archive_date))

            manual_clean(submission) # find and delete jar files (s.b. from source)

            print("\n------------------------------------------------------------")
            print("Output from building executable, if necessary")
            
            if not locate_exe(submission) == -1:
                print("-----------------------------------------------------------\n")
                result = run_test(submission,ID,name)

                corr_pct = check_correctness(result) / 100
                corr_pts = round(corr_pct * CORR_SCORE,2)

                eff_pct = min(100,100*(1-average_result(result, ref_results))) / 100
                eff_pts = round(eff_pct * EFF_SCORE,2)

                print("\nCorrectness points:  \t"+str(corr_pts))
                print("Effectiveness points:\t"+str(eff_pts))

                # check for help message and missing file message, cuz it angers me
                mf = lab_missing_file_check()
                hm = lab_help_message_check()

                if conf < 0 or mf != 1 or hm != 1:
                    print("\nSubmission loses 10 points for conformance problems")
                    conf_str = "\t-10\t"
                else:
                    conf_str = "\t0\t"
                    
                Scores.write(ID+'\t'+name+conf_str+str(corr_pts)+'\t'+str(eff_pts))

                # days late calculation
                diff = archive_date - normal_deadline
                if diff < -early_day_limit:
                    diff = -early_day_limit
                elif diff > late_day_limit:
                    diff = late_day_limit

                Scores.write("\t"+str(archive_date)+"\t"+str(diff.days)+"\n")
                print ('\nFinished submission ', submission)
            else:
                print("Submission failed to build correctly.")
                failed.append(ID)
        else:
            print("-----------------------------------------------------------\n")
            failed.append(ID)


        # clean up everything that was created during testing
        os.chdir(root)
        fixed_submission = submission.replace(" ", "\ ").replace("(", "\(").replace(")", "\)").replace("'", "\\'")
        folder = submission.split('.', 1)[0]
        fixed_folder = fixed_submission.split('.', 1)[0]
        os.system('rm ' + fixed_folder + ' -rf')

    print ("==================================================\n")
        
    Scores.close()

    # Write the list of netids that failed to work
    Failed_file = open(result_dir+'grader_failed.txt', 'w')
    Failed_file.write("COMP 412, Lab 2 Autograder, NetIDs of Failed Submissions\n")

    for id in failed:
        Failed_file.write(id+ '\n')
    Failed_file.close()

    print("Grading run complete.\n")

if __name__ == "__main__":
    main()
