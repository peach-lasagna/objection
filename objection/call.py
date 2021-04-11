import ast
import inspect
from typing import Callable


class CallExplorer:
    def __init__(self):
        pass

    def call_tree(self, func: Callable):
        ast.parse(inspect.getsource(func))




class CallVisitor(ast.NodeVisitor):
    def visit_Call(self, node):
        print(node.__dict__)
        return node

"""
>>> Functionname
f1 ()



"""
