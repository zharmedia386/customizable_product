from flask import Flask, request
from pymongo import MongoClient
from datetime import datetime

cluster = MongoClient("mongodb+srv://zhar:zhar@cluster0.e99t7.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", tls=True, tlsAllowInvalidCertificates=True)

db = cluster["customizable_product"]
users = db["users"]
orders = db["orders"]

app = Flask(__name__)


@app.route("/", methods=["get", "post"])
def reply():
    text = request.form.get("message")
    number = request.form.get("sender")
    res = {"reply": ""}
    user = users.find_one({"number": number})
    users_print = users.find_one({ "number": 'zharmedia' })
    if bool(user) == False:
        res["reply"] += '\n' + ("Hi, thanks for contacting *The Red Velvet*.\nYou can choose from one of the options below: "
                    "\n\n*Type*\n\n 1️⃣ To *contact* us \n 2️⃣ To *order* snacks \n 3️⃣ To know our *working hours* \n 4️⃣ "
                    "To get our *address*")
        res["reply"] += '\n\n' + ("If there's any late responds, Please send the same message until 2 or 3 times due to connection and server speed")
        users.insert_one({"number": number, "status": "main", "messages": [], "item" : []})
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
                "You can contact us through phone or e-mail.\n\n*Phone*: +62-xxxx-xxxx \n*E-mail* : redvelvet@gmail.com") 
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
            {"number": number}, {"$set": {"status": "main"}})
    users.update_one({"number": number}, {"$push": {"messages": {"text": text, "date": datetime.now()}}})
    return str(res)


if __name__ == "__main__":
    app.run(port=5000)
