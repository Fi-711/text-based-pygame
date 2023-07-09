import pkg_resources, sys, os

# This functions gets your installed modules and checks if any key ones are missing
def package_checker():
    installed_packages = pkg_resources.working_set
    installed_packages_list = sorted(["%s==%s" % (i.key, i.version) for i in installed_packages]) 
    print(installed_packages_list)
    #list of packages you need    
    required_packages = (['google-auth-oauthlib==0.4.1', 'google-auth==1.22.1', 'gspread==3.6.0', 
    'multipledispatch==0.6.0', 'oauth2client==4.1.3', 'oauthlib==3.1.0', 'pandas==1.1.3',
    'pygame==1.9.6', 'pyopenssl==19.1.0', 'requests-oauthlib==1.3.0'])

    #prints out if you are missing any dependencies
    print(list(set(required_packages) - set(installed_packages_list))) if (
        len(list(set(required_packages) - set(installed_packages_list))) > 0) else print(
            "\nYou have all the required python dependencies.\n")
    
    if len(list(set(required_packages) - set(installed_packages_list))) > 0:
        print("\nYou are missing the above packages. Type:\n\
        python -m pip install gspread oauth2Client PyOpenSSL pygame multipledispatch pandas\
            \nto install the missing packages\n")
        c = input("Attempt to install now? Y/n > ")
        if c == "" or c.lower() == "y":
            os.system("python3 -m pip install gspread oauth2Client PyOpenSSL pygame multipledispatch pandas")
            os.system("pause")
        else:
            pass
    
    print(f"This game was made in python version 3.7.8 - your version is {sys.version[:5]}. Consider grabbing 3.7.8") if(
        int(sys.version[2]) >= 8) else print(f"This game was made in python version 3.7.8. Your system version - {sys.version[:5]} - should be compatible.")

# If you are missing any here's a command to install all modules used so far:
# python -m pip install gspread oauth2Client PyOpenSSL pygame multipledispatch pandas

package_checker()
