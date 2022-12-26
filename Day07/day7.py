class File:
    def __init__(self, size, name, parent) -> None:
        self.name = name
        self.size = size
        self.folders = []
        self.parent = parent
        self.depth = parent.depth + 1

    def computeSize(self):
        return self.size
    
    def getParent(self): return self.parent

    def render(self):
        delta_space = "  " * self.depth + " "
        print(delta_space + self.name)

class Directory:
    def __init__(self, name, parent) -> None:
        self.name = name
        self.folders = []
        self.files = []
        self.parent = parent
        self.depth = parent.depth + 1 if parent != None else 0

    def addFile(self, line_raw):
        line_list = line_raw.split(" ")
        size = int(line_list[0])
        name = line_list[1]
        file = File(size, name, self)
        self.files.append(file)
    
    
    def addFolder(self, line_raw):
        line_list = line_raw.split(" ")
        dir = Directory(line_list[1], self)
        self.folders.append(dir)

    def computeSize(self):
        size = 0
        for folder in self.folders:
            size += folder.computeSize()
        for file in self.files:
            size += file.size
        return size

    def getParent(self): return self.parent

    def render(self):
        delta_space = "--" * self.depth + " "
        print(delta_space + self.name)
        for file in self.files:
            print(delta_space + file.name)
        for folder in self.folders:
            folder.render()

    def findFolderLowerSize(self, size, out):
        if self.computeSize() < size:
            out.append(self.computeSize())
        for folder in self.folders:
            out = folder.findFolderLowerSize(size, out)
        return out

    def findFolderLargerThan(self, size, out):
        if self.computeSize() >= size:
            out.append(self.computeSize())
        for folder in self.folders:
            out = folder.findFolderLargerThan(size, out)
        return out

def is_dir(line_raw):
    return line_raw.startswith("dir")

root = Directory("/", None)
with open("input.txt") as file:
    lines = file.readlines()
    lines = [line.strip() for line in lines]
    
    currentDir = root
    
    i = 1
    while i < len(lines):
        line = lines[i]
        # print(line)
        if line.startswith("$ cd .."):
            currentDir = currentDir.getParent()
        elif line.startswith("$ cd "):
            folder_name = line.split(" ")[-1]
            new_folder = [folder for folder in currentDir.folders if folder.name == folder_name]
            if len(new_folder) != 1:
                root.render()
                print(currentDir.folders)
                raise("Unable to find dir " + new_folder)
            else: currentDir = new_folder[0]
        elif line.startswith("$ ls"):
            i+=1
            while i < len(lines) and not lines[i].startswith("$"):
                line = lines[i]
                # print(line)
                if is_dir(line): 
                    currentDir.addFolder(line)
                    # print([folder.name for folder in currentDir.folders])
                else: currentDir.addFile(line)
                i+=1
            i -= 1
        else:
            raise("This line is not managed: " + line)
        i+=1

# PART 1
# out = []
# root.findFolderLowerSize(100000, out)
# print(out)
# print(sum(out))
# # 1348005


# PART 2
MAX = 70000000
current_size = root.computeSize()
unused_space = MAX - current_size
unused_space = 30000000 - unused_space

out = []
root.findFolderLargerThan(unused_space, out)
print(out)
print(min(out))

# 45811471