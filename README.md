# TomScript
Python code developed for managing multiple GitHub repositories at any one time.

The need for this program has origin in my unique workflow: we work on projects which in turn use scripts and files from multiple libraries. Each project is a separate repository on GitHub, and each Library is also its own repository on GitHub. 

As long as there is a file containing information about the Libraries that are required inside the Project repository, we are able to create a new working branch in each repository and clone each repository (Project and Libraries) to a local working directory.
