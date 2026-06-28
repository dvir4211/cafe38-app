import streamlit as st
import sqlite3

# ==========================================
# 1. נתוני המסעדה (הכל מרוכז כאן לניהול קל)
# ==========================================
food_menu = [
    {"name": "אומלט פטריות", "cat": "בוקר", "desc": "חביתה ממולאת פטריות צלויות, מחית כמהין, מוצרלה ומסקרפונה. סלט קטן ולחם קסטן.", "preg": 1, "vegan": 0, "gf": 0, "notes": "מכיל לקטוז וגלוטן. לחם ללג אפשרי.", "preg_note": ""},
    {"name": "אומלט WD (אבוקדו)", "cat": "בוקר", "desc": "טוסט קאסטן, אבוקדו, מקושקשת, פרמזן, רומסקו וביארנז.", "preg": 1, "vegan": 0, "gf": 0, "notes": "מכיל לקטוז וגלוטן.", "preg_note": "רק WD וללא רוטב ביארנז"},
    {"name": "בנדיקט", "cat": "בוקר", "desc": "בריוש צלוי, סלמון / אווז / תרד, ביצים עלומות, הולנדייז ועירית.", "preg": 0, "vegan": 0, "gf": 0, "notes": "לא לנשים בהיריון! ביצים עלומות חצי חיות.", "preg_note": ""},
    {"name": "כריך סלט ביצים", "cat": "בוקר", "desc": "לחם מחמצת לבן, בצל מקורמל, סלט ביצים (מכיל צלפים), שאלוט פריך ועירית.", "preg": 1, "vegan": 0, "gf": 0, "notes": "לא ניתן להוציא צלפים.", "preg_note": ""},
    {"name": "קרוק מאדאם", "cat": "בוקר", "desc": "טוסט קסטן, גבינת אמנטל, פרמזן, חזה אווז וחרדל. ביצת עין, בשמל וסלט.", "preg": 0, "vegan": 0, "gf": 0, "notes": "לא ניתן להוציא אווז/גבינות מהטוסט.", "preg_note": ""},
    {"name": "גרנולה שלנו", "cat": "בוקר", "desc": "שיבולת שועל, שקדים, גרעינים, מייפל. מוגש עם יוגורט בקר, דבש ופירות.", "preg": 1, "vegan": 0, "gf": 0, "notes": "מכיל גלוטן ולקטוז.", "preg_note": ""},
    {"name": "פרנץ' טוסט", "cat": "בוקר", "desc": "בריוש מטוגן, מסקרפונה, קרמל מלוח, פרי העונה.", "preg": 1, "vegan": 0, "gf": 0, "notes": "מכיל גלוטן ולקטוז.", "preg_note": ""},
    {"name": "פנקייק", "cat": "בוקר", "desc": "3 יחידות עם אנגלז חמאה חומה, מסקרפונה, מייפל ואוכמניות.", "preg": 1, "vegan": 0, "gf": 0, "notes": "מכיל גלוטן ולקטוז.", "preg_note": ""},
    {"name": "צלחת גבינות", "cat": "ערב", "desc": "3 גבינות משתנות (ברי, קמבזולה, מנצ'גו), ריבה, פירות וקרקרים ללג.", "preg": 1, "vegan": 0, "gf": 1, "notes": "מכיל לקטוז, ללא גלוטן.", "preg_note": ""},
    {"name": "סלט קיסר", "cat": "ערב", "desc": "חסה קיסר, רוטב (שמנת חמוצה, חרדל, פרמזן, אנשובי - ללא ביצים), קרוטונים ובצל.", "preg": 1, "vegan": 0, "gf": 0, "notes": "מכיל גלוטן ולקטוז.", "preg_note": ""},
    {"name": "סלט עגבניות מגי", "cat": "ערב", "desc": "עגבניות רכות, בצל סגול, זעתר, צ'ילי חריף, רוקט, קרם פטה, שמן זית ולימון.", "preg": 1, "vegan": 0, "gf": 1, "notes": "ללא גלוטן.", "preg_note": ""},
    {"name": "טרטר דג ים", "cat": "ערב", "desc": "50 גרם דג ים, שעועית ירוקה, שקדים, צ'ילי, עירית, מוגש עם יוגורט בקר.", "preg": 0, "vegan": 0, "gf": 1, "notes": "לא מתאים להיריון! דג נא.", "preg_note": ""},
    {"name": "טרטר בקר", "cat": "ערב", "desc": "שייטל קצוץ, שומשום, עירית, צ'ילי אדום. איולי שום ירוק וטוסטונים.", "preg": 0, "vegan": 0, "gf": 0, "notes": "לא מתאים להיריון. בשר נא.", "preg_note": ""},
    {"name": "ברוקולי בגריל פחמים", "cat": "ערב", "desc": "על רומסקו, שמן זית, פרמזן וסחוג ירוק.", "preg": 1, "vegan": 1, "gf": 1, "notes": "טבעוני וללא לקטוז רק ללא פרמזן.", "preg_note": ""},
    {"name": "פטריות יער", "cat": "ערב", "desc": "פטריות ירדן פחם, סחוג, שמן זית, קרם שקדים, זרעי חמנייה.", "preg": 1, "vegan": 1, "gf": 1, "notes": "טבעוני לחלוטין וללא גלוטן.", "preg_note": ""},
    {"name": "פאקרי לחי עגל", "cat": "ערב", "desc": "150 גרם לחי עגל ביין אדום וירקות שורש, רוטב חמאה ושום, פסטה פאקרי ופרמזן.", "preg": 1, "vegan": 0, "gf": 0, "notes": "לא כשר! מכיל לקטוז וגלוטן.", "preg_note": ""},
    {"name": "המבורגר בקר", "cat": "ערב", "desc": "180 גרם בקר, גבינת צ'דר, איולי חרדל, שאלוט פריך, צ'יפס.", "preg": 1, "vegan": 0, "gf": 0, "notes": "מכיל גלוטן ולקטוז.", "preg_note": "חובה מידת עשייה WD וללא איולי חרדל"},
    {"name": "עוגת גבינה באסקית", "cat": "קינוח", "desc": "עוגת גבינה קלאסית, אפויה ומושחתת.", "preg": 0, "vegan": 0, "gf": 1, "notes": "לא מתאימה להיריון! מכיל ביצים חצי אפויות.", "preg_note": ""},
    {"name": "סמורס", "cat": "קינוח", "desc": "אנגלז חמאה חומה, קרמו שוקולד, קרמבל קקאו, מרשמלו שרוף.", "preg": 1, "vegan": 0, "gf": 1, "notes": "ללא גלוטן (ללג). מכיל ביצים ולקטוז.", "preg_note": ""}
]

