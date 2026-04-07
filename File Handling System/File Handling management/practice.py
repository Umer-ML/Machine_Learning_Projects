file=open("Sample.txt","w")
file.write("Hello i am Omar")
file.close
file=open("Sample.txt","r")
content=print(f"Hello ji janab ,{file.read()}")
file.close()

