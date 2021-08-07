word = "this is a sentence with two is"
list = word.split()

for item in list:
    if item == "is":
        list.remove(item)
        break
word = " ".join(list)

print(word)