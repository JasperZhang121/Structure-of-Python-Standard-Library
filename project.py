"""
Template for the COMP1730/6730 project assignment, S2 2022.
The assignment specification is available on the course web
site, at https://cs.anu.edu.au/courses/comp1730/assessment/project/

Collaborators: <list the UIDs of ALL members of your project group here>
"""


def analyse_stdlib():

    task1()
    task2()
    task3()
    task4()
    task5()


# The section below will be executed when you run this file.
# Use it to run tests of your analysis function on the data
# files provided.

'''
Task 1 Collect names of the StdLib modules and packages
'''


def task1():
    res = get_stdlib_packages()  # use helper function for getting all module and package names from stdlib
    length = len(res)
    print("StdLib contains", length, "external modules and packages:")  # Printing our findings
    print(res)


def get_stdlib_packages():
    """
    This function use the isort from anaconda to get all module and package
    names from stdlib. After get all names, remove names which start by
    underscore and particular names "this" and "antigravity".

    parameters: None
    return: names of module or package in stdlib
    """

    import isort
    names = isort.stdlibs.py38.stdlib  # use isort to get names

    start_with_underscore = []  # remove underscore
    for s in names:
        if s[0] == '_':  # if the names start with underscore we restore it inside a list
            start_with_underscore.append(s)
    if start_with_underscore:  # if the underscore list in not null
        for x in start_with_underscore:  # looping through the start_with_underscore list
            names.remove(x)  # remove underscore from names
    if "this" in names:  # remove module "this"
        names.remove("this")
    if "antigravity" in names:  # remove module "antigravity"
        names.remove("antigravity")
    return names


'''
Task 2 
'''


def task2():
    temp = get_real(get_stdlib_packages())  # get valid import modules
    res = []
    for x in get_stdlib_packages():  # loop through all import modules in stdlib
        if x not in temp:  # if module in stdlib but not in temp (valid importable modules)
            res.append(x)  # append it in the res for return

    print("These StdLib packages are not importable: ", res)


def get_real(package_names):
    """
    This function use the importlib for importing the names, and use the try
    and except to pass invalid module.

    parameters: sequential package_names
    return: a new list of invalid names
    """

    temp = []
    import importlib
    for x in package_names:  # loop the package_names and pass if module cannot be imported
        try:  # catch invalid module
            importlib.import_module(x)  # import by using the String name of
            temp.append(x)  # if the module can be imported, append it into the temp list for return
            if x != 'importlib':
                del x  # free up memory
        except:  # pass invalid module
            pass
    return temp


'''
Task 3
'''


def task3():
    most_dependant()  # use the helper function to print 5 most dependent packages
    temp = core_module()  # get first 5 most dependent modules by descending order
    print("The ", len(temp), " core packages are:")  # printing out core packages
    print(temp)


def module_dependency(module_names, name):
    """
    This function shows the dependency of the module in stdlib, and will throw
    empty list if the name if bad name (not a module name)

    parameters: list of module names, the name of module of checking
    return: list of dependant module (some modules in the stdlib)
    """
    import importlib
    try:  # catch bad module name
        module = importlib.import_module(name)  # import the input name
        temp = vars(module)  # get all dependencies
    except:
        return []  # return empty list if bad name
    lis = []
    for x in temp.keys():  # loop the keys and append it if the dependency in the module_names and not itself
        if x in module_names and x != name:
            lis.append(x)  # add in the res if dependant
    return lis


def most_dependant():
    """
    parameters: none
    return: first 5 most dependent modules by descending order
    """

    temp = get_real(get_stdlib_packages())  # get valid module names
    res = {}
    for x in temp:  # loop the names and use the module_dependency function
        ans = module_dependency(temp, x)
        res[x] = len(ans)  # add in the dict in this format {name of the modules: number of dependency}
    sortedByVal = {k: v for k, v in sorted(res.items(), key=lambda v: v[1], reverse=True)}  # sort by val descending
    count = 0
    print("The following StdLib packages are most dependent:")
    for x, y in sortedByVal.items():
        if count == 5:  # print first 5 items after sorting
            break
        print(f"{x:<12}{y:>12}")  # adjusting the print format
        count += 1


def core_module():
    """
    parameters: none
    return: core module by descending order
    """
    temp = get_real(get_stdlib_packages())  # get valid module names
    res = {}
    for x in temp:  # loop the names and use the module_dependency function
        ans = module_dependency(temp, x)
        res[x] = len(ans)  # add in the dict in this format {name of the modules: number of dependency}
    fin = []
    for x, y in res.items():  # loop the dictionary to check whether the value is 0, which mean no dependency
        if y == 0:  # if 0 then meaning core, add in list
            fin.append(x)
    return fin


"""
Task 4
"""


