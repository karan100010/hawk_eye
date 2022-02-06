#write a fuction that takes google sheets as input and returns a json object
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from newspaper import Article
import requests
from datetime import datetime

from torch import prelu   
def read_google_sheet_to_json(sheet):
   
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name( secret_key,scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet).sheet1
    data = sheet.get_all_records()
    return data


 # given a link scrape the news,title,date_published artical using the newspaper3k library and return a json object

def news_scraper(link):
    article = Article(link)
    article.download()
    article.parse()
    article.nlp()
    data = {
        'title': article.title,
        'link': link,
        'date': article.publish_date,
        'text': article.text,
        "summary": article.summary,
    "date_scraped": datetime.now()  }
    return data
    
    

 #create a postgresql table 


#create a fuction that takes a list of json objects ,name of the table and user and inserts them into a postgresql table three parameters link,title,text

theme_dict={
    "Adolescent Health":["Adolescent Abortion","Adolescent Anaemia (WIFS)","Adolescent Child bearing","Adolescent Counselling","Adolescent Nutrition","AFHS Clinic","Cyber crime","Deworming","Drug abuse","Knowledge of contraceptives and early pregnancy","Menstrual hygiene","Adolescent Mental health","PEER Education Program","RKSK","Sex abuse","Sexual and reproductive health Education, (including myths and misconceptions","Teenage pregnancy","Tobacco and alcohol use"],
"Child Health": ["AEFI-Routine Immunization","Child Death or U5MR","Child Nutrition","Complementary feeding","Diarrhoea","Exclusive Breastfeeding","HBYC","Malnutrition","Measles rubella","NRC","Pneumonia","RBSK","Routine Immunization"],
"Communicable Diseases":["Dengue","Filaria","Hepatitis","Integrated Disease Surveillance Programme (IDSP)","JE/AES","Kala-Azar","Malaria","National AIDS Control Programme (NACP)","National Leprosy Eradication Programme (NLEP)","National Programme on Containment of Anti-Microbial Resistance (AMR)","National Rabies Control Programme","National Tuberculosis Elimination Programme","National Viral Hepatitis Control Program ","Programme for Prevention and Control of leptospirosis","Pulse Polio Programme","Seasonal Diseases","Typhoid","Zika Virus"],
"Health System Strengthening":["Asha Anganwadi and ANM combined meetings","Aanganwadi training","Acre gradation of doctors", 
"Acre gradation of Paramedical staff",
"Ambulance Services",
"ANM training",
"ASHA training",
"Bio Waste Management",
"Chaos at health facility",
"District ranking",
"Doctors training"
"Equipment’s",
"Facility Ranking", 
"Health and wellness centres",
"Health Camps/Days",
"Infection and Prevention Management",
"Kayakalp Awards",
"Lab technician training",
"Medical negligence", 
"Medicines",
"Monitoring Visits",
"Negligence in services",
"New Government Announcements",
"New program Launch", 
"Nurse mentor training",
"OPD Services",
"Pradhan Sammelan",
"Resumption of Services",
"Service awards", 
"Strike/Protest",
"Study/Research Reports",
"Up-Gradation of health facility",
"VHSND (Village health sanitation and nutrition day)",
"Workshops/Seminars",
"Ayushman Bharat Digital Mission (ADHM)",
"Ayushman Bharat Yojana PMJAY",
"Infrastructure Related",
"Blood bank",
"PM Ayushman Bharat Health Infrastructure Mission",
"Pradhan Mantri Swasthya Suraksha Yojana (PMSSY)"
],
"Maternal Health":["ANC Check-up",
"Anemia management",
"Birth Preparedness",
"C-Section",
"Early Registration of Pregnancy",
"FRU operationalization",
"HDU ICU for complicated delivery infertility management",
"High Risk Pregnancy",
"Home Deliveries",
"Institutional Deliveries",
"JSSK (Janani Shishu surksha karykram)",
"Maternal Death/MMR/MDR",
"Maternal Nutrition",
"Maternity Benefits (JSY)",
"Maternity Benefits (PMMY)",
"Non Institutional Deliveries",
"PMSA Day",
"Postnatal Care"

],
"National Nutrition Program":["Integrated Child Development Services (ICDS)",
"MAA (Mothers’ Absolute Affection) Programme for Infant and Young Child Feeding",
"Mid-Day Meal Programme",
"National Iodine Deficiency Disorders Control Programme",
"National Iron Plus Initiative for Anaemia Control",
"National Programme for Prevention and Control of Fluorosis (NPPCF)",
"National Vitamin A prophylaxis Programme"],
"Newborn Health":["Birth Asphyxia", 
"Colostrum feeding",
"DEIC(District Early intervention center)",
"Early initiation of breastfeeding",
"First dose-BCG",
"HBNC",
"Infant Death/IMR/CDR",
"IYCF (Infant Young child feeding)",
"Kangaroo Mother Care",
"Low birth Weight",
"Navjat Shishu surakha karykram",
"NBCU",
"Newborn care corner",
"Newborn Stabilisation unit",
"NICU",
"Reduction in morbidity and mortality due to ARI and Diarrhoea",
"SNCU",
"Still Birth"

],
"Non Communicable Diseases":["Alzheimer’s disease",
"Anti Drug campaign",
"Arthritis",
"Blindness",
"Cerebral palsy",
"Control Treatment of Occupational Diseases",
"Health Care for the Elderly (NPHCE)",
"Jaundice",
"Lip cleft (transfer in RBSK)",
"Mental Health Programme",
"National Oral Health programme",
"National Tobacco Control Program(NTCP)",
"NPCDCS",
"NPPCD",
"Pradhan Mantri National Dialysis Program",
"Prevention & Management of Burn Injuries (NPPMBI)",
"Sickle cell anemia"],
"Reproductive health":["Abortion",
"Condoms"
"Counselling"
"Discontinuation of service due to side effect",
"Family planning indemnity scheme",
"Fix days services",
"Injectable MPA ( Antara Program)",
"IUCD",
"Khushaal parivar diwas",
"Dampati sampark pakhwada",
"Janshankhya sthirikaran pakhwada",
"ANTARA Diwas",
"NSV Day",
"Oral contraceptive pills",
"PPIUCD and PAIUCD",
"Saas bahu beta Sammelan",
"Sterilization Female",
"Sterilization Male",
"Supply/demand FPLMIS",
"FP awareness",
"Migration",
"Myths and misconception"
],
"State Program":["ANMOL APP",
"Atal Swasthya Mela", 
"AYUSH Programme",
"Ayushman Bharat (MMJAY)",
"Balika Samriddhi yojana",
"Child line_1098",
"KSY",
"MANTRA APP",
"Mission shakti",
"SBY",
"Special ability",
"15+Vaccination",
"18+ vaccination", 
"45+ vaccination", 
"60+ vaccination", 
"Advisory for Vaccination", 
"AEFI Covid Vaccination", 
"Appeal for Vaccination", 
"Booster Dose",
"Child vaccination (under 1 years)",
"Cluster Approach",
"Door to Door Vaccination",
"Front line workers vaccination", 
"Health worker vaccination",
"Vaccination Camps",
"Vaccination Hesitancy",
"Vaccination Certificate"],
"Covid appropriate Behavior (CAB)":["Authentic Sources seeking",
"Avoid spitting",
"Avoid touching eyes, nose and mouth",
"Avoid unnecessary travel",
"Discourage crowds",
"Hand Washing",
"Maintain Distance",
"Mental Health-Covid",  
"Reusable mask",
"Sanitization/Cleaning services",
"Toll free helpline",
"Violation of guideline"],
"Stigma and Discrimination":["Appeal",
"Corona survivors",
"Corona warriors"],
"Covid Other Reports":["Awareness",
"AYUSH Covid",
"Bio-medical waste",
"Case Detection",
"Contact Tracing",
"Corona Help desk", 
"Covid death",
"COVID facilities",
"Covid Medication",
"Cremation",
"Donation",
"Covid Government Announcement",
"Covid Government guidelines", 
"Covid Government Initiatives",
"Isolation",
"Lock down",
"Maternal Health in COVID",
"Migrant labourers’ issues",
"Monitoring visits",  
"Motivating report",
"New variant",
"Oxygen Plants",
"Oxygen Supply",
"PPE kits",
"Quarantine",
"Recovery rate",
"Covid Research/Study",
"Surveillance Committees",
"Testing",
"Covid Training", 
"Covid Webinar"]


}
#search a term with google search api in python
#restrict the serch to only the past week


def search(term):
    page_index=0
    all_links=[]
    while True:
        search_url = "https://www.googleapis.com/customsearch/v1?key=AIzaSyAT6MMtfiG24pdVoF8Fh3pYLgkZr7Zm39c&cx=291b60e6939d20fef&q={}&start={}".format(term,page_index)
        response = requests.get(search_url)
        json_response = response.json()
        try:
            links=[i['link'] for i in json_response['items']]
        except:
            print("Error in getting links")
            return all_links    
        all_links=all_links+links
        print(len(all_links))
        if len(links)<10:
            print("done")
            break
        else:
            page_index+=10
            
    return all_links


#converting a dataframe with columns links, discription ,text ,title to a dataframe with columns links, discription ,text ,title, category
# into a rss stream
def to_rss(df):
    rss_stream=[]
    for i in df.index:
        rss_stream.append({"link":df.loc[i,"link"],"description":df.loc[i,"description"],"text":df.loc[i,"text"],"title":df.loc[i,"title"],"category":df.loc[i,"category"]})
    return rss_stream
    

 

 