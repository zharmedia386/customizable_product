from flask import Flask, request
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId
import time

cluster = MongoClient("mongodb+srv://zhar:zhar@cluster0.e99t7.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", tls=True, tlsAllowInvalidCertificates=True)

# Connect to the database
db = cluster["customizable_product"]

# Connect to the collection
users = db["users"]
orders = db["orders"]
items = db["items"]

# Create the application
app = Flask(__name__)

# Create the routes
@app.route("/", methods=["get", "post"])

# Create the function
def reply():
    # Get the message from the request
    text = request.form.get("message")
    
    # Get the user's contact from the request
    number = request.form.get("sender")

    # Response to the user
    res = {"reply": ""}

    # Check if the user is saved in the database
    user = users.find_one({"number": number})

    # Kaos Polos
    kaos_polos = items.find_one({"_id" : ObjectId("6298c1476c253522a321efea")})
    name_kaos_polos = kaos_polos["item_name"]
    link_kaos_polos = kaos_polos["photo"]
    jumlah_kaos_polos = kaos_polos["quantity"]

    # Kaos Motif
    kaos_motif = items.find_one({"_id" : ObjectId("6298c4646c253522a321eff4")})
    name_kaos_motif= kaos_motif["item_name"]
    link_kaos_motif= kaos_motif["photo"]
    jumlah_kaos_motif = kaos_motif["quantity"]

    # Kaos Jepang
    kaos_jepang = items.find_one({"_id" : ObjectId("6298c4646c253522a321eff5")})
    name_kaos_jepang= kaos_jepang["item_name"]
    link_kaos_jepang= kaos_jepang["photo"]
    jumlah_kaos_jepang = kaos_jepang["quantity"]

    # Kaos Custom
    kaos_custom = items.find_one({"_id" : ObjectId("6298c4646c253522a321eff6")})
    name_kaos_custom= kaos_custom["item_name"]

    #Tumbler Stainless
    tumbler_stain = items.find_one({"_id" : ObjectId("6298c5936c253522a321eff8")})
    name_tumbler_stain = tumbler_stain["item_name"]
    link_tumbler_stain = tumbler_stain["photo"]
    quantity_tumbler_stain = tumbler_stain["quantity"]

    #Tumbler Kaca
    tumbler_kaca = items.find_one({"_id" : ObjectId("6298c5936c253522a321eff9")})
    name_tumbler_kaca = tumbler_kaca["item_name"]
    link_tumbler_kaca = tumbler_kaca["photo"]
    quantity_tumbler_kaca = tumbler_kaca["quantity"]

    #Tumbler Motif
    tumbler_motif = items.find_one({"_id" : ObjectId("6298c5936c253522a321effa")})
    name_tumbler_motif = tumbler_motif["item_name"]
    link_tumbler_motif = tumbler_motif["photo"]
    quantity_tumbler_motif = tumbler_motif["quantity"]

    #Tumbler Custom
    tumbler_custom = items.find_one({"_id" : ObjectId("6298c5936c253522a321effb")})
    name_tumbler_custom = tumbler_custom["item_name"]

    # If the user is not saved in the database
    # FORM INPUT KALAU USERS PERTAMA KALI CHAT SAMA BOT
    if bool(user) == False:
        # Ask the user to register first
        res["reply"] += '\n\n' + ("Sebelum melanjutkan isikan data Anda berikut ini. \n\nNama: \nNomor WhatsApp: \nAlamat: ")
        res["reply"] += '\n\n' + ("*Catatan:*\nFormat yang Anda digunakan pastikan sesuai.\n\n*Contoh:*\nNama: Asep Mulyana\nNomor WhatsApp: 081123456789\nAlamat: Jl. Raya Bogor KM.5, Bogor")

        # Save the user's contact in the database        
        users.insert_one({"number": number, "status": "before_main", "cart" : []})

    # WELCOMING MESSAGE
    elif user["status"] == "before_main":
        # Check first if the user's new
        if "Nama: " in text and "Nomor WhatsApp: " in text and "Alamat: " in text:
            # Get the user's name, address, and No.WhatsApp from the request
            name = text[text.index('Nama: ') + len('Nama: '):text.index('\nNomor WhatsApp: ')]
            noWhatsApp = text[text.index('Nomor WhatsApp: ') + len('Nomor WhatsApp: '):text.index('\nAlamat: ')]
            address = text[text.index('Alamat: ') + len('Alamat: '):]

            # Welcome the user
            res["reply"] += '\n' + ("Halo, terima kasih telah menghubungi kami\nSelanjutnya, Anda dapat memilih salah satu menu di bawah ini:"
                        "\n\n*Ketik*\n\n 1️⃣ Untuk *memesan produk* \n 2️⃣ Untuk mengetahui *kontak penjual*\n 3️⃣ Untuk melihat *jam kerja* \n 4️⃣ "
                        "Untuk mendapatkan *alamat penjual*")
            res["reply"] += '\n\n' + ("Jika respon yang diberikan lambat, silahkan kirim pesan yang sama sebanyak 2 atau 3 kali\n"
                        "Hal ini mungkin terjadi karena koneksi buruk atau server yang sedang lambat")

            # Update the user's data in the database
            users.update_one({"number": number}, {"$set": {"status": "main", "name": name, "noWhatsApp": noWhatsApp, "address": address, "cart": []}})
        else:
            res["reply"] += '\n' + ("Harap menggunakan format yang sesuai.\n\n*Contoh:*\nNama: Asep Mulyana\nNomor WhatsApp: 081123456789\nAlamat: Jl. Raya Bogor KM.5, Bogor")

    # RESPON PILIHAN DARI WELCOMING MESSAGE
    elif user["status"] == "main":
        try:
            # Get the user's choice from the request
            option = int(text)
        except:
            # If the user's choice is not an integer
            res["reply"] += '\n' + ("Harap memasukkan sesuai dengan pilihan yang tersedia\n")
            res["reply"] += '\n' + ("Anda dapat memilih salah satu menu di bawah ini:"
                    "\n\n*Ketik*\n\n 1️⃣ Untuk *memesan produk* \n 2️⃣ Untuk mengetahui *kontak penjual*\n 3️⃣ Untuk melihat *jam kerja* \n 4️⃣ "
                    "Untuk mendapatkan *alamat penjual*")
            return str(res)

        # Process for every user's choice
        if option == 1: # Pemesanan Produk
            res["reply"] += '\n' + (
                "Anda dapat memilih pilihan produk yang tersedia:\n\n1️⃣ Kaos \n2️⃣ Tumbler\n0️⃣ Kembali")
            users.update_one(
                {"number": number}, {"$set": {"status": "ordering"}})
        elif option == 2: # Kontak Penjual
            res["reply"] += '\n' + (
                "Anda bisa menghubungi kami melalui.\nemail: customizable_product@gmail.com\nno telp: +6281542346842 (Admin)") 
        elif option == 3: # Jam Kerja
            res["reply"] += '\n' + ("Kami siap melayani anda dari hari senin - jumat pukul 07.00 - 19.00 WIB, dan hari sabtu - minggu pukul 13.00 - 19.00 WIB.")
        elif option == 4: # Alamat Penjual
            res["reply"] += '\n' + (
                "Jl. Ciwaruga No.50, Ciwaruga, Kec. Parongpong, Kabupaten Bandung Barat, Jawa Barat 40559")
        else:
            # if the input is exclude the available choice
            res["reply"] += '\n' + ("Harap memasukkan sesuai dengan pilihan yang tersedia\n")
            res["reply"] += '\n' + ("Anda dapat memilih salah satu menu di bawah ini:"
                    "\n\n*Ketik*\n\n 1️⃣ Untuk *memesan produk* \n 2️⃣ Untuk mengetahui *kontak penjual*\n 3️⃣ Untuk melihat *jam kerja* \n 4️⃣ "
                    "Untuk mendapatkan *alamat penjual*")

    # UDAH MILIH KAOS, TUMBLER, ATAU KEMBALI TERUS DIKEMANAIN
    elif user["status"] == "ordering":
        try:
            option = int(text)
        except:
            # If the user's choice is not an integer
            res["reply"] += '\n' + ("Harap memasukkan sesuai dengan pilihan yang tersedia\n")
            res["reply"] += '\n' + ("Anda dapat memilih salah satu menu di bawah ini:"
                    "\n\n*Ketik*\n\n 1️⃣ Untuk *memesan produk* \n 2️⃣ Untuk mengetahui *kontak penjual*\n 3️⃣ Untuk melihat *jam kerja* \n 4️⃣ "
                    "Untuk mendapatkan *alamat penjual*")
            return str(res)

        # KALAU MILIH KEMBALI
        if option == 0: # Kembali
            res["reply"] += '\n' + ("Halo, terima kasih telah menghubungi kami\nSelanjutnya, Anda dapat memilih salah satu menu di bawah ini:"
                    "\n\n*Ketik*\n\n 1️⃣ Untuk *memesan produk* \n 2️⃣ Untuk mengetahui *kontak penjual*\n 3️⃣ Untuk melihat *jam kerja* \n 4️⃣ "
                    "Untuk mendapatkan *alamat penjual*")
            res["reply"] += '\n\n' + ("Jika respon yang diberikan lambat, silahkan kirim pesan yang sama sebanyak 2 atau 3 kali\n"
                    "Hal ini mungkin terjadi karena koneksi buruk atau server yang sedang lambat")

            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})

        # KALAU MILIH KAOS
        elif option == 1: # Kaos
            # Response message
            res["reply"] += '\n' + ("Kaos tersedia dalam berbagai ukuran dan desain.")
            res["reply"] += '\n\n' + (f"Anda dapat memilih salah satu produk kaos di bawah ini: \n\nKetik\n\n"
                    f"1️⃣ *{name_kaos_polos}* \n {link_kaos_polos} \n Jumlah berdasarkan ukuran: \n S: {jumlah_kaos_polos['s']}   M: {jumlah_kaos_polos['m']}   L: {jumlah_kaos_polos['l']} \n XL: {jumlah_kaos_polos['xl']}   XXL: {jumlah_kaos_polos['xxl']}\n\n" 
                    f"2️⃣ *{name_kaos_motif}* \n {link_kaos_motif} \n Jumlah berdasarkan ukuran: \n S: {jumlah_kaos_motif['s']}   M: {jumlah_kaos_motif['m']}   L: {jumlah_kaos_motif['l']} \n XL: {jumlah_kaos_motif['xl']}   XXL: {jumlah_kaos_motif['xxl']}\n\n" 
                    f"3️⃣ *{name_kaos_jepang}* \n {link_kaos_jepang} \n Jumlah berdasarkan ukuran: \n S: {jumlah_kaos_jepang['s']}   M: {jumlah_kaos_jepang['m']}   L: {jumlah_kaos_jepang['l']} \n XL: {jumlah_kaos_jepang['xl']}   XXL: {jumlah_kaos_jepang['xxl']}\n\n" 
                    f"4️⃣ *{name_kaos_custom}* \n Kustomisasi kaos yang anda inginkan\n\n"
                    f"0️⃣ *Kembali*")

            # Connecting to Form_Kaos
            users.update_one(
                {"number": number}, {"$set": {"status": "form_kaos"}})
        
        # KALAU MILIH TUMBLER
        elif option == 2: #Tumbler
            # Response message
            res["reply"] += '\n' + ("Tumbler tersedia dalam berbagai volume dan desain.")
            res["reply"] += '\n\n' + (f"Anda dapat memilih salah satu produk tumbler di bawah ini: \n\nKetik\n\n"
                                      f"1️⃣ *{name_tumbler_stain} - stok: {quantity_tumbler_stain}* \n {link_tumbler_stain} \n\n"
                                      f"2️⃣ *{name_tumbler_kaca} - stok: {quantity_tumbler_kaca}* \n {link_tumbler_kaca} \n\n"
                                      f"3️⃣ *{name_tumbler_motif} - stok: {quantity_tumbler_motif}* \n {link_tumbler_motif} \n\n"
                                      f"4️⃣ *{name_tumbler_custom}* \n\n"
                                      f"0️⃣ *Kembali*")

            #Connection to form_tumbler
            users.update_one(
                {"number": number}, {"$set": {"status": "form_tumbler"}})
        else:
            # if the input is exclude the available choice
            res["reply"] += '\n' + ("Harap memasukkan sesuai dengan pilihan yang tersedia\n")
            res["reply"] += '\n' + (
                "Anda dapat memilih pilihan produk yang tersedia:\n\n1️⃣ Kaos \n2️⃣ Tumbler\n0️⃣ Kembali")

    elif user["status"] == "form_kaos":
        try:
            option = int(text)
        except:
            # If the user's choice is not an integer
            res["reply"] += '\n' + ("Kaos tersedia dalam berbagai ukuran dan desain.")
            res["reply"] += '\n\n' + (f"Anda dapat memilih salah satu produk kaos di bawah ini: \n\nKetik\n\n"
                    f"1️⃣ *{name_kaos_polos}* \n {link_kaos_polos} \n Jumlah berdasarkan ukuran: \n S: {jumlah_kaos_polos['s']}   M: {jumlah_kaos_polos['m']}   L: {jumlah_kaos_polos['l']} \n XL: {jumlah_kaos_polos['xl']}   XXL: {jumlah_kaos_polos['xxl']}\n\n" 
                    f"2️⃣ *{name_kaos_motif}* \n {link_kaos_motif} \n Jumlah berdasarkan ukuran: \n S: {jumlah_kaos_motif['s']}   M: {jumlah_kaos_motif['m']}   L: {jumlah_kaos_motif['l']} \n XL: {jumlah_kaos_motif['xl']}   XXL: {jumlah_kaos_motif['xxl']}\n\n" 
                    f"3️⃣ *{name_kaos_jepang}* \n {link_kaos_jepang} \n Jumlah berdasarkan ukuran: \n S: {jumlah_kaos_jepang['s']}   M: {jumlah_kaos_jepang['m']}   L: {jumlah_kaos_jepang['l']} \n XL: {jumlah_kaos_jepang['xl']}   XXL: {jumlah_kaos_jepang['xxl']}\n\n" 
                    f"4️⃣ *{name_kaos_custom}* \n Kustomisasi kaos yang anda inginkan\n\n"
                    f"0️⃣ *Kembali*")
            return str(res)

        # KALAU MILIH KEMBALI
        if option == 0: 
            res["reply"] += '\n' + (
                "Anda dapat memilih pilihan produk yang tersedia:\n\n1️⃣ Kaos \n2️⃣ Tumbler\n0️⃣ Kembali")
            users.update_one(
                {"number": number}, {"$set": {"status": "ordering"}})
            
        # KALAU MILIH KAOS POLOS, MOTIF, DAN JEPANG
        elif option == 1 or option == 2 or option == 3:
            # Form Kaos Polos, Motif, dan Jepang
            res["reply"] += '\n\n' + ("*Form Detail Pemesanan* \n Ukuran: [S/M/L/XL/XXL]\n Jumlah: ")
            res["reply"] += '\n\n' + ("*Catatan:*\n- Jumlah yang dipesan tidak melebihi stok yang tersedia\n- Format yang Anda digunakan pastikan sesuai.\n\nContoh:\nUkuran: L\nJumlah: 3 \n")
            
            users.update_one(
                {"number": number}, {"$set": {"status": "pesen_lagi_gak"}})

            # NAMA PRODUK YANG DIPILIH
            kaos = ["Kaos Polos", "Kaos Motif", "Kaos Jepang"]
            selected = (kaos[option - 1])
            users.update_one({"number": number}, {"$set": {"item": selected}})

        # KALAU MILIH KAOS KUSTOM
        elif option == 4: 
            # Form Kaos Kustom
            res["reply"] += '\n\n' + ("*Form Detail Pemesanan* \n Jenis kaos: [O-neck,Poloshirt]\n Panjang lengan: [panjang/pendek]\n Ukuran: [S/M/L/XL/XXL]\n Desain: \n Jumlah: ")
            res["reply"] += '\n\n' + ("*Catatan:*\nFormat yang Anda digunakan pastikan sesuai.\n\nContoh:\nJenis kaos: O-neck\n Panjang lengan: panjang\n Ukuran: L\n Desain: https://i.ytimg.com/vi/wSo8yMXIK8M/maxresdefault.jpg\n Jumlah: 1\n")

            users.update_one(
                {"number": number}, {"$set": {"status": "pesen_lagi_gak"}})

            # NAMA PRODUK YANG DIPILIH
            users.update_one({"number": number}, {"$set": {"item": "Kaos Custom"}})

        # MILIH DI LUAR KAOS POLOS, MOTIF, JEPANG, DAN KUSTOM
        else:
            # if the input is exclude the available choice
            res["reply"] += '\n' + ("Harap memasukkan sesuai dengan pilihan yang tersedia\n")
            res["reply"] += '\n\n' + (f"Anda dapat memilih salah satu produk kaos di bawah ini: \n\nKetik\n\n"
                    f"1️⃣ *{name_kaos_polos}* \n {link_kaos_polos} \n Jumlah berdasarkan ukuran: \n S: {jumlah_kaos_polos['s']}   M: {jumlah_kaos_polos['m']}   L: {jumlah_kaos_polos['l']} \n XL: {jumlah_kaos_polos['xl']}   XXL: {jumlah_kaos_polos['xxl']}\n\n" 
                    f"2️⃣ *{name_kaos_motif}* \n {link_kaos_motif} \n Jumlah berdasarkan ukuran: \n S: {jumlah_kaos_motif['s']}   M: {jumlah_kaos_motif['m']}   L: {jumlah_kaos_motif['l']} \n XL: {jumlah_kaos_motif['xl']}   XXL: {jumlah_kaos_motif['xxl']}\n\n" 
                    f"3️⃣ *{name_kaos_jepang}* \n {link_kaos_jepang} \n Jumlah berdasarkan ukuran: \n S: {jumlah_kaos_jepang['s']}   M: {jumlah_kaos_jepang['m']}   L: {jumlah_kaos_jepang['l']} \n XL: {jumlah_kaos_jepang['xl']}   XXL: {jumlah_kaos_jepang['xxl']}\n\n" 
                    f"4️⃣ *{name_kaos_custom}* \n Kustomisasi kaos yang anda inginkan\n\n"
                    f"0️⃣ *Kembali*")

    elif user["status"] == "form_tumbler":
        try:
            option = int(text)
        except:
            # If the user's choice is not an integer
            res["reply"] += '\n' + ("Tumbler tersedia dalam berbagai volume dan desain.")
            res["reply"] += '\n\n' + (f"Anda dapat memilih salah satu produk tumbler di bawah ini: \n\nKetik\n\n"
                                      f"1️⃣ *{name_tumbler_stain} - stok: {quantity_tumbler_stain}* \n {link_tumbler_stain} \n\n"
                                      f"2️⃣ *{name_tumbler_kaca} - stok: {quantity_tumbler_kaca}* \n {link_tumbler_kaca} \n\n"
                                      f"3️⃣ *{name_tumbler_motif} - stok: {quantity_tumbler_motif}* \n {link_tumbler_motif} \n\n"
                                      f"4️⃣ *{name_tumbler_custom}* \n\n"
                                      f"0️⃣ *Kembali*")
            return str(res)

        # KALAU MILIH KEMBALI
        if option == 0:
            res["reply"] += '\n' + (
                "Anda dapat memilih pilihan produk yang tersedia:\n\n1️⃣ Kaos \n2️⃣ Tumbler\n0️⃣ Kembali")
            users.update_one(
                {"number": number}, {"$set": {"status": "ordering"}})

        # KALAU MILIH TUMBLER STAIN, KACA, MOTIF
        elif option == 1 or option == 2 or option == 3:
            # Form Kaos Polos, Motif, dan Jepang
            res["reply"] += '\n\n' + ("*Form Detail Pemesanan* \n Jumlah: ")
            res["reply"] += '\n\n' + ("*Catatan:*\n- Jumlah yang dipesan tidak melebihi stok yang tersedia\n- Format yang Anda digunakan pastikan sesuai.\n\nJumlah: 3 \n")

            users.update_one(
                {"number": number}, {"$set": {"status": "pesen_lagi_gak"}})
            
            # NAMA PRODUK YANG DIPILIH
            tumbler = ["Tumbler Stainless 600ml", "Tumbler Kaca 1L", "Tumbler Motif 600ml"]
            selected = (tumbler[option - 1])
            users.update_one({"number": number}, {"$set": {"item": selected}})

        # KALAU MILIH TUMBLER KUSTOM
        elif option == 4:
            # Form Kaos Kustom
            res["reply"] += '\n\n' + ("*Form Detail Pemesanan* \n Volume: [600ml/1L]\n Desain: \n Jumlah: ")
            res["reply"] += '\n\n' + ("*Catatan:*\nFormat yang Anda digunakan pastikan sesuai.\n\nContoh:\nVolume: 1L\n Desain: https://i.ytimg.com/vi/wSo8yMXIK8M/maxresdefault.jpg\n Jumlah: 1\n")

            users.update_one(
                {"number": number}, {"$set": {"status": "pesen_lagi_gak"}})
            
            # NAMA PRODUK YANG DIPILIH
            users.update_one({"number": number}, {"$set": {"item": "Tumbler Custom"}})

        # MILIH DI LUAR TUMBLER STAIN, KACA, MOTIF, DAN KUSTOM
        else:
            # if the input is exclude the available choice
            res["reply"] += '\n' + ("Harap memasukkan sesuai dengan pilihan yang tersedia\n")
            res["reply"] += '\n\n' + (f"Anda dapat memilih salah satu produk tumbler di bawah ini: \n\nKetik\n\n"
                                      f"1️⃣ *{name_tumbler_stain} - stok: {quantity_tumbler_stain}* \n {link_tumbler_stain} \n\n"
                                      f"2️⃣ *{name_tumbler_kaca} - stok: {quantity_tumbler_kaca}* \n {link_tumbler_kaca} \n\n"
                                      f"3️⃣ *{name_tumbler_motif} - stok: {quantity_tumbler_motif}* \n {link_tumbler_motif} \n\n"
                                      f"4️⃣ *{name_tumbler_custom}* \n\n"
                                      f"0️⃣ *Kembali*")

    elif user["status"] == "pesen_lagi_gak":
    # KAOS
        # Kustom (2)
        if "Jenis kaos: " in text and "Panjang lengan: " in text  and "Ukuran: " in text and "Desain: " in text and "Jumlah: " in text:
            jenis_2 = text[text.index('Jenis kaos: ') + len('Jenis kaos: '):text.index('\nPanjang lengan: ')]
            panjang_lengan_2 = text[text.index('Panjang lengan: ') + len('Panjang lengan: '):text.index('\nUkuran: ')]
            ukuran_2 = text[text.index('Ukuran: ') + len('Ukuran: '):text.index('\nDesain: ')]
            desain_2 = text[text.index('Desain: ') + len('Desain: '):text.index('\nJumlah: ')]
            jumlah_2 = text[text.index('Jumlah: ') + len('Jumlah: '):]

            item_selected = users.find_one({"number": number})["item"]

            # MASUKIN CART
            users.update_one({"number": number}, {"$push": {"cart": {"item_name": item_selected, "jenis_kaos": jenis_2, "panjang_lengan": panjang_lengan_2, "ukuran": ukuran_2, "desain": desain_2, "jumlah": jumlah_2}}})
            
        # Polos, Motif, dan Jepang (1)
        elif "Ukuran: " in text and "Jumlah: " in text:
            ukuran_1 = text[text.index('Ukuran: ') + len('Ukuran: '):text.index('\nJumlah: ')]
            jumlah_1 = text[text.index('Jumlah: ') + len('Jumlah: ')]
            
            item_selected = users.find_one({"number": number})["item"]

            # MASUKIN CART
            users.update_one({"number": number}, {"$push": {"cart": {"item_name": item_selected, "ukuran": ukuran_1, "jumlah": jumlah_1}}})
    
    # TUMBLER
        # Kustom (4)
        elif "Volume: " in text and "Desain: " in text  and "Jumlah: " in text:
            volume_4 = text[text.index('Volume: ') + len('Volume: '):text.index('\nDesain: ')]
            desain_4 = text[text.index('Desain: ') + len('Desain: '):text.index('\nJumlah: ')]
            jumlah_4 = text[text.index('Jumlah: ') + len('Jumlah: '):]

            item_selected = users.find_one({"number": number})["item"]

            # MASUKIN CART
            users.update_one({"number": number}, {"$push": {"cart": {"item_name": item_selected, "volume": volume_4, "desain": desain_4, "jumlah": jumlah_4}}})

        # Stain, Kaca, Motif, dan Kustom (3)
        elif "Jumlah: " in text:
            jumlah_3 = text[text.index('Jumlah: ') + len('Jumlah: ')]
            
            item_selected = users.find_one({"number": number})["item"]

            # MASUKIN CART
            users.update_one({"number": number}, {"$push": {"cart": {"item_name": item_selected, "jumlah": jumlah_3}}})

        # PESEN LAGI NGGAK
        cart = user["cart"]
        
        n = 1
        res["reply"] += '\n' + ("Pilihan menarik! 😉")
        res["reply"] += '\n\n' + ("Pesanan  Anda: ")
        time.sleep(1)
        for item in cart:
            if item["item_name"] == "Kaos Polos" or item["item_name"] == "Kaos Motif" or item["item_name"] == "Kaos Jepang":
                res["reply"] += '\n' + (f"*{n}. {item['item_name']} - {item['ukuran']} - {item['jumlah']}*")
            
            elif item["item_name"] == "Kaos Custom":
                res["reply"] += '\n' + (f"*{n}. {item['item_name']} - {item['jenis_kaos']} - {item['panjang_lengan']} - {item['ukuran']} - {item['desain']} - {item['jumlah']}*")
            
            elif item["item_name"] == "Tumbler Stainless 600ml" or item["item_name"] == "Tumbler Kaca 1L" or item["item_name"] == "Tumbler Motif 600ml":
                res["reply"] += '\n' + (f"*{n}. {item['item_name']} {item['jumlah']}*")

            elif item["item_name"] == "Tumbler Custom":
                res["reply"] += '\n' + (f"*{n}. {item['item_name']} - {item['volume']} - {item['desain']} - {item['jumlah']}*")
            
            n += 1
    
        res["reply"] += '\n\n' + ("Apakah anda ingin memesan yang lain?\n")
        res["reply"] += '\n' + ("1️⃣ Ya, saya ingin memesan lagi produk lainnya \n2️⃣ Tidak, sudah cukup")      

        users.update_one(
                {"number": number}, {"$set": {"status": "pending"}})

    elif user["status"] == "pending":
        try:
            option = int(text)
        except:
            res["reply"] += '\n\n' + ("Apakah anda ingin memesan yang lain?")
            res["reply"] += '\n' + ("1️⃣ Ya, saya ingin memesan lagi produk lainnya \n2️⃣ Tidak, sudah cukup")   
            return str(res)
        
        if option == 1:
            res["reply"] += '\n' + (
                "Anda dapat memilih pilihan produk yang tersedia:\n\n1️⃣ Kaos \n2️⃣ Tumbler\n0️⃣ Kembali")
            users.update_one(
                {"number": number}, {"$set": {"status": "ordering"}})
        elif option == 2:
            users.update_one(
                {"number": number}, {"$set": {"status": "form_bayar"}})

            res["reply"] += '\n\n' + ("*Form Detail Pengiriman* \n Alamat Penerima: \n Nama Penerima: \n Telp. Penerima: \n")
            res["reply"] += '\n\n' + ("*Catatan:*\nFormat yang Anda digunakan pastikan sesuai.\n\nContoh:\nAlamat Penerima: Jln. Mars no.15, Kecamatan Padasuka\nNama Penerima: Asep Mulyana\nTelp. Penerima: 0851-4235-2321\n")

    elif user["status"] == "form_bayar":
        if "Alamat Penerima: " in text and "Nama Penerima: " in text and "Telp. Penerima: " in text:
            alamat_penerima = text[text.index('Alamat Penerima: ') + len('Alamat Penerima: '):text.index('\nNama Penerima: ')]
            nama_penerima = text[text.index('Nama Penerima: ') + len('Nama Penerima: '):text.index('\nTelp. Penerima: ')]
            telp_penerima = text[text.index('Telp. Penerima: ') + len('Telp. Penerima: '):]

        # MASUKIN KE ORDERS

        res["reply"] += "\n" +  "Terima kasih telah berbelanja di toko kami! 😊\n\n"
        res["reply"] += "\n" +  "Pesanan dapat dibayarkan melalui transfer bank ke rekening berikut:\n\n"
        res["reply"] += "\n" +  "Bank Mandiri: \n"
        res["reply"] += "\n" +  "No. Rekening: 0987654321\n"
        res["reply"] += "\n" +  "Atas Nama: PT. Customizable Product\n"

        users.update_one(
            {"number": number}, {"$set": {"status": "ordered"}})
        users.update_one({"number": number}, {"$unset": {"item": ""}})

    elif user["status"] == "ordered":
        # Welcome the user
        res["reply"] += '\n' + ("Halo, terima kasih telah menghubungi kami\nSelanjutnya, Anda dapat memilih salah satu menu di bawah ini:"
                    "\n\n*Ketik*\n\n 1️⃣ Untuk *memesan produk* \n 2️⃣ Untuk mengetahui *kontak penjual*\n 3️⃣ Untuk melihat *jam kerja* \n 4️⃣ "
                    "Untuk mendapatkan *alamat penjual*")
        res["reply"] += '\n\n' + ("Jika respon yang diberikan lambat, silahkan kirim pesan yang sama sebanyak 2 atau 3 kali\n"
                    "Hal ini mungkin terjadi karena koneksi buruk atau server yang sedang lambat")

    return str(res)


if __name__ == "__main__":
    app.run(port=5050)