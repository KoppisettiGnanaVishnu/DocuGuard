'''with open("data/sample.txt","r") as file:
    text1=file.readlines()
    
print(text1)

print(type(text1))'''

'''with open("data/sample.txt","r") as file:
    for line in file:
        print(line.strip())'''
        

'''with open("data/output.txt","w") as file:
    file.write("This is my first RAG document")'''
    
'''with open("data/output.txt","a") as file:
    file.write("\nThis is a new line added")'''
    
    
def read_document(filename):
    with open(filename,"r") as file:
        text=file.read()
        
    return text

text=read_document("data/sample.txt")
print(text)

    