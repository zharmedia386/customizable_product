# https://stackoverflow.com/questions/58823411/how-to-get-certain-phrase-from-the-middle-of-the-string-in-python#:~:text=The%20syntax%20string%5Bstart%3Aend,%2C%20use%20len(word)%20.

string = 'Nama : M Azhar Alauddin Alamat : Bandung'

nama = string[string.index('Nama : ') + len('Nama : '):string.index(' Alamat : ')]
alamat = string[string.index('Alamat : ') + len('Alamat : '):]
print(alamat)