
# 💊 PharmaGo - Medical Supplies Delivery Platform

**PharmaGo** is a web application designed for the fast and reliable delivery of urgent medical supplies.
 Whether you're in need of everyday health essentials or emergency medication, PharmaGo ensures you get
 what you need—right when you need it. 🚚⚕️

---

## 🌟 Features

- 🔐 **User Authentication** – Register, login, and logout securely.
- 🛍️ **Product Catalog** – Browse medical products with detailed descriptions.
- 🔎 **Search Functionality** – Quickly find specific medicines and supplies.
- 🛒 **Shopping Cart** – Add/remove items and manage your selections.
- 🚚 **Flexible Delivery Options** – Choose from Standard, Express, Eco-Friendly, or Click & Collect.
- 📦 **Order Placement & Tracking** – Real-time updates on your delivery status.
- 👤 **User Account Management** – View order history and manage personal details.
- 📱 **Responsive Design** – Works seamlessly on desktops, tablets, and mobile devices.

---

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Database**: MySQL
- **Frontend**: HTML, CSS, JavaScript, Bootstrap

---

## ⚙️ Installation and Setup

Follow the steps below to get PharmaGo up and running locally:

### 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Configure the Database

Start your MySQL server using a tool like XAMPP, MAMP, or directly via terminal.

Update your environment variables in the `.env` file or directly in the config if needed:

```env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=my_sql_pass
MYSQL_DB=pharmago
```

### 3️⃣ Initialize the Database

```bash
python init_db.py
```

### 4️⃣ Run the Application

```bash
python run.py
```