cocktails_list = [
    {"n": "Jasmin 38 (ג'זמין 38)", "i": "45 סלואו ג'ין | 22.5 קמפרי | 22.5 ליקר רובארב | 22.5 מיץ לימון", "p": "שקשוק וסינון לקרח חדש — כוס לואו בול, פלח תפוז"},
    {"n": "Smoky Paloma (סמוקי פלומה)", "i": "30 טקילה | 15 מזקל | 15 ליקר אשכוליות | 22.5 לימון | טיפות מלח | סגירה בסודה", "p": "שקשוק, סינון כפול, סגירה בסודה אשכוליות — היי בול, פלח תפוז"},
    {"n": "Hamara Cosmo (חמרה קוסמו)", "i": "45 וודקה ציפורן | 22.5 מיץ רימונים | 22.5 לימון | 15 קואנטרו | 15 מקציף | 15 מי סוכר", "p": "שקשוק רטוב ואז שקשוק יבש, סינון כפול — כוס מרגריטה"},
    {"n": "Torino spritz (טורינו שפריץ)", "i": "60 ורמוט אדום (קוקי) | סגירה בפרוסקו ובסודה", "p": "בנייה ישירה בכוס מלאה בקרח — כוס יין, פלח תפוז"},
    {"n": "Inca Gold", "i": "30 פיסקו | 15 ליקר פסיפלורה | 30 לימון | 22.5 מי סוכר | סגירה בפרוסקו", "p": "שקשוק וסינון, סגירה בפרוסקו — כוס מרגריטה"},
    {"n": "דאטה ביאנקה", "i": "30 ג'ין | 30 קינה אפרטיף | 15 מאנצינו סקו | 15 ודטה ביאנקו | דש ביטר תפוז", "p": "ערבוב בכוס ערבוב (Stir) — כוס ניק ונורה, טוויסט לימון"},
    {"n": "Trinidad 10", "i": "22.5 אנגסטורה ביטרס | 45 רוזטת אגוזי לוז | 30 ברבן | 15 לימון | דש ליין | מקציף", "p": "שקשוק רטוב ויבש, סינון כפול — כוס מרגריטה, זסט לימון אובש"},
    {"n": "Alpine Daiquiri", "i": "45 רום מתוסלם פלטינו | 30 דולין דריי | 22.5 לימון | 15 ז'נפי | 22.5 מייפל חריף", "p": "שקשוק בשייקר, חצי רים שאטה — כוס מרגריטה"},
    {"n": "Aviation", "i": "45 ג'ין | 22.5 לימון | 15 ליקר סיגליות | 15 מרסקינו | מקציף", "p": "שקשוק רטוב ויבש — כוס מרגריטה, דובדבן אמרנה בתחתית"},
    {"n": "Naked & Famous", "i": "22.5 מזקל | 22.5 שרטרז צהוב | 22.5 אפרול | 22.5 לימון", "p": "שקשוק חזק בשייקר וסינון כפול — כוס מרגריטה, תפוז מיובש"},
    {"n": "נגרוני הבית / טינטורטו", "i": "30 בלנד ורמוטים של הבית | 30 קמפרי | 30 ג'ין | 22.5 מיץ לימון", "p": "ערבוב בכוס ערבוב וסינון — כוס לואו בול, קוביות קרח גדולות"},
    {"n": "אספרסו מרטיני קלאסי", "i": "60 וודקה | 15 ליקר קפה | 10 מי סוכר | מנת אספרסו חם טרי", "p": "שקשוק אגרסיבי עם המון קרח לסינון קצף סמיך — כוס ניק ונורה, פולי קפה"},
    {"n": "וויסקי סאוור", "i": "60 ברבן | 30 מיץ לימון | 22.5 מי סוכר | 15 מקציף חלבון", "p": "שקשוק יבש (בלי קרח) ואז רטוב (עם קרח) — לואו בול, דש אנגסטורה למעלה"},
    {"n": "באזיל סמאש", "i": "60 ג'ין | 30 מיץ לימון | 22.5 מי סוכר | 6-8 עלי בזיליקום טריים", "p": "כתישת בזיליקום עדינה בתחתית השייקר, שקשוק וסינון כפול — לואו בול עם קרח"},
    {"n": "מרגריטה קלאסית", "i": "45 טקילה בלאנקו | 30 קואנטרו | 30 מיץ לימון טרי", "p": "שקשוק חזק וסינון — כוס מרגריטה עם חצי רים מלח"}
]

