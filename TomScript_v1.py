"""
TomScript for easy using GitHub
 
1. choose github repository and a new directory for local use
    >> run the python script
    >>> the repository is now saved locally in 'new_directory'
2. edit the files you wish off the repository locally (e.g. in ms word)
3. add the files into 'new_directory' (drag & drop, for now)
4. use the additor function 


NOTE:
    THE PROJECT FILE MUST HAVE A .txt FILE WITH JUST A LINE-BY-LINE LIST OF 
    LIBRARIES THAT IT REQUIRES TO FUNCTION. NOTHING MORE, NOTHING LESS! THE 
    LIST MUST BE IDENTICAL TO THE SUFFIX CORRESPONDING TO GITHUB!!
"""

import glob
import shutil
from git import Repo

#==============================================================================
# Project and libraries
#==============================================================================

print('')
print('Ensure the input is in quotation marks')

# User input section
project = input("Project Name:")
project_URL = 'https://github.com/DigicoUK/' + project
new_directory = input("Name of local working directory:")

print('Cloning project...')
# Automatic cloning of the project file (must happen first as this contains
# information about the libraries required for the project)
proj = Repo.clone_from(project_URL, new_directory)

print('Cloning libraries...')

# Extracting libraries information
repo_list = glob.glob(new_directory+'*')

libs_file = filter(lambda x: 'Lib' in x, repo_list)
libs_extract = ''.join(str(e) for e in libs_file)
libs_required = open(libs_extract, "r")

libraries = libs_required.readlines()
# Names of all required project libraries stored here
libraries = [x.strip('\n') for x in libraries]

# Names of required project libraries' URLs
lib_URL = []
for i in range(len(libraries)):
    lib_URL.append('https://github.com/DigicoUK/firmware_library_' 
                     +  libraries[i] + '.git')
    
# Automatic cloning of the libraries
libs = []
for i in range(len(lib_URL)):
    libs.append(Repo.clone_from(lib_URL[i], new_directory + libraries[i]))

libs.append(proj)
libraries.append(project)
#==============================================================================
# Contents
#==============================================================================

# Contents of functions in this script
# It is also worth noting that I would expect the functions to be performed
# in the order they are listed below.
def contents():
    '''
    
    Functions:
        
        1. status_check()
        
        2. newbranch(branchname)
        
        3. choosebranch(branchname)

        4. add()
        
        5. commit(message)
        
        6. push()
        
    Compound Functions:
        
        1. compush(message)
        
    Callable Parameters (helpful for debugging):
        
        - project
        - project_URL
        - proj
        - repo_list
        - libraries
        - libs

    If function is not working, ensure command input is in quotation marks.
    Use help(function) e.g. help(push) for more detailed information.
    
    '''
    return help(contents)
print('----------------------------------------------------')
print('')
print('Type contents() for a list of functions.')

#==============================================================================
# Function section 
#==============================================================================

def status_check(repo):
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
    '''      
    if repo == 'all':
        for x in libraries:
            status_check(x)
    
    j = libraries.index(repo)        
    f = libs[j]
    
    status = f.git.status()
    return status

# checkout and track a remote branch
def newbranch(repo, branchname):
       
    j = libraries.index(repo)
    f = libs[j]
    
    return f.create_head(branchname)

def newtag(repo, tagname, tagmessage):

    j = libraries.index(repo)
    f = libs[j]
    
    new_tag = f.create_tag(tagname, message=tagmessage)    
    return new_tag

# checkout and track a remote branch
def choosebranch(repo, branchname):
    '''
    Chooses branch to track remote branch updates from origin
    
    Parameters
    ----------
    repository : string
        Repository name (e.g. DmiAdc) command is intended to be applied to.
        
    branchname : string
        Select name of branch for changes and updates to files to be committed 
        to, ensure the argument input is of the form 'mybranch'
    
    Returns
    -------
    out : checkout
        Performs git 'checkout' routine, switching branch changes are committed
        to
    '''
    j = libraries.index(repo)
    f = libs[j]
    
    selection = f.git.checkout('origin/'+branchname, b = branchname)    
    return selection

# move a file to the repository
def move2repo(filename, local_directory):
    '''
    Move a new file into the local repository (i.e. the local working
    directory). This should ONLY be used for new features, and not for bugfixes
    or current editing of files inside the repository
    
    Parameters
    ----------
    filename : string
        The full file location on the local disk
    
    Returns
    -------
    out : edited working directory
        New file(s) moved to the directory are now ready to be added (using the 
        additor function)
    '''
    
    return shutil.move(filename, local_directory)

# add a file
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
    j = libraries.index(repo)
    f = libs[j]
    
    add_changes = f.git.add('.')    
    return add_changes

# commit and comment
def commit(repo, message):
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
    
    j = libraries.index(repo)
    f = libs[j]
    
    make_commit = f.git.commit(m = message)    
    return make_commit


# commit and comment
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
    
    j = libraries.index(repo)
    f = libs[j]
    
    origin = f.remote('origin')
    push_to = origin.push()   
    return push_to

#==============================================================================
# Compound Functions
#==============================================================================

def compush(repo, message):
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
    
    j = libraries.index(repo)
    f = libs[j]
      
    f.git.commit(m = message)
    origin = f.remote('origin')
    commit_and_push = origin.push()    
    return commit_and_push