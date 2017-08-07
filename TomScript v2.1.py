"""
TomScript for easy using GitHub

NOTE:
    THE PROJECT FILE MUST HAVE A .txt FILE WITH JUST A LINE-BY-LINE LIST OF 
    LIBRARIES THAT IT REQUIRES TO FUNCTION. NOTHING MORE, NOTHING LESS! THE 
    LIST MUST BE IDENTICAL TO THE SUFFIX CORRESPONDING TO GITHUB!!
"""

import glob
from git import Repo

#==============================================================================
# Contents
#==============================================================================

# Contents of functions in this script
# It is also worth noting that I would expect the functions to be performed
# in the order they are listed below.
def contents():
    '''
    All functions take the single argument repo. This argument is used to determine the repository
    to which action is to be taken. The repo argument must always be entered in quotation marks,
    e.g. status('repo')
    
    Functions:
        
        1. status(repo)
        
        2. newbranch(repo)
        
        3. choosebranch(repo)

        4. add(repo)
        
        5. commit(repo)
        
        6. push(repo)
        
    Compound Functions: #WIP
        
        1. compush(repo)
        
        2. addcompush(repo)
        
    Callable Parameters:
        
        - project
        - project_URL
        - proj
        - repo_list
        - libraries
        - libs

    If function is not working, ensure argument input is in quotation marks.
    Use help(function) e.g. help(push) for more detailed information about that function.
    
    '''
    return help(contents)

def workflow():
    '''
    
    Generalised workflow:
        
        > Project repository and associated Library repositories are cloned onto local drive:
            - this is called the 'local working directory'
            
        > Use the choosebranch [newbranch] functions to choose [name] the branch of the project you will be working on.
        
        > Files in the repositories may now be edited, and new features added to the local repository folder(s). 
        
        > New files must be added to the repository on a Git-level. This means they must be 'added' to 'stage' them for being committed.
        
        > Use the add(repo) function to add files.
        
        > Use the commit(repo) function to commit files to the repository
        
        > Use the push(repo) function to push files locally from your computer back up to the GitHub cloud.
    
    Note: repo refers to repository, that is, the area on GitHub where all the associated files to that project/library are hosted.
    '''
    return help(workflow)

#==============================================================================
# Project and libraries
#==============================================================================

print('')
print('Ensure that input is in quotation marks...')

# User input section ----------------------------------------------------------
project = input("Project Name:")
project_URL = 'https://github.com/DigicoUK/' + project

###############################################################################
directoryprefix = 'Z://new_work_area_12/'
local_directory = directoryprefix + 'project//' + project + '/'
###############################################################################

print('Cloning project...')
proj = Repo.clone_from(project_URL, local_directory)

# Extracting libraries information --------------------------------------------
print('Cloning libraries...')
repo_list = glob.glob(local_directory+'*')

libs_file = filter(lambda x: 'Lib' in x, repo_list)
libs_extract = ''.join(str(e) for e in libs_file)
libs_required = open(libs_extract, "r")

libraries = libs_required.readlines()
libraries = [x.strip('\n') for x in libraries]

# Names of required project libraries' URLs -----------------------------------
lib_URL = []

for i in range(len(libraries)):
    lib_URL.append('https://github.com/DigicoUK/firmware_library_' 
                     +  libraries[i] + '.git')
    
# Automatic cloning of the libraries
libs = []
for i in range(len(lib_URL)):
    libs.append(Repo.clone_from(lib_URL[i],
                                directoryprefix + 'Libs//' 
                                + libraries[i]))

libs.append(proj)
libraries.append(project)
#==============================================================================
# Function section 
#==============================================================================
"""
                                        
The function section is split into three parts:
    1. Atomic Functions
    2. User Functions
    3. Compound functions
    
Atomic functions rely entirely on the lists of files and repository paths, and
the arguments input. Debugging should begin here, as the other functions are 
logical interpretations of these. 

User functions each follow the same logic format. These are unlikely to break
in the result of bugs being found, and it is these functions which are brought
to command by the user.

The compound functions are amalgamations of the user functions. This will speed
up large volumes of adds/commits to multiple branches in multiple repo's.


"""
print('-----------------------------------------------')
print('Type contents() for a list of functions.')
print('Type workflow() for help in functional logic.')

#==============================================================================
# Atomic functions
#==============================================================================

# Create identical local and remote (on GitHub) branch.
def branch_creator(repository, branch):
    
    j = libraries.index(repository)
    f = libs[j]
    
    f.create_head(branch)
    f.git.checkout(branch)
    
    origin = f.remote('origin')
    remote_branch = origin.git.push('origin',branch)
    return remote_branch

# Add files to local branch
def git_add(repository):
    
    j = libraries.index(repository)
    f = libs[j]
    
    add_changes = f.git.add('.')    
    return add_changes

# Commit changes to local branch
def git_commit(repository, message):
    
    j = libraries.index(repository)
    f = libs[j]
    
    make_commit = f.git.commit(m = message)    
    return make_commit

# Push to remote branch
def git_push(repository):
    
    j = libraries.index(repository)
    f = libs[j]
    
    origin = f.remote('origin')
    push_to = origin.push()   
    return push_to

# Checkout branch
def git_checkout(repository, branch):
    
    j = libraries.index(repository)
    f = libs[j]
    
    selection = f.git.checkout('origin/'+branch, b = branch)    
    return selection