checklists_data = [
    ("פתיחה", "לעשות אצבע (שעון נוכחות) מיד בכניסה למשמרת"),
    ("פתיחה", "סידור ביוב, שטיחי בר ושטיח צ'קר חיצוני"),
    ("פתיחה", "הורדת מנה בכל ראש של מכונת הקפה (לזרוק, לא לשימוש)"),
    ("פתיחה", "הורדת קונדומים מבקבוקי האלכוהול והלבשת פוררים נקיים"),
    ("פתיחה", "חיתוך פירות טריים למשמרת: לימונים ותפוזים לפלחים/זסטים"),
    ("פתיחה", "הוצאת בקבוקי אלכוהול רלוונטיים ממקרר המטבח ישירות לאמבטיות"),
    ("פתיחה", "מילוי קרח בבר — חובה 3 אמבטיות מלאות לחלוטין!"),
    ("פתיחה", "סידור קו הבר מימין לשמאל: פרח -> מלח פלפל -> נר"),
    ("פתיחה", "הכנת מי סוכר ותרכיז מאצ'ה טרי לכל היום"),
    ("סגירה", "קידום סגירה: סגירת ראש אחד במכונה, מילוי סכו\"ם, ניקוי מגירת קפה ומטחנה"),
    ("סגירה", "ניקוי יסודי של ברז הבירה ואיזור השטיחים/משטחים עם סקוץ' וסבון"),
    ("סגירה", "שפיכת מים רותחים על כל הפוררים (בחוץ, לא כשהם בתוך הבקבוק!) והבקבוקים"),
    ("סגירה", "כתיבת תאריך פתיחה מדויק על בקבוקי יין פתוחים והחזרתם למקרר"),
    ("סגירה", "ניקוי צ'ייסרים ואזור ספיד (לרוקן קרח, שטיחים, מגש ניקוז עם סקוץ' וסבון)"),
    ("סגירה", "ניקוי מכונת הקפה, שטיפת ראשים עם עיוור, והחלפת מגבת סטימר"),
    ("סגירה", "החלפת שקיות זבל בכל הבר ושטילת הפחים מאחוריהם"),
    ("סגירה", "ניקוי כסאות הבר עם סמרטוט לח — ורק אז הפיכתם על הבר"),
    ("ראשון", "בוקר: הקפאת מקפיא חזרה, ניקוי אקסטרות | ערב: ניקיון דיספליי ורמוטים ומדף ביטרים"),
    ("שני", "בוקר: ניקיון דיספליי ג'ין, כוסות יין ובירה | ערב: שטיפת קונדומים ושמפניירות בסבון"),
    ("שלישי", "בוקר: דיספליי וויסקי וטקילה | ערב: ניקיון מדף אקסטרות ומגירת קופה"),
    ("רביעי", "בוקר: ניקוי יסודי של מקרר יין לבן (לרוקן, לשפשף עם סקוץ' וסבון)"),
    ("חמישי", "בוקר: הכנת נענע לסופ\"ש (4 ליטר תפזורת ו-4 תפרחת) | ערב: סידור מגירת סכו\"ם"),
    ("שישי", "ערב: ניקיון יסודי של מגירת תה, מלח ופלפל של השולחנות"),
    ("שבת", "ערב: הפשרת המקפיא לחלוטין לצורך ניקוי שבועי")
]

