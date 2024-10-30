# Part of the COMP 412 Lab 2 autotimer (and autograder)

import os, datetime

# helper function to search directory structure for maximum date
def find_latest_mod_date(p,max_date_yet,depth):
    # list files in this directory

    files = os.listdir(p)
    d = depth
    for f in files:
        t = str(p) + str(f)

        if os.path.isfile(t):       # take its modification time

            mod_date = datetime.datetime.fromtimestamp(os.path.getmtime(t)).date()

            if mod_date > max_date_yet:
                max_date_yet = mod_date

        elif os.path.isdir(t):  # recur into the directory
            mod_date, d = find_latest_mod_date(t+'/',max_date_yet,d+1)

            if mod_date > max_date_yet:
                max_date_yet = mod_date

    return max_date_yet, d

#submission is the name of a given tar archive
def change_to_test_location(submission):
    
    #in case of "frag1 frag2 (frag3) frag4's"
    fixed_submission = submission.replace(" ", "\ ").replace("(", "\(").replace(")", "\)").replace("'", "\\'")
    folder = submission.split('.', 1)[0]
    fixed_folder = fixed_submission.split('.', 1)[0]

    # if folder exists, remove it to restart what we are doing
    if os.path.exists(folder):
        cmd = 'rm ' + fixed_folder + ' -rf'
        os.system(cmd)

    # make dir and cp
    #print('========' + submission)
    #print('========' + folder)
    os.makedirs(folder)
    cmd = 'cp ' + fixed_submission + ' ' + fixed_folder
    os.system(cmd)
    #print(fixed_submission + ' '+ submission + ' ' + fixed_folder +' ' + folder)

    # change dir
    os.chdir(folder)
    # unzip or untar
    if '.zip' in fixed_submission:
        cmd = 'unzip ./' + fixed_submission + ' > /dev/null'
    if '.tar' in fixed_submission:
        if 'tar.gz' in fixed_submission:
            cmd = 'tar xfvz ./' + fixed_submission + ' >& /dev/null'
        elif 'tar.bz' in fixed_submission:
            cmd = 'tar xfv ./' + fixed_submission + ' >& /dev/null'
        else:
            cmd = 'tar xfv ./' + fixed_submission + ' >& /dev/null'
    elif '.tgz' in fixed_submission:
        cmd = 'tar xfv ./' + fixed_submission + ' >& /dev/null'
    os.system(cmd)

    # remove the tar file so that its date does not get copied
    cmd = 'rm -rf ' + fixed_submission
    os.system(cmd)
    
    # find latest file modification date
    submission_date, depth = find_latest_mod_date("./",datetime.date(2020,1,1),1)

    if datetime.date(2020,1,1) == submission_date:
        print("\n***\tProblem reading files, data is inaccurate.\n")

    if depth > 5:
        print("\n***\tTar archive has more than 5 levels of subdirectories.")
        print("\tMay indicate a poorly constructed archive.")
        
    

    return submission_date
    
def locate_exe(submission):
    global language

    language = ""
    
    #must have either makefile or 412alloc script
    subDir = os.getcwd()
    os.system('find . -iname "makefile" > tmp')
    f = open('tmp', 'r')
    line = f.readline()
    next = f.readline()
    while next != "":
        if len(next) < len(line):
            line = next
        next = f.readline()            
    f.close()

    os.system('rm tmp')
    if line != "":
        print('--- building executable ---')
        os.chdir(line.strip().rsplit('/', 1)[0])
        os.system('make clean')
        os.system('make build')
        scan_makefile()
    
    print('--- built executable; should be ready to run ---\n')

    # Need to move back to the top-level directory before looking for
    # the script or executable. If the submission contains a subsystem
    # that has a makefile, it moved down to the makefile's directory and
    # executed "make clean" and "make build". If that subsystem is
    # not where 412alloc lives (e.g., the submission includes a copy of
    # the simulator source code or something similar), then it is below
    # the point in the directory tree where it will find 412alloc.
    # So, 
    os.chdir(subDir)

    os.system('find . -name "412alloc" > tmp')

    f = open('tmp', 'r')
    line = f.readline()
    next = f.readline()
    while next != "":
        if len(next) < len(line):
            line = next
        next = f.readline()            
    f.close()
    os.system('rm tmp')
    if line == "":
        print(submission + ' didn\'t folllow the instructions: no 412alloc')
        return -1
    
    #change to dir that contains makefile/412alloc
    os.chdir(line.strip().rsplit('/', 1)[0])
    os.system('chmod +x 412alloc')
    if language == "":
        scan_shell_script_file()

    if language == "":
        language = "unknown "
    
    # verify that we are back where we belong
    #os.system('pwd')

    return 0

def scan_makefile():
    global language

    #print("\nIn scan_file():",)
    found_mf = 0
    found_java = 0
    found_cpp  = 0
    found_c    = 0

    try: 
        mf = open("Makefile")
        found_mf = 1
    except:
        try: 
            mf = open("makefile")
            found_mf = 1
        except:
            found_mf = 0

    if found_mf == 1:
        line = mf.readline()
        while line != "":
            if line.find("java") > -1:
                found_java = 1
            elif line.find(".cpp") > -1:
                found_cpp = 1
            elif line.find(".c") > -1 and line.find(".class") == -1:
                found_c = 1
            line = mf.readline()
        mf.close()

    if found_java == 1:
        #print("Language appears to be java")
        language += "java "
    if found_cpp == 1:
        #print("Language appears to be C++")
        language += "c++ "
    if found_c == 1: 
        #print("Language appears to be C")
        language += "c "

def scan_shell_script_file():
    global language

    #print("\nIn scan_file():",)
    found_fe = 0
    found_java = 0
    found_python = 0

    try:
        fe = open("412alloc")
        found_fe = 1
    except:
        language = "unknown"

    if found_fe == 1:
        try:
            line = fe.readline()
            
            while line != "":
                #print("\t'"+line+"'")
                if line.find("python") > -1:
                    found_python = 1
                elif line.find("java") > -1:  
                    found_java = 1
                line = fe.readline()
        except:
            # 412alloc is executable binary code, so do nothing
            found_fe = 1  # a nop to make the syntax work
        fe.close()

    if found_java == 1:
        #print("Language appears to be java")
        language += "java "
    if found_python == 1:
        #print("Language appears to be python")
        language += "python "
        
def  get_language():
    global language

    return language

            
        