def task4():
    packages = get_real(get_stdlib_packages())  # get all importable module names
    mapp = {}
    for x in packages:
        # go inside the package, and get a tuple in the format (lines in all .py files, custom classes in all .py file)
        temp = explore_package(x)
        mapp[x] = temp  # store the module name as the key and tuple as the value

    # 5 largest packages in terms of lines of code
    v = mapp.values()  # get the tuple
    descending_v = sorted(v)[::-1]  # sort by the first value of tuple descending
    lis = Count_Five_Packages(descending_v)  # get first five elements as list in tuple_array[0] excluding 0
    five_largest = []
    for x, y in mapp.items():  # loop the mapp, if the first value in tuple is in lis, append the module name
        if y[0] in lis:  # y[0] in lis means x is one of five largest packages in terms of lines of code
            five_largest.append(x)  # append the module name x in the five_largest
        if len(five_largest) == 5:
            break  # if already get 5 elements in the list, stop the loop and return five_largest
    print("5 largest packages in terms of the number of lines of code (LOC): ")
    print(five_largest)

    # 5 smallest packages in terms of lines of code
    ascending_v = sorted(v)  # sort by the first value of tuple ascending
    lis = Count_Five_Packages(ascending_v)  # get first five elements as list in tuple_array[0] excluding 0
    five_smallest = []
    for x, y in mapp.items():  # loop the mapp, if the first value in tuple is in lis, append the module name
        if y[0] in lis:  # y[0] in lis means x is one of five smallest packages in terms of lines of code
            five_smallest.append(x)  # append the module name x in the five_smallest
        if len(five_smallest) == 5:
            break  # if already get 5 elements in the list, stop the loop and return five_smallest
    print("5 smallest packages in terms of the number of lines of code (LOC): ")
    print(five_smallest)

    # 5 largest custom classes
    # sort by the 2nd value in tuple descending
    descending_v_by_second_item = sorted(v, key=lambda x: x[1], reverse=True)
    # get first five elements as list in tuple_array[0] excluding 0
    lis = Count_Five_Custom_Class_Packages(descending_v_by_second_item)
    five_most_classes = []
    for x, y in mapp.items():  # loop the mapp, if the second value in tuple is in lis, append the module name
        if y[1] in lis:
            five_most_classes.append(x)
        if len(five_most_classes) == 5:
            break  # if already get 5 elements in the list, stop
    print("5 largest custom classes packages: ")
    print(five_most_classes)

    # no custom class
    no_custom_classes = []
    for x, y in mapp.items():
        if y[1] == 0:  # if second value in tuple is 0, it means no custom class
            no_custom_classes.append(x)
    print("no custom classes packages: ")
    print(no_custom_classes)


def explore_package(a_package):
    """
    This function explore the module either the module is single .py file or a directory, counting total lines and
    custom types

    parameters: string a_package
    return: a tuple (lines in all .py files, custom classes in all .py file)
    """

    import os
    import importlib
    lines = 0  # initialize for counting lines
    custom_types = 0  # initialize for counting
    try:  # catch bad module name
        module = importlib.import_module(a_package)
        temp = vars(module)
        for x, y in temp.items():
            if x == "__path__":  # if the module is a package
                s = ""
                for x in y[0]:  # make the path readable by changing "\\" to '/'
                    if x != "\\":
                        s += x
                    else:
                        s += '/'
                for dir_root, dirs, files in os.walk(str(s), topdown=True):  # use os.walk() to get all names inside
                    for names in files:
                        if names[-3:] == '.py':  # if end with '.py', we know it is a python file
                            lines += Number_of_Lines(s + '/' + names)  # add number of lines from all files inside
                            custom_types += Number_Of_Custom_Types(s + '/' + names)  # add number of custom types
                break
            else:
                if x == "__file__" and y[-3:] == '.py':  # if the module is a single python file
                    lines = Number_of_Lines(y)  # directly go inside and check the number of lines
                    custom_types = Number_Of_Custom_Types(y)  # directly go inside and check the number of custom
    except:
        pass
    return (lines, custom_types)  # return a tuple


def Number_of_Lines(my_file_obj):
    """
    This is a helper function for counting total number of lines in the document

    parameters: String value of the path of the file
    return: how many lines in total in that file
    """
    c = 0
    fileobj = open(my_file_obj, "r")  # open the file
    for line in fileobj:
        if line:
            c += 1  # count the line if the line is not None
    fileobj.close()  # close the file
    return c


def Number_Of_Custom_Types(path):
    """
    This the function for return how many custom types in the current file

    parameters: the path of the file
    return: number of custom classes

    """
    count = 0
    fileobj = open(path, "r")  # open the file
    for line in fileobj:
        if line:  # if line is not None
            line = line.split()  # split a string into a list
            if line:  # if list is not None
                if line[0] == 'class':  # count the line if the first element in the lien is string 'class'
                    count += 1
    fileobj.close()  # close the file
    return count


def Count_Five_Packages(tuple_array):
    """
    This function is used for return first five elements as list in tuple_array[0] excluding 0

    parameters: tuple_array
    returns: a list with length 5
    """
    count = 0
    lis = []
    for x in tuple_array:
        if count == 5:  # if already run 5 loops, break the loop
            break
        if x[0] != 0:  # only append when first element is not 0
            lis.append(x[0])
            count += 1
    return lis


