from py2g_utils.arguments import FileArgumentParser

parser = FileArgumentParser('./samples/parameters/base.yaml', './samples/parameters/process.yaml')
arguments = parser.parse()

for key in arguments.keys():
    argument = arguments.__getattribute__(key)
    if type(argument) == list:
        print("{}:".format(key))
        for v in argument:
            print("\t{}".format(v))
    else:
        print("{}: {}".format(key, argument))