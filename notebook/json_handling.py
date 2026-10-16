'''import json

with open("data/document.json","r") as file:
    data=json.load(file)
    
print(data)
print(type(data))

print(data["text"])
print(data["source"])
print(data["page"])'''

'''import json

data={
    "text":"Embedding represent text as vectors",
    "source":"embedding.pdf",
    "page":8
}

with open("data/new_document.json","w")as file:
    json.dump(data,file,indent=4)'''
    
    
import json

with open("data/chunks.json","r") as file:
    chunks=json.load(file)
    
for chunk in chunks:
    print("Text: ",chunk["text"])
    print("Source: ",chunk["source"])
    print("PageNo: ",chunk["page"])
    