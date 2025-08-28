#read content of input.txt
with open('input.txt', 'r') as file:
    content = file.read()

#count the number of words
word_count = len(content.split())

#convert all text to uppercase
NewContent = content.upper()

#write the processed content to output.txt
with open('output.txt', 'a') as file:
    file.write(NewContent)
    
print("output.txt has been created with the processed content.")