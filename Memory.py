# class Memory:

# def __init__(self, name):
#         self.dict = {}
#         self.name = name

#     def has_key(self, name):
#         return ( name in self.dict )

#     def get(self, name):
#         return self.dict[name]

#     def put(self, name, value):
#         self.dict[name] = value


class MemoryStack:
    def __init__(self, memory=None):
        self.stack = [memory] if ( memory is not None ) else []

    # def get(self, name):
    #     self.stack

    # def insert(self, name, value):
    #     self.stack[-1].put( name, value )

    # def set(self, name, value):
    #     for memory in reversed( self.stack ):
    #         if memory.has_key(name):
    #             return memory.put( name, value )

    def push(self, memory):
        self.stack.append(memory)

    def pop(self):
        return self.stack.pop()


