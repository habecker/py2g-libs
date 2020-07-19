import yaml, os, re, sys, json

class ArgumentError(Exception): ...

class ArgumentParser(object):
    def __init__(self):
        self.parsers = {}
        self.converters = {}

    def add(self, type, parser, converter=lambda v: v):
        assert type not in self.parsers
        self.parsers[type] = parser
        self.converters[type] = converter

    def parse(self, type, value):
        assert self.parsers[type](value)
        return self.converters[type](value)

_argument_parser = ArgumentParser()
_argument_parser.add('int', lambda value: value.isdigit(), lambda value: int(value))
_argument_parser.add('string', lambda value: type(value) == str)
_argument_parser.add('path', lambda value: type(value) == str and os.path.exists(value))
_argument_parser.add('list', lambda value: type(value) == str, lambda value: json.loads(value))

class ArgumentValidator(object):
    def __init__(self):
        self.validators = {}

    def add(self, type, validator):
        assert type not in self.validators
        self.validators[type] = validator

    def validate(self, val, value):
        return self.validators[val['type']](val, value)

_argument_validator = ArgumentValidator()
_argument_validator.add('regex', lambda val, value: re.match(val['expression'], value))

class Arguments(object):
    def __init__(self):
        object.__setattr__(self, 'arguments', {})
    def set(self, name, value):
        _arguments = object.__getattribute__(self, 'arguments')
        _arguments[name] = value
    def __getattribute__(self, name):
        _arguments = object.__getattribute__(self, 'arguments')
        if name in _arguments:
            return _arguments[name]
        return object.__getattribute__(self, name)
    def keys(self):
        return object.__getattribute__(self, 'arguments').keys()

class FileArgumentParser(object):
    def __init__(self, *files, encoding='utf-8'):
        self.arguments = {}
        for fp in files:
            with open(fp, 'r', encoding=encoding) as f:
                _keys = set()
                for argument in yaml.safe_load(f):
                    if argument['key'] in _keys:
                        raise ''
                    self.arguments[argument['key']] = argument
                    _keys.add(argument['key'])

    def _get_arguments(self):
        _arguments = {}
        last_arg = None
        for arg in sys.argv[1:]:
            if last_arg is None and arg[:2] != '--':
                raise ArgumentError('{} has no argument to be assigned to'.format(arg[:2]))
            if last_arg is not None and arg[:2] != '--':
                _arguments[last_arg] = arg
                last_arg = None
            elif arg[:2] == '--':
                last_arg = arg[2:]
                _arguments[last_arg] = None
        return _arguments

    def parse(self):
        _arguments = self._get_arguments()
        arguments = Arguments()
        _required_arguments = {k for k,v in self.arguments.items() if 'default' not in v}
        _default_arguments = {k for k,v in self.arguments.items() if 'default' in v}

        for k,v in _arguments.items():
            if k in self.arguments:
                argument = self.arguments[k]
            else:
                raise ArgumentError('Unknown argument {}'.format(k))
            v = _argument_parser.parse(argument['type'], v)
            if 'validation' in argument:
                for val in argument['validation']:
                    if not _argument_validator.validate(val, v):
                        raise ArgumentError("Validator of type {} failed for argument {}".format(val['type'], k))
            arguments.set(k,v)
            _required_arguments -= {k}
        if len(_required_arguments) > 0:
            raise ArgumentError('Arguments {} required'.format(_required_arguments))
        
        for k in _default_arguments:
            if k not in arguments.arguments:
                arguments.set(k, self.arguments[k]['default'])
        
        return arguments
        # argument = self.arguments[name]
        # _argument_parser.parse(argument['type'], value)
        # if 'validation' in argument:
        #     for val in argument['validation']:
        #         _argument_validator.validate(val, value)
        # return value


if __name__ == '__main__':
    parser = FileArgumentParser('./arguments/base.yaml')
    print(parser.parse().__dict__)