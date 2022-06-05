# https://stackoverflow.com/questions/58823411/how-to-getindex-certain-phrase-from-the-middle-of-the-string-in-python#:~:string=The%20syntax%20string%5Bstart%3Aend,%2C%20use%20len(word)%20.

# string = 'FORM DETAIL PEMESANAN: \n Nama: Asep Mulyana\nNomor WhatsApp: 081123456789\nAlamat: Jl. Raya Bogor KM.5, Bogor'

# string_produk = 'Jenis : Polo\nPanjang Lengan : Panjang\nBahan : Plastisol\nUkuran : XL'

# name = string[string.index('Nama: ') + len('Nama: '):string.index('\nNomor WhatsApp: ')]
# noWhatsApp = string[string.index('Nomor WhatsApp: ') + len('Nomor WhatsApp: '):string.index('\nAlamat: ')]
# address = string[string.index('Alamat: ') + len('Alamat: '):]

# jenis = string[string.index('Jenis : ') + len('Jenis : '):string.index('\nPanjang Lengan : ')]
# panjang_lengan = string[string.index('Panjang Lengan : ') + len('Panjang Lengan : '):string.index('\nBahan : ')]
# bahan = string[string.index('Bahan : ') + len('Bahan : '):string.index('\nUkuran : ')]
# ukuran = string[string.index('Ukuran : ') + len('Ukuran : '):]

# if "Nama: " in string and "Nomor WhatsApp: " in string and "Alamat: " in string:
#     print(name)
#     print(noWhatsApp)
#     print(address)
# print(address)

string = 'Ukuran: L\nJumlah: 3'

ukuran = string[string.index('Ukuran: ') + len('Ukuran: '):string.index('\nJumlah: ')]
jumlah = string[string.index('Jumlah: ') + len('Jumlah: ')]

print(jumlah)
print(ukuran)