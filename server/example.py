import mmap

filepath='/home/pi/Desktop/server/variables.txt'


file_object=open(filepath,mode="r",encoding="utf8")
mmap_object=mmap.mmap(file_object.fileno(),length=0,access=mmap.ACCESS_READ,offset=0)

mmap_object.seek(0)

print(mmap_object.readline())
print(mmap_object.tell())
print(mmap_object.readline())
print(mmap_object.tell())
print(mmap_object.readline())
print(mmap_object.tell())