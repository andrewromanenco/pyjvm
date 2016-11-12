'''Java decompiler; same as call javap with no flags.'''
import sys

from pyjvm.utils.javap import javap

def describe_class_from(path):
    '''Decompile and nicely print a class.'''
    klass = javap(path)
    line = []
    line.extend(klass.accessor)
    line.append(klass.class_or_interface)
    line.append(klass.class_name)
    if klass.super_class != 'java.lang.Object':
        line.append('extends')
        line.append(klass.super_class)
    if len(klass.interfaces):
        line.append('implements')
        line.append(', '.join(klass.interfaces))
    line.append('{')
    print(' '.join(line))

    for field in klass.fields:
        if field.name == 'serialVersionUID':
            continue
        line = ["   "]
        line.extend(field.flags)
        line.append(field.type)
        line.append(field.name)
        print(' '.join(line) + ';')

    for method in klass.methods:
        if method.name == '<clinit>':
            print('    static {};')
            continue
        if '$' in method.name:
            continue
        line = ["   "]
        line.extend(method.flags)
        line.append(method.returns)
        signature = method.name
        if method.name == '<init>':
            signature = klass.class_name
        signature += '('
        signature += ', '.join(method.params)
        signature += ')'
        line.append(signature)
        print(' '.join(line) + ';')

    print('}')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Provide parameter with path to a Java8 class file.")
    else:
        describe_class_from(sys.argv[1])
