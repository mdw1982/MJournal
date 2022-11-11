class LD(dict):
    def __setitem__(self, key, value):
        print(f"setting {key} {value}")
        super().__setitem__(key,value)

    def __getitem__(self, item):
        print(f"getting item {item}")
        return super().__getitem__(item)

    def __delitem__(self, key):
        print(f"deleting item {key}")
        super().__delitem__(key)

# jam = LD()
# sumstrg = 'test'
# for i in range(5):
#     val = sumstrg + str(i)
#     jam.__setitem__(key=i,value=val)
#
# print(jam)
# jam.__setitem__(len(jam)+1,'this is really cool!')
# print(jam)