# ==========================================
# 2. מנוע בניית ה-SQL (אוטומטי בענן!)
# ==========================================
@st.cache_resource
def init_db():
    conn = sqlite3.connect('cafe38.db')
    cursor = conn.cursor()
    
    cursor.execute('DROP TABLE IF EXISTS food')
    cursor.execute('DROP TABLE IF EXISTS cocktails')
    cursor.execute('DROP TABLE IF EXISTS checklists')
    
    cursor.execute('''CREATE TABLE food (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, category TEXT, description TEXT, is_vegan BOOLEAN, is_gf BOOLEAN, is_preg_safe BOOLEAN, preg_note TEXT, notes TEXT)''')
    cursor.execute('''CREATE TABLE cocktails (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, glass_prep TEXT, ingredients TEXT)''')
    cursor.execute('''CREATE TABLE checklists (id INTEGER PRIMARY KEY AUTOINCREMENT, type TEXT, task TEXT)''')
    
    for item in food_menu:
        cursor.execute('INSERT INTO food (name, category, description, is_vegan, is_gf, is_preg_safe, preg_note, notes) VALUES (?,?,?,?,?,?,?,?)', (item['name'], item['cat'], item['desc'], item['vegan'], item['gf'], item['preg'], item['preg_note'], item['notes']))
    for c in cocktails_list:
        cursor.execute('INSERT INTO cocktails (name, glass_prep, ingredients) VALUES (?,?,?)', (c['n'], c['p'], c['i']))
    for t in checklists_data:
        cursor.execute('INSERT INTO checklists (type, task) VALUES (?,?)', (t[0], t[1]))
        
    conn.commit()
    conn.close()
    return True

