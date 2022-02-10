# PyPkgGen
![PyPkgGen Logo](https://i.ibb.co/kBf4T8c/pypkggen.png)

Python Package Generator is a Python library for generating Python libraries for PyPI.org in an easier and faster way.
Or do you not know how to package your Python project? Or do you want an easier and faster way to package your Python projects? If yes, then PyPkgGen is for you.
In just a few commands, your Python project will be live on PyPI.org and developers will be able to install it using ```pip```.


## Table of Contents
- [Installation](https://github.com/Samuel-HSSP/pypkggen/blob/main/README.md/#installation)
- [Usage](https://github.com/Samuel-HSSP/pypkggen/blob/main/README.md/#usage)
- [To-Do](https://github.com/Samuel-HSSP/pypkggen/blob/main/README.md/#to-do)


## Installation
Installing PyPkgGen from PyPI will install all the libraries required to build your Python projects.
Follow the instructions below to install PyPkgGen:

Use pip/pip3 to install from PyPI
```
$ pip install pypkggen
```
You can also use Python from your command prompt
```
$ python -m pip install pypkggen
```
Lastly, to install from GitHub (ensuring that Git has been added to PATH), run:
```
$ python -m pip install git+https://www.github.com/Samuel-HSSP/pypkggen
```

## Usage
PyPkgGen is best used on the terminal. Make sure you have Python and Pip installed on your computer and they must be added to PATH. The following section of the documentation will guide you on how to package your Python project using PyPkgGen.

1. Initialize Python REPL
    ```
    $ python
    ```
2. Create a folder called **source** and move all your source files (.py) into this folder. Note the path to this folder because it will be your `code_source_dir` when generating your package.
3. Follow the instructions below and run the codes to generate your Python project.
```python
>>> from pypkggen import PyPkgGen
>>> generator = PyPkgGen("package_name", "import_name", "code_source_dir")
```

'package_name' is the name you want to give your Python package
'import_name' is the name your package will be stored with. This is what you will use to import the package
'code_source_dir' is the path to `source` containing all the source files for your project.

```python
>>> generator.generate_setup_file("filename.txt", test=True)
```
A simple setup file will be generated in the current working directory with the filename given, as a text file.
Set `test` to True if you want to test your package first on test.pypi.org before publishing on PyPI.org. It is recommended to set it to True because you should test your package before publishing.
Edit the setup file and run this final code:

```python
>>> generator.create_package(test=True)
```

The code above will start creating your package. Make sure you set `test` to True if you did that on the previous code and False if you had set it to False when generating setup file.
Carefully follow the instructions given when creating your package. All the files you need will be generated automatically for you. Make sure you double-check them and edit to your taste.

Congratulations! You should now have your package published to PyPI.


## To-Do
- [ ] Automate terminal commands
- [ ] Make it more intuitive
- [ ] Add more functionalities
- [ ] Proper documentation
- [ ] Fix all the bugs, and probably add more
