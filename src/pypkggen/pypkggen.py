import os, time, glob, shutil
from datetime import datetime
from pypkggen.licenses import LICENSES
from pypkggen.files import *
from pypkggen.setup_file import setup_template, test_setup_template

DOC = """
# {}
{}
"""
# Class
class PyPkgGen:
    setup_filepath = None
    YEAR = str(datetime.today().year)
    AUTHOR = ""
    description = ""
    USERNAME = ""
    VERSION = ""

    # Constructor
    def __init__(self, package_name:str,
                       import_name:str,
                       code_source_dir:str):
        """
        `package_name` is the name of the folder containing all the source codes and folders
        `import_name` is the name that will be used to import the library when it has been compiled and published.
        `code_source_dir` is the folder containing all the source codes for the project.

        """
        self.package_name = package_name.lower()
        self.code_source_dir = code_source_dir
        self.import_name = import_name

    # Generate setup file
    def generate_setup_file(self, filename:str, test:bool=True):
        """
        filename must have a .txt extension. "Ex: sample.txt"
        `test` should be True if you're trying to publish on test.pypi.org
        """
        with open(filename, "w") as SETUP:
            if test:
                SETUP.write(setup_template)
            else:
                SETUP.write(test_setup_template)
        self.setup_filepath = filename
        print(f"Setup file has been saved to \"{filename}\"")
        print("Open the file to edit")

    # Help user to choose a license
    def choose_license(self):
        print("Choose a license from the available ones below:")
        print("1. MIT License\n2. GNU GPL\n3. GNU AGPL\n4. GNU LGPL\n5. The Unlicense")
        print("If your desired license is not available, please choose a random license and visit https://choosealicense.com/appendix for the licenses you could use.")
        print("You can then edit the LICENSE file with your chosen license")
        license = input("Choose a number: ")
        if license.isdigit():
            if license == "1":
                return "MIT"
            elif license == "2":
                return "GPL"
            elif license == "3":
                return "AGPL"
            elif license == "4":
                return "LGPL"
            elif license == "5":
                return "UNLICENSE"
            else:
                print("You typed an unavailable option, please try again.")
                return self.choose_license()

    # Ask for confirmation to generate MANIFEST.in file
    def manifest_in(self):
        man = input("Do you want the MANIFEST.in file? [Y/n]")
        if man.lower() == "y":
            return "yes"
        elif man.lower() == "n":
            return "no"
        else:
            print("You inputted a wrong value, please try again!")
            return self.manifest_in()


    # Create package
    def create_package(self, test=True):
        import os
        folders = ["", "/src", "/tests"]
        for folder in folders:
            if not os.path.exists(self.package_name+folder):
                os.makedirs(self.package_name+folder)
            else:
                pass
        if not os.path.exists(self.package_name+"/src/"+self.import_name):
            os.makedirs(self.package_name+"/src/"+self.import_name)
        else:
            pass

        print("Generating pyproject.toml...")
        with open(self.package_name+"/pyproject.toml", "w") as TOML:
            TOML.write(PP_TOML)
        time.sleep(0.5)

        with open(self.setup_filepath, "r") as setup:
            lines = setup.readlines()
            # Setup details
            name = lines[1].split("->")[-1].strip()
            version = lines[3].split("->")[-1].strip()
            author = lines[5].split("->")[-1].strip()
            email = lines[7].split("->")[-1].strip()
            desc = lines[9].split("->")[-1].strip()
            github = lines[11].split("->")[-1].strip()
            pypi = lines[12].split("->")[-1].strip()
            bug = lines[13].split("->")[-1].strip()
            lics = lines[15].split("->")[-1].strip()
            ops = lines[17].split("->")[-1].strip()
            py_version = lines[19].split("->")[-1].strip()
            _deps = lines[21].split("->")[-1]
            deps = _deps.replace("==",
                                "; python_version == \"").replace(
                                "<=",
                                "; python_version <= \"").replace(
                                ">=",
                                "; python_version >= \""
                                ).split(",")
            self.AUTHOR = author
            self.USERNAME = pypi
            self.VERSION = version
            self.description = desc
        #print("Dependencies: ", deps)
        deps[-1] = deps[-1].strip("\n")
        #print("Dependencies: ", deps)
        for dep in deps:
            if "=" in dep:
                deps[deps.index(dep)] = "   "+dep+'\"'
            else:
                deps[deps.index(dep)] = "   "+dep
        deps[-1] = deps[-1]+"\n"
        #print("Now: ", deps)
        deps = "\n".join(deps)

        print("Generating setup.cfg...")
        with open(self.package_name+"/setup.cfg", "w") as SETUP_:
            SETUP_.write(SETUP.format(name, version, author, email, desc, github,
                                      bug, lics, ops, py_version, deps))

        print("Generating license file...")
        with open(self.package_name+"/LICENSE", "w") as LICENSE:
            license = self.choose_license()
            if license == "MIT":
                LICENSE.write(LICENSES["MIT"].format(self.YEAR, self.AUTHOR))
            elif license == "GPL":
                LICENSE.write(LICENSES["GNU GPL"])
            elif license == "AGPL":
                LICENSE.write(LICENSES["GNU AGPL"])
            elif license == "LGPL":
                LICENSE.write(LICENSES["GNU LGPL"])
            elif license == "UNLICENSE":
                LICENSE.write(LICENSES["UNLICENSE"])
        print("LICENSE file has been generated.\nPlease edit it to your taste.")
        time.sleep(0.5)

        man_ = self.manifest_in()
        if man_ == "yes":
            print("Generating MANIFEST.in file...")
            with open(self.package_name+"/MANIFEST.in", "w") as manifest:
                manifest.write(MANIFEST)
            print("MANIFEST.in template has been generated.\nVisit https://packaging.python.org/en/latest/guides/using-manifest-in/#using-manifest-in for a guide on how to use the file")
            print("The file contains all the commands used in MANIFEST.in files.\nIf you don't know anything about it, please delete the MANIFEST.in file. It's not necessarily needed.")
        elif man_ == "no":
            pass
        time.sleep(0.5)

        with open(self.package_name+"/src/"+self.import_name+"/__init__.py", "w") as init:
            init.write(INIT.format(self.description, self.package_name, self.AUTHOR))

        print("Generating README.md...")
        with open(self.package_name+"/README.md", "w") as README:
            README.write(DOC.format(self.package_name, self.description))
        time.sleep(0.5)
        print("Done!")
        print(f"You can edit the README.md saved at \"{self.package_name+'/README.md'}\"")

        print("Preparing test folder...")
        time.sleep(1)

        for file in glob.glob(self.code_source_dir+"*"):