# הרצת פונקציית הבנייה - זה מה שיסדר לך את השגיאה בענן!
init_db()

def fetch_data(query, params=()):
    conn = sqlite3.connect('cafe38.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows

# ==========================================
# 3. ממשק האפליקציה (UI)
# ==========================================
st.set_page_config(page_title="CAFÉ 38 | צוות", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;600;800&display=swap');
    * { font-family: 'Assistant', sans-serif !important; direction: rtl !important; text-align: right !important; }
    .stApp { background-color: #fcfbf9; }
    h1 { font-size: clamp(2.2rem, 6vw, 4rem) !important; color: #1e3799; font-weight: 800 !important; text-align: center !important; margin-bottom: 25px;}
    h2 { font-size: clamp(1.6rem, 4vw, 2.2rem) !important; color: #2c3e50; font-weight: 600 !important; margin-top: 20px;}
    .card { background: white; padding: 20px; border-radius: 18px; margin-bottom: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.03); border: 1px solid #eaeaea; }
    .card-food { border-right: 10px solid #ff6b81; }
    .card-cocktail { border-right: 10px solid #f39c12; background-color: #fffdf9; }
    .card-task { border-right: 10px solid #16a085; }
    .item-title { font-size: clamp(1.3rem, 3.5vw, 1.7rem); font-weight: 800; color: #1e272e; margin-bottom: 8px;}
    .item-desc { font-size: clamp(1rem, 2.8vw, 1.25rem); color: #485460; line-height: 1.5; margin-bottom: 12px;}
    .ingredients-box { background: #f1f2f6; padding: 12px 18px; border-radius: 10px; font-size: clamp(1.05rem, 3vw, 1.3rem); color: #2f3542; font-weight: 600; line-height: 1.6; border-left: 4px solid #f39c12; margin-top: 10px; }
    .item-notes { font-size: clamp(0.95rem, 2.5vw, 1.15rem); color: #c23616; font-weight: 600; background: #ffebee; padding: 6px 12px; border-radius: 8px; display: inline-block; margin-top: 10px;}
    .tag { font-size: clamp(0.8rem, 2.2vw, 0.95rem); font-weight: 600; padding: 4px 10px; border-radius: 6px; display: inline-block; margin: 4px 0 4px 6px; }
    .t-veg { background: #e8f5e9; color: #2e7d32; }
    .t-gf { background: #fff8e1; color: #f57f17; }
    .t-preg { background: #e3f2fd; color: #1565c0; }
    .t-warn { background: #ffebee; color: #c62828; }
    .stTabs [data-baseweb="tab"] { font-size: clamp(1rem, 3vw, 1.4rem) !important; font-weight: 600 !important; }
</style>
""", unsafe_allow_html=True)

if 'role' not in st.session_state:
    st.session_state.role = None

def set_role(role):
    st.session_state.role = role

if st.session_state.role is None:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; margin-bottom: 50px;">
        <h1 style="font-size: clamp(3.5rem, 10vw, 6rem) !important; color: #1e3799; font-weight: 800 !important; letter-spacing: 4px; margin-bottom: 0;">CAFÉ 38</h1>
        <p style="font-size: clamp(1.2rem, 4vw, 1.8rem); color: #7f8fa6; margin-top: -10px; font-weight: 600;">ברוכים הבאים למשמרת</p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
    with col2: st.button("🍸 ברמן", on_click=set_role, args=("bartender",), use_container_width=True)
    with col3: st.button("📝 מלצר", on_click=set_role, args=("waiter",), use_container_width=True)

elif st.session_state.role == "waiter":
    col1, col2 = st.columns([8, 2])
    with col1: st.markdown("<h2>🍽️ תפריט ומחלקות אוכל</h2>", unsafe_allow_html=True)
    with col2: st.button("איפוס ↩", on_click=set_role, args=(None,))
    
    f_col1, f_col2, f_col3, f_col4 = st.columns(4)
    filter_type = "הכל"
    if f_col2.button("🌱 טבעוני", use_container_width=True): filter_type = "vegan"
    if f_col3.button("🤰 היריון", use_container_width=True): filter_type = "preg"
    if f_col4.button("🌾 ללא גלוטן", use_container_width=True): filter_type = "gf"
    if f_col1.button("הכל", use_container_width=True): filter_type = "הכל"

    query = "SELECT * FROM food WHERE 1=1"
    if filter_type == "vegan": query += " AND is_vegan = 1"
    if filter_type == "preg": query += " AND is_preg_safe = 1"
    if filter_type == "gf": query += " AND is_gf = 1"
    
    items = fetch_data(query)
    for item in items:
        tags = ""
        if item["is_vegan"]: tags += "<span class='tag t-veg'>🌱 טבעוני</span>"
        if item["is_gf"]: tags += "<span class='tag t-gf'>🌾 ללא גלוטן</span>"
        if item["is_preg_safe"]:
            tags += f"<span class='tag t-preg'>🤰 היריון: {item['preg_note'] if item['preg_note'] else 'מאושר'}</span>"
        else:
            tags += "<span class='tag t-warn'>🚫 לא להיריון</span>"

        st.markdown(f"""
        <div class="card card-food">
            <div class="item-title">{item['name']} <span style="font-size:14px; color:#aaa;">[{item['category']}]</span></div>
            <div class="item-desc">{item['description']}</div>
            <div>{tags}</div>
            <div class="item-notes">מידע חיוני: {item['notes']}</div>
        </div>
        """, unsafe_allow_html=True)

elif st.session_state.role == "bartender":
    col1, col2 = st.columns([8, 2])
    with col1: st.markdown("<h2>🍸 עמדת בר ומשימות</h2>", unsafe_allow_html=True)
    with col2: st.button("איפוס ↩", on_click=set_role, args=(None,))
    
    tab1, tab2, tab3 = st.tabs(["🍹 מתכוני קוקטיילים", "🌅 צ'קליסט משמרת", "📅 משימות יומיות"])
    
    with tab1:
        cocktails = fetch_data("SELECT * FROM cocktails")
        for c in cocktails:
            ingredients_html = c['ingredients'].replace(" | ", "<br>• ")
            st.markdown(f"""
            <div class="card card-cocktail">
                <div class="item-title" style="color:#1e3799;">{c['name']}</div>
                <div class="item-desc"><b>טכניקה וכוס:</b> {c['glass_prep']}</div>
                <div class="ingredients-box">
                    <span style="color:#7f8fa6; font-size:13px; display:block; margin-bottom:5px;">רכיבים לבנייה:</span>
                    • {ingredients_html}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    with tab2:
        st.markdown("<h3>📋 נהלי פתיחה וסגירה </h3>", unsafe_allow_html=True)
        col_open, col_close = st.columns(2)
        with col_open:
            st.markdown("<h4 style='color:#16a085;'>🌅 פתיחת בר</h4>", unsafe_allow_html=True)
            open_tasks = fetch_data("SELECT * FROM checklists WHERE type='פתיחה'")
            for t in open_tasks:
                st.markdown(f"<div class='card card-task' style='padding:10px;'>✔️ {t['task']}</div>", unsafe_allow_html=True)
        with col_close:
            st.markdown("<h4 style='color:#c0392b;'>🌌 סגירת בר</h4>", unsafe_allow_html=True)
            close_tasks = fetch_data("SELECT * FROM checklists WHERE type='סגירה'")
            for t in close_tasks:
                st.markdown(f"<div class='card card-task' style='padding:10px; border-right-color:#c0392b;'>🛑 {t['task']}</div>", unsafe_allow_html=True)

    with tab3:
        st.markdown("<h3>📅 משימות ניקיון שבועיות קבועות</h3>", unsafe_allow_html=True)
        days = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי", "שבת"]
        for day in days:
            day_tasks = fetch_data("SELECT * FROM checklists WHERE type=?", (day,))
            if day_tasks:
                st.markdown(f"#### יום {day}")
                for t in day_tasks:
                    st.markdown(f"<div class='card card-task' style='border-right-color:#8e44ad; padding:12px;'>📅 {t['task']}</div>", unsafe_allow_html=True)
