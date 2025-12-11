# Hospital Database Project  
*A complete relational and NoSQL data modeling project*

This repository contains my SOEN 363 (Database Systems) term project at Concordia University.  
It demonstrates SQL relational modeling, ERD design, analytical querying, NoSQL document modeling, and a Python migration script that transforms data from a relational database into MongoDB documents.

This project models a simplified hospital information system, including patients, stays, diagnoses, and medical events.

---

## 🏥 Project Overview

This project represents the full design and implementation of a hospital database system.  
It covers every stage of database development:

### ✔ Relational Model (MySQL)
- Conceptual & logical schema design  
- Fully normalized relational schema  
- Primary & foreign keys  
- SQL `CREATE TABLE` implementation  
- Complex analytical queries using `JOIN`, `GROUP BY`, `HAVING`, and filtering  
- ERD diagrams showing entity relationships  

### ✔ NoSQL Model (MongoDB)
- Patient-centric document model  
- Embedding for high-cohesion attributes (diagnoses, ICU stays)  
- Referencing for large collections (events, lab data)  
- Example JSON documents  
- Document modeling explanations  

### ✔ Migration Script
The `migrate_to_nosql.py` script demonstrates how relational data can be converted into a NoSQL document model using Python.

It:
- Connects to MySQL & MongoDB  
- Reads relational rows  
- Transforms them into nested JSON documents  
- Inserts them into MongoDB collections  

This shows how schema migration works in real-world systems.

---

## 🛠 Technologies Used
- **MySQL / MariaDB** – relational schema & queries  
- **MongoDB** – NoSQL document model  
- **Python 3** – migration script  
- **PyMySQL / PyMongo** – database drivers  
- **Draw.io** – ERD diagrams  
- **JSON** – document representation  

---

## 🔍 Key Features

### 🔹 Relational Model
- Fully structured hospital schema  
- ERD diagrams for Phase 1 & Phase 2  
- Analytical SQL queries (e.g., patient statistics, diagnosis counts)  
- Focus on database normalization & consistency  

### 🔹 NoSQL Model
- Flexible document design  
- Embedded subdocuments for patient-centric access  
- Referenced collections for scalable event data  
- Indexing strategy and modeling decisions included  

### 🔹 Migration Workflow
- Demonstrates SQL → NoSQL data transformation  
- Shows flattening of relational joins into nested JSON  
- Realistic pipeline similar to ETL processes  