def Count_Five_Custom_Class_Packages(tuple_array):
    """
    This function is used for return first five elements as list in tuple[1]
    parameters: tuple_array
    returns: a list with length 5
    """
    count = 0
    lis = []
    for x in tuple_array:
        if count == 5:  # if already run 5 loops, break the loop
            break
        lis.append(x[1])  # append second value in tuple
        count += 1
    return lis


"""
Task 5
"""


def task5():
    find_cycles()


def find_cycles():
    p = get_real(get_stdlib_packages())  # get all package names
    packages = p.copy()
    print("The StdLib packages form a cycle of dependency:")
    final = []
    for x in packages:  # use the for loop for running the recursion
        res = Generate_Dependency(x, 0, [], [], p)
        if res:  # if list is not None
            for link in res:  # for each list in res
                linkage = ""
                for i in range(len(link)):
                    linkage += link[i]  # append elements in link into linkage
                    if i != len(link) - 1:
                        linkage += "->"  # connect elements in link with "->"
            final.append(linkage)  # append it to the list final for return
    print(final)


def Generate_Dependency(name, count, lis, res, stdlib):
    """
    This function is a recursion function which stops

    1.  when we explore (go deeper) the branch for more than 10, and we still cannot find self-dependent.
    In this case we assume there is no further self-dependent. Actually for count =10, it is already very robust as
    this function does not allow this kind of situation happen:
            [subprocess->contextlib->sys->platform->platform->platform->platform->platform->subprocess]
    you can see the self-dependent module platform repeat 5 times, which is unnecessary, because it can simply be:
            [subprocess->contextlib->sys->platform->subprocess]

    2.  if we find the current name is the first one in the list (where we begin), stop and add it to the result

    3.  if there is no dependent file in the current package, return because of end of the branch

    4.  cannot import the module and return

    parameters: name (name of module), count (deep of recursion), lis (recording path), res (adding path for output),
                stdlib (all importable module names in stdlib)
    return: res
    """
    # basically use the DFS algorithm
    import importlib
    if count == 10:  # Stop when go depth = 10
        return  # stop recursion because maxi depth according to assumptions
    if lis:
        if lis[0] == name:  # if start element is equal to current element, find cycle
            temp = lis.copy()
            res.append(temp)  # append it into the result
            return
    else:
        lis.append(name)  # not finding result, put it into list for recording path

    try:
        module = importlib.import_module(name)  # import module
    except:
        return  # if the module cannot be imported, return to last recursion

    temp = vars(module)
    t = temp.copy()  # get the dependencies
    if not t:
        return  # if empty dependencies return to last recursion
    for dependency in t.keys():  # looping the dependencies inside the module
        if dependency in stdlib:
            if dependency in lis and lis[0] != dependency:  # not allowing self-dependent except first and last one
                continue  # if A->B and it will be A->B->B after appending, not allowing, return to last recursion
            lis.append(dependency)  # add into the lis as the path
            Generate_Dependency(dependency, count + 1, lis, res, stdlib)  # recursion with only change: count++
            lis.pop(-1)  # pop out the added item in current recursion for next loop
    return res


"""
Task 6
"""


def task6():
    visualize_connectivity()


def visualize_connectivity():
    """
    This is the function for drawing the links inside StdLib

    parameters: none
    return: a graph
    """

    import networkx as nx
    import matplotlib.pyplot as plt
    g = nx.Graph()  # initialize
    nodes = get_real(get_stdlib_packages())  # get all importable module names as nodes
    for node in nodes:
        g.add_node(node)  # add all importable module name as nodes in the graph
    edges = connection_In_Stdlib()  # get linkages of nodes in the graph
    for edge in edges:
        g.add_edge(edge[0], edge[1])  # add linkages of nodes in the graph
    # set the graph style
    plt.figure(figsize=(10, 8))
    pos = nx.kamada_kawai_layout(g)
    node_options = {"node_color": "black", "node_size": 10}
    edge_options = {"width": 1, "alpha": .5, "edge_color": "black"}
    nx.draw_networkx_nodes(g, pos, **node_options)
    nx.draw_networkx_edges(g, pos, **edge_options)
    # plot
    plt.show()


def connection_In_Stdlib():
    """
    This is the function for finding link between two modules in the StdLib
    If two modules have dependency, put them as a tuple in the lis

    parameters: None
    return: list with tuples inside
    """
    import importlib
    res = []
    packages = get_real(get_stdlib_packages())  # get all importable module names
    for name in packages:
        module = importlib.import_module(name)  # import
        temp = vars(module)  # get dependency
        t = temp.copy()
        for x in t.keys():  # loop the dependency and avoid self dependent
            if x in packages and x != name:
                res.append((name, x))  # append the tuple in the list
    return res


"""
Run section:
"""

if __name__ == '__main__':
    NAME = 'Hao Zhang'
    ID = 'u6523462'
    print(f'My name is {NAME}, my id is {ID}, and these are my findings for Project COMP1730.2022.S2')
    analyse_stdlib()
