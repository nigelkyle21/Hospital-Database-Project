import pymysql
from pymongo import MongoClient

# MySQL connection 
print("Connecting to MySQL...")
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='HSP_DB',
    charset='utf8mb4'
)
cursor = conn.cursor(pymysql.cursors.DictCursor)
print("Connected to MySQL ✅")

# MongoDB connection
print("Connecting to MongoDB...")
mongo = MongoClient("mongodb://localhost:27017/")
db = mongo["HSP_NoSQL"]
collection = db["patients"]
print("Connected to MongoDB ✅")

collection.drop()  # clear old data

# Helper queries 
def get_admissions(subject_id):
    cursor.execute("SELECT * FROM ADMISSIONS WHERE SUBJECT_ID=%s", (subject_id))
    return cursor.fetchall()

def get_icustays(subject_id, hadm_id):
    cursor.execute("SELECT * FROM ICUSTAYS WHERE SUBJECT_ID=%s AND HADM_ID=%s",
                   (subject_id, hadm_id))
    return cursor.fetchall()

def get_diagnoses(subject_id, hadm_id):
    cursor.execute("""
        SELECT d.SEQ_NUM, d.ICD9_CODE, dd.SHORT_TITLE, dd.LONG_TITLE
        FROM DIAGNOSES_ICD d
        JOIN D_ICD_DIAGNOSES dd ON d.ICD9_CODE = dd.ICD9_CODE
        WHERE d.SUBJECT_ID=%s AND d.HADM_ID=%s
    """, (subject_id, hadm_id))
    return cursor.fetchall()

def get_notes(subject_id, hadm_id):
    cursor.execute("""
        SELECT ROW_ID, CHARTDATE, CHARTTIME, STORETIME,
               CATEGORY, E_DESCRIPTION, CGID, ISERROR, E_TEXT
        FROM NOTEEVENTS
        WHERE SUBJECT_ID=%s AND HADM_ID=%s
        LIMIT 100
    """, (subject_id, hadm_id))
    return cursor.fetchall()

# Load patients
print("Loading patients…")
cursor.execute("SELECT * FROM PATIENTS")
patients = cursor.fetchall()
print(f"Found {len(patients)} patients ✔")

# --- Migration ---
for p in patients:
    sid = p["SUBJECT_ID"]
    print(f"\nProcessing patient SUBJECT_ID={sid}…")

    patient_doc = {
        "_id": sid,
        "gender": p["GENDER"],
        "dob": str(p["DOB"]),
        "dod": str(p["DOD"]) if p["DOD"] else None,
        "expire_flag": p["EXPIRE_FLAG"],
        "admissions": []
    }

    admissions = get_admissions(sid)
    print(f"  {len(admissions)} admissions found")

    for a in admissions:
        hadm = a["HADM_ID"]
        print(f"    Admission HADM_ID={hadm}")

        adm_doc = {
            "hadm_id": hadm,
            "admittime": str(a["ADMITTIME"]),
            "dischtime": str(a["DISCHTIME"]),
            "admission_type": a["ADMISSION_TYPE"],
            "admission_location": a["ADMISSION_LOCATION"],
            "discharge_location": a["DISCHARGE_LOCAITON"],
            "insurance": a["INSURANCE"],
            "diagnosis": a["DIAGNOSIS"],
            "hospital_expire_flag": a["HOSPITAL_EXPIRE_FLAG"],
            "has_chartevents_data": a["HAS_CHARTEVENTS_DATA"],
            "icu_stays": [],
            "diagnoses": [],
            "notes": []
        }

        adm_doc["icu_stays"] = get_icustays(sid, hadm)
        adm_doc["diagnoses"] = get_diagnoses(sid, hadm)
        adm_doc["notes"] = get_notes(sid, hadm)

        patient_doc["admissions"].append(adm_doc)

    collection.insert_one(patient_doc)
    print("    Inserted into MongoDB ✅")

print("\n------------------------------------")
print("        MIGRATION COMPLETED      ")
print("------------------------------------")