##            print(file)
            if file.endswith(".py"):
                shutil.copy(file, self.package_name+"/tests/")
                shutil.copy(file, self.package_name+"/src/"+self.import_name+"/")
        print("Done!")
        print("Your package is now fully ready for publishing")
        print("###############\nNext steps: \n###############")
        print("""Open your terminal and set the current working directory to the package_name where the `pyproject.toml` file is located.
        Follow the instructions below if you're using the test version of the package (if you used `test=True`):
            1. Create an account on test.pypi.org and verify your email.
            2. Log in and click on your profile icon to open `Account settings`
            3. Scroll down and click on `Add API token`
            4. Name it as the package name
            5. Set the `Scope` to `Entire account (all projects)` and proceed by clicking `Add token`
            6. Copy the whole API key (including the pypi- prefix) and paste it somewhere
               before you close the page, else you won't ever find it again!
            7. Next, type the following commands in your terminal after setting the cwd as the package folder:
                $ python -m build
                $ python -m twine upload --repository testpypi dist/*
            8. This is going to ask for a username and password.
            9. Type '__token__' for the username (without the quotes) and press Enter
            10.Finally, paste the API key you copied earlier for the password and press Enter
            11.Wait till your package is uploaded to test.pypi.org and type the command below
               to install your own package, for testing.
               $ python -m pip install --index-url https://test.pypi.org/simple/ --no-deps package-name-YOUR-PYPI-USERNAME-HERE
               Example: $ python -m pip install --index-url https://test.pypi.org/simple/ --no-deps pylibgen-SamuelHSSP
            [When the installation is done!, you can then import your package with the name saved...]
        ...
        Otherwise, if you're using the original package to publish on pypi.org,
        follow the same instructions above but register on pypi.org instead of test.pypi.org.
        Do not type the commands above for the original package, but rather use the following commands:
            $ python -m build
            $ python -m twine upload dist/*
            And finally, after entering your credentials for pypi.org (username and password), type the command below to install your package:
                $ python -m pip install package-name
                Example: $ python -m pip install pypkggen

        [Huge congrats!]
        To know more about packaging Python projects, visit https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/
        [Please follow me on GitHub and let me know if you'd like to contribute to the project :)]

        """)