# Add tags
def tag_maker(repository):
    tagname = input('Tag name:')
    tagmessage = input('Tag description:')
    
    j = libraries.index(repository)
    f = libs[j]
    
    new_tag = f.create_tag(tagname, message=tagmessage)    
    return new_tag

#==============================================================================
# User functions
#==============================================================================

def status(repo):
    '''
    Status report of changes made since repository was cloned.
    
    Parameters
    ----------
    repository : string
        Repository name (e.g. DmiAdc) command is intended to be applied to.
    
    Returns
    -------
    out : status update
        Includes current branch, committs since clone, condition of working
        tree
        
    Notes
    -----
    This function cannot be used under the 'all' function. Use it only for 
    individual repositories.
    '''      
    
    if repo == 'all':
        return 
    else:
        j = libraries.index(repo)        
        f = libs[j]
    
        status = f.git.status()
        if 'branch master' in status:
            print('Action on master branch forbidden. Use choosebranch() function to change.')
            return
        else:               
            return status

def newbranch(repo):
    '''
    Chooses branch to track remote branch updates from origin
    
    Parameters
    ----------
    repo : string
        Repository name (e.g. DmiAdc) command is intended to be applied to.
    
    Returns
    -------
    out : checkout
        Performs Git 'checkout' routine, switching branch changes are committed
        to
    '''
    
    branchname = input('Name of branch to be created:')
    
    if repo == 'all':
        print('This may take a moment...')
        for x in libraries:
            branch_creator(x, branchname)
    else:     
        branch_creator(repo, branchname)
    return
    

def choosebranch(repo):
    '''
    Chooses branch to track remote branch updates from origin
    
    Parameters
    ----------
    repo : string
        Repository name (e.g. DmiAdc) command is intended to be applied to.
        
    Returns
    -------
    out : checkout
        Performs Git 'checkout' routine, switching branch changes are committed
        to
    '''
    
    branchname = input('Enter name of working branch:')
    
    if repo == 'all':
        print('This may take a moment...')
        for x in libraries:
            git_checkout(x, branchname)
    else:     
        git_checkout(repo, branchname)
    return


def tag(repo):
    '''
    Chooses branch to track remote branch updates from origin
    
    Parameters
    ----------
    repo : string
        Repository name (e.g. DmiAdc) command is intended to be applied to.
        
    Returns
    -------
    out : checkout
        Performs git 'checkout' routine, switching branch changes are committed
        to
    '''
    
    tag_maker(repo)
    return


def add(repo):
    '''
    Add files into the new local repository. This stages them for the first 
    commit
    
    Parameters
    ----------
    repository : string
        Repository name (e.g. DmiAdc) command is intended to be applied to.
    
    Returns
    -------
    out : files added
        Files moved into the 'new_directory' are now staged in the repository
        
    Notes
    -----
    This must be followed by git_commit('message')
    '''   

    if repo == 'all':
        print('This may take a moment...')
        for x in libraries:
            git_add(x)      
    else:     
        git_add(repo)
    return


def commit(repo):
    '''
    Commit changes to the local repository
    
    Parameters
    ----------
    repository : string
        Repository name (e.g. DmiAdc) command is intended to be applied to.
        
    message : string
        Make the message as detailed as possible, keeping track of changes. 
        Ensure the message is enclosed by 'quotation marks'
    
    Returns
    -------
    out : Commit made
        We are now one commit ahead of the previous version of the repository
    '''
    
    msg = input('Message to commit:')
    
    if repo == 'all':
        print('This may take a moment...')
        for x in libraries:
            git_commit(x, msg)
    else:     
        git_commit(repo, msg)
    return


def push(repo):
    '''
    Push committed changes onto the chosen GitHub working branch
    
    Parameters
    ----------
    repository : string
        Repository name (e.g. DmiAdc) command is intended to be applied to.
    
    Returns
    -------
    out : push to remote branch
        Changes are pushed and visible on the working branch on GitHub
    '''

    if repo == 'all':
        print('This may take a moment...')
        for x in libraries:
            git_push(x)
    else:     
        git_push(repo)
    return

#==============================================================================
# Compound Functions
#==============================================================================

def compush(repo):
    
    '''
    Commit changes to the local repository and push changes out to remote branch
    
    Parameters
    ----------
    repository : string
        Repository name (e.g. DmiAdc) command is intended to be applied to.
        
    message : string
        Make the message as detailed as possible, keeping track of changes. 
        Ensure the message is enclosed by 'quotation marks'
    
    Returns
    -------
    out : Commit made
        We are now one commit ahead of the previous version of the repository
        
    out : push to remote branch
        Changes are pushed and visible on the working branch on GitHub
    '''
    
    message = input('Message to commit:')
    
    if 'branch master' in status(repo):
        print('Action on master branch forbidden. Use choosebranch() function to change.')
        return
    
    j = libraries.index(repo)
    f = libs[j]
      
    f.git.commit(m = message)
    origin = f.remote('origin')
    commit_and_push = origin.push()    
    return commit_and_push

def monty(repo):
    
    message = input('Message to commit:')

    if 'branch master' in status(repo):
        print('Action on master branch forbidden. Use choosebranch() function to change.')
        return
            
    j = libraries.index(repo)
    f = libs[j]
    
    f.git.add('.')  
    f.git.commit(m = message)
    origin = f.remote('origin')
    add_commit_push = origin.push() 
    return add_commit_push