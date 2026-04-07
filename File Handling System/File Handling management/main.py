import os

def create_file(filename):
        try:
            with open(filename,"x")as f:
                print(f"File {filename}: CREATED SUCCESSFULLY")
        except FileExistsError:
             print(f"File {filename}: ALREADY EXISTED!")
        except Exception as E:
             print("An Error Occurred!")

def view_all_files():
    files=os.listdir()
    if not files:
          print("File dont Exist")
    else:
         print("files existed")
         for file in files:
              print(file)
             
def delete_file(filename):
    try:
        os.remove(filename)
        print("File Deleted Successfully")
    except FileNotFoundError:
        print("File not Existed!")
    except Exception as E:
         print("An Error Occurred!")

def read_file(filename):
    try:
        with open(filename,"r") as f:
            content=f.read()
            print(f"Content of {filename}:\n{content}")
    except FileNotFoundError:
        print("File not found!")
    except Exception as E:
        print("An Error Occured!")

def edit_file(filename):
    try:
        with open(filename,"a") as f:
            content=input("Enter data :")
            f.write(content + "\n")
            print("Content added succesfully")
    except FileNotFoundError:
        print("File not Found!")
    except Exception as E:
        print("An Error Occured!")
         
def main():
    while True:
        print("-----------FILE MANAGEMENT AAP-------------")
        n=input('Print q for quit or press ENTER for continue :').lower()
        if(n=="q"):
            print("Goodbye!")
            break
        else:
            choice=int(input("Press 1 for Create File,\nPress 2 for View all File,\nPress 3 for Delete File,\nPress 4 for Read File,\nPress 5 for Edit File\n"))
            if(choice==1):
                filename=input("Enter your File name here :")
                create_file(filename)
            elif(choice==2):
                view_all_files()
            elif(choice==3):
                filename=input("Enter your File name here :")
                delete_file(filename)    
            elif(choice==4):
                filename=input("Enter your File name here :")
                read_file(filename)
            elif(choice==5):
                filename=input("Enter your File name here :")
                edit_file(filename)
            else:
                print("Write a number between (1-5)")                

if __name__=="__main__":
    main()

         

     
         
                

   
