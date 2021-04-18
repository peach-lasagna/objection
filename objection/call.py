import ast
import inspect
from typing import Callable
import re

MATCH_PACK = r'(?<=site-packages\/).*(?=\.\w+$)'
_list = []
PATH = ""

def solve_name(node):
    if isinstance(node, ast.Call):
        fu = node.func
        return solve_name(fu), node.args
    elif isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Attribute):
        return solve_name(node.value) + '.' + node.attr

def imp_com(path: str, name: str):
    if '.' in name:
        exc = f"from {path} import {name.split('.')[0]}"
    else:
        exc = f"from {path} import {name}"
    print(exc)
    exec(exc)

class CallExplorer:
    def __init__(self):
        self.space =  '    '
        self.branch = '│   '
        self.tee =    '├── '
        self.last =   '└── '

    def call_tree(self, func: Callable):
        global PATH
        _list = []
        visitor = CallVisitor()
        tree = ast.parse(inspect.getsource(func))
        PATH = inspect.getsourcefile(func)
        PATH = re.search(MATCH_PACK, PATH).group().replace('/', '.')
        imp_com(PATH, func.__name__)
        tree = visitor.visit(tree)
        return _list


class CallVisitor(ast.NodeVisitor):
    def visit_Call(self, node: ast.Call):
        global PATH
        # try:
        name, args = solve_name(node)
        print(name)
        imp_com(PATH, name)
        _list.append((name, args))
        obj = exec(name)
        PATH = inspect.getsourcefile(obj)
        PATH = re.search(MATCH_PACK, PATH).group().replace('/', '.')
        self.visit(ast.parse(inspect.getsource(obj)))
        # except Exception as e: print(e)
        # finally:
        return node
"""
>>> Functionname
|-f1 ()
  |_ f3(args)

"""
from fastapi import Depends



print(CallExplorer().call_tree(Depends))
