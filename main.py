from flask import Flask, request
from pymongo import MongoClient
from datetime import datetime

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

    # If the user is not saved in the database
    if bool(user) == False:
        # Ask the user to register first
        res["reply"] += '\n\n' + ("Sebelum melanjutkan isikan data Anda berikut ini. \n\nNama: \nNomor WhatsApp: \nAlamat: ")
        res["reply"] += '\n\n' + ("*Catatan:*\nFormat yang Anda digunakan pastikan sesuai.\n\n*Contoh:*\nNama: Asep Mulyana\nNomor WhatsApp: 081123456789\nAlamat: Jl. Raya Bogor KM.5, Bogor")
        
        # Save the user's contact in the database        
        users.insert_one({"number": number, "status": "before_main", "cart" : []})
    elif user["status"] == "before_main":
        # Welcome the user
        res["reply"] += '\n' + ("Halo, terima kasih telah menghubungi kami\nSelanjutnya, kamu dapat memilih salah satu menu di bawah ini:"
                    "\n\n*Ketik*\n\n 1️⃣ Untuk *memesan produk* \n 2️⃣ Untuk mengetahui *kontak penjual*\n 3️⃣ Untuk melihat *jam kerja* \n 4️⃣ "
                    "Untuk mendapatkan *alamat penjual*")
        res["reply"] += '\n\n' + ("Jika respon yang diberikan lambat, silahkan kirim pesan yang sama sebanyak 2 atau 3 kali\nHal ini mungkin terjadi karena koneksi buruk atau server yang sedang lambat")
        
        # Get the user's name, address, and No.WhatsApp from the request
        name = text[text.index('Nama: ') + len('Nama: '):text.index('\nNomor WhatsApp: ')]
        noWhatsApp = text[text.index('Nomor WhatsApp: ') + len('Nomor WhatsApp: '):text.index('\nAlamat: ')]
        address = text[text.index('Alamat: ') + len('Alamat: '):]

        # Update the user's data in the database
        users.update_one({"number": number}, {"$set": {"status": "main", "name": name, "noWhatsApp": noWhatsApp, "address": address, "cart": []}})
    elif user["status"] == "main":
        try:
            option = int(text)
        except:
            # if the input is exclude the available choice
            res["reply"] += '\n' + ("Please enter a valid response \n")
            res["reply"] += '\n' + ("You can choose from one of the options below: "
                    "\n\n*Type*\n\n 1️⃣ To *contact* us \n 2️⃣ To *order* snacks \n 3️⃣ To know our *working hours* \n 4️⃣ "
                    "To get our *address*")
            return str(res)

        if option == 1:
            res["reply"] += '\n' + (
                "Anda bisa menghubungi kami melalui \nemail : customizable_product@gmail.com\nno telp : +6281542346842 (Admin)") 
        elif option == 2:
            res["reply"] += '\n' + ("You have entered *ordering mode*.")
            users.update_one(
                {"number": number}, {"$set": {"status": "ordering"}})
            res["reply"] += '\n' + (
                "You can select one of the following cakes to order: \n\n1️⃣ Red Velvet  \n2️⃣ Dark Forest \n3️⃣ Ice Cream Cake"
                "\n4️⃣ Plum Cake \n5️⃣ Sponge Cake \n6️⃣ Genoise Cake \n7️⃣ Angel Cake \n8️⃣ Carrot Cake \n9️⃣ Fruit Cake  \n0️⃣ Go Back")
        elif option == 3:
            res["reply"] += '\n' + ("We work from *9 a.m. to 5 p.m*.")
        elif option == 4:
            res["reply"] += '\n' + (
                "We have multiple stores across the city. Our main center is at *Cibiru, Bandung*")
        else:
            # if the input is exclude the available choice
            res["reply"] += '\n' + ("Please enter a valid response \n")
            res["reply"] += '\n' + ("You can choose from one of the options below: "
                    "\n\n*Type*\n\n 1️⃣ To *contact* us \n 2️⃣ To *order* snacks \n 3️⃣ To know our *working hours* \n 4️⃣ "
                    "To get our *address*")
    elif user["status"] == "ordering":
        try:
            option = int(text)
        except:
            # if the input is exclude the available choice
            res["reply"] += '\n' + ("Please enter a valid response \n")
            res["reply"] += '\n' + ("You can choose from one of the options below: "
                    "\n\n*Type*\n\n 1️⃣ To *contact* us \n 2️⃣ To *order* snacks \n 3️⃣ To know our *working hours* \n 4️⃣ "
                    "To get our *address*")
            return str(res)
        if option == 0:
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})
            res["reply"] += '\n' + ("Go back to previous page")
            res["reply"] += '\n' + ("You can choose from one of the options below: "
                        "\n\n*Type*\n\n 1️⃣ To *contact* us \n 2️⃣ To *order* snacks \n 3️⃣ To know our *working hours* \n 4️⃣ "
                        "To get our *address*")
        elif 1 <= option <= 9:
            cakes = ["Red Velvet Cake", "Dark Forest Cake", "Ice Cream Cake",
                     "Plum Cake", "Sponge Cake", "Genoise Cake", "Angel Cake", "Carrot Cake", "Fruit Cake"]
            selected = (cakes[option - 1])
            users.update_one({"number": number}, {"$push": {"item": selected}})
            users.update_one(
                {"number": number}, {"$set": {"status": "pending"}})

            # selected_print : spesifik menu yg dipilih user tertentu
            selected_print = users.find_one({"number": number})
            print(selected_print["item"])
            print_temp = selected_print["item"]
            res["reply"] += '\n' + ("Excellent choice 😉")
            res["reply"] += '\n' + (f"You already choose *{', '.join(print_temp)}*. Is there any other choices?")
            res["reply"] += '\n\n' + ("1️⃣ Yes, i want to order other cakes \n2️⃣ No, it's enough")          
        else:
            # if the input is exclude the available choice
            res["reply"] += '\n' + ("Please enter a valid response \n")
            res["reply"] += '\n' + (
                "You can select one of the following cakes to order: \n\n1️⃣ Red Velvet  \n2️⃣ Dark Forest \n3️⃣ Ice Cream Cake"
                "\n4️⃣ Plum Cake \n5️⃣ Sponge Cake \n6️⃣ Genoise Cake \n7️⃣ Angel Cake \n8️⃣ Carrot Cake \n9️⃣ Fruit Cake  \n0️⃣ Go Back")
    elif user["status"] == "pending":
        selected_print = user["item"]
        try:
            option = int(text)
        except:
            # if the input is exclude the available choice
            print(selected_print)
            res["reply"] += '\n' + ("Please enter a valid response \n")
            res["reply"] += '\n' + (f"You already choose *{', '.join(selected_print)}*. Is there any other choices?")
            res["reply"] += '\n\n' + ("1️⃣ Yes, i want to order another cakes \n2️⃣ No, it's enough")
            return str(res)

        if option == 1 :
            res["reply"] += '\n' + ("You have entered *ordering mode*.")
            users.update_one(
                {"number": number}, {"$set": {"status": "ordering"}})
            res["reply"] += '\n' + (
                "You can select one of the following cakes to order: \n\n1️⃣ Red Velvet  \n2️⃣ Dark Forest \n3️⃣ Ice Cream Cake"
                "\n4️⃣ Plum Cake \n5️⃣ Sponge Cake \n6️⃣ Genoise Cake \n7️⃣ Angel Cake \n8️⃣ Carrot Cake \n9️⃣ Fruit Cake  \n0️⃣ Go Back")
        if option == 2 :
            users.update_one(
                {"number": number}, {"$set": {"status": "address"}})
            res["reply"] += '\n' + ("Please enter your address to confirm the order")
    elif user["status"] == "address":
        selected_print = user["item"]
        res["reply"] += "\n" +  "Thanks for shopping with us 😊"
        res["reply"] += "\n" +  f"Your order for *{', '.join(selected_print)}* has been received and will be delivered within an hour"
        orders.insert_one({"number": number, "item": selected_print, "address": text, "order_time": datetime.now()})
        users.update_one(
            {"number": number}, {"$set": {"status": "ordered"}})
        users.update_one({"number": number}, {"$set": {"item": []}})
    elif user["status"] == "ordered":
        res["reply"] += "\n" +  ("Hi, thanks for contacting again.\nYou can choose from one of the options below: "
                     "\n\n*Type*\n\n 1️⃣ To *contact* us \n 2️⃣ To *order* snacks \n 3️⃣ To know our *working hours* \n 4️⃣ "
                     "To get our *address*")
        res["reply"] += '\n\n' + ("If there's any late responds, Please send the same message until 2 or 3 times due to connection and server speed")
        users.update_one(
            {"number": number}, {"$set": {"status": "before_main"}})
    # users.update_one({"number": number}, {"$push": {"messages": {"text": text, "date": datetime.now()}}})
    return str(res)


if __name__ == "__main__":
    app.run(port=5000)
