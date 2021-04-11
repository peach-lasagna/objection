class TreeExplorer:
    def __init__(self,  ignore_danders=True, view_values=True, view_seq_values=True):
        self.ignore_danders=ignore_danders
        self.view_values=view_values
        self.view_seq_values=view_seq_values
        self.space =  '    '
        self.branch = '│   '
        self.tee =    '├── '
        self.last =   '└── '

    def tree(self, obj: type, prefix: str=''): # type: -> Generator
        '''получить дерево атрибутов объекта в виде ascii кракозябр'''
        contents = obj.__dict__
        if self.ignore_danders:
            contents = dict(filter(lambda x: x[0][0] != '_', contents.items()))

        # contents each get pointers that are ├── with a final └── :
        pointers = [self.tee] * (len(contents) - 1) + [self.last]
        for pointer, key in zip(pointers, contents):
            attr = getattr(obj, key)

            res = prefix + pointer + key
            if self.view_values:
                res += f' value={attr}'
            yield res
            if hasattr(attr, '__dict__') and key != '__class__':
                extension = self.branch if pointer == self.tee else self.space
                yield from self.tree(attr, prefix=prefix+extension)
            if self.view_seq_values and hasattr(attr, '__iter__'):
                extension = self.branch if pointer == self.tee else self.space
                for k in attr:
                    try:
                        yield from self.tree(k, prefix=prefix+extension)
                    except AttributeError:
                        yield prefix +extension + pointer + str(k)

    # def tree(obj, level: int=0): # type: -> Generator
    #     '''получить дерево атрибутов объекта в виде кортежей вида (атрибут, степеньвложенности)'''
    #     contents = obj.__dict__
    #     # contents each get pointers that are ├── with a final └── :
    #     for key in contents:
    #         yield (level, key)
    #         attr = getattr(obj, key)
    #         # exp = not isdescriptor(attr) and attr is not None and not inspect.isbuiltin(attr) and 
    #         if hasattr(attr, '__dict__') and key != '__class__':
    #             yield from tree(attr, level=level+1)

    def get_tree_parents(self, obj: type) -> list: # эта поебень не работает, потому что я поправил tree
        '''получить атрибуты объекта и его родителей'''
        if hasattr(obj, '__mro__'):
            s = list()
            for par in (obj,)+obj.__mro__[::-1]:
                # s.add(par.__name__)
                for it in self.tree(par):
                    if it in s:
                        pref = it.split()[0]
                        if  pref+' ' == self.tee:
                            continue
                        elif pref+' ' == self.last:
                            s.remove(it)
                            s.append(it)
                        else:
                            s.append(it)
                    else:
                        s.append(it)

            return s

    def get_dict_tree(self, obj: type): # type: -> Generator
        '''получить дерево атрибутов объекта в виде словаря'''
        dct = {}
        contents = obj.__dict__
        for key in contents:
            dct[key] = {}
            attr = getattr(obj, key)
            if hasattr(attr, '__dict__') and key != '__class__':
                for i in self.get_dict_tree(attr):
                    dct[key][i] = {}
        return dct

