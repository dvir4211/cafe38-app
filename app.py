import streamlit as st
import sqlite3

def fetch_data(query, params=()):
    conn = sqlite3.connect('cafe38.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows

st.set_page_config(page_title="CAFÉ 38 | צוות", layout="wide", initial_sidebar_state="collapsed")

# ---------------------------------------------------------
# CSS מודרני, אחיד ויוקרתי המותאם ללמידה במובייל
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;600;800&display=swap');
    
    * {
        font-family: 'Assistant', sans-serif !important;
        direction: rtl !important;
        text-align: right !important;
    }
    
    .stApp { background-color: #fcfbf9; }
    
    h1 { font-size: clamp(2.2rem, 6vw, 4rem) !important; color: #1e3799; font-weight: 800 !important; text-align: center !important; margin-bottom: 25px;}
    h2 { font-size: clamp(1.6rem, 4vw, 2.2rem) !important; color: #2c3e50; font-weight: 600 !important; margin-top: 20px;}
    
    /* כרטיסיות מידע משופרות ללמידה */
    .card {
        background: white;
        padding: 20px;
        border-radius: 18px;
        margin-bottom: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        border: 1px solid #eaeaea;
    }
    
    .card-food { border-right: 10px solid #ff6b81; }
    .card-cocktail { border-right: 10px solid #f39c12; background-color: #fffdf9; }
    .card-task { border-right: 10px solid #16a085; }
    
    .item-title { font-size: clamp(1.3rem, 3.5vw, 1.7rem); font-weight: 800; color: #1e272e; margin-bottom: 8px;}
    .item-desc { font-size: clamp(1rem, 2.8vw, 1.25rem); color: #485460; line-height: 1.5; margin-bottom: 12px;}
    
    /* מבנה לימודי מיוחד למרכיבי קוקטיילים */
    .ingredients-box {
        background: #f1f2f6;
        padding: 12px 18px;
        border-radius: 10px;
        font-size: clamp(1.05rem, 3vw, 1.3rem);
        color: #2f3542;
        font-weight: 600;
        line-height: 1.6;
        border-left: 4px solid #f39c12;
        margin-top: 10px;
    }
    
    .item-notes { font-size: clamp(0.95rem, 2.5vw, 1.15rem); color: #c23616; font-weight: 600; background: #ffebee; padding: 6px 12px; border-radius: 8px; display: inline-block; margin-top: 10px;}
    
    .tag { font-size: clamp(0.8rem, 2.2vw, 0.95rem); font-weight: 600; padding: 4px 10px; border-radius: 6px; display: inline-block; margin: 4px 0 4px 6px; }
    .t-veg { background: #e8f5e9; color: #2e7d32; }
    .t-gf { background: #fff8e1; color: #f57f17; }
    .t-preg { background: #e3f2fd; color: #1565c0; }
    .t-warn { background: #ffebee; color: #c62828; }

    /* התאמת טאבים */
    .stTabs [data-baseweb="tab"] { font-size: clamp(1rem, 3vw, 1.4rem) !important; font-weight: 600 !important; }
</style>
""", unsafe_allow_html=True)

if 'role' not in st.session_state:
    st.session_state.role = None

def set_role(role):
    st.session_state.role = role

# ---------------------------------------------------------
# עמוד שער יוקרתי ונקי לנייד
# ---------------------------------------------------------
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

# ---------------------------------------------------------
# מסך מלצרים
# ---------------------------------------------------------
elif st.session_state.role == "waiter":
    col1, col2 = st.columns([8, 2])
    with col1: st.markdown("<h2>🍽️ תפריט ומחלקות אוכל</h2>", unsafe_allow_html=True)
    with col2: st.button("איפוס ↩", on_click=set_role, args=(None,))
    
    # כפתורי סינון מהירים במובייל
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

# ---------------------------------------------------------
# מסך ברמנים - קוקטיילים וצ'קליסטים מלאים מ-SQL
# ---------------------------------------------------------
elif st.session_state.role == "bartender":
    col1, col2 = st.columns([8, 2])
    with col1: st.markdown("<h2>🍸 עמדת בר ומשימות</h2>", unsafe_allow_html=True)
    with col2: st.button("איפוס ↩", on_click=set_role, args=(None,))
    
    tab1, tab2, tab3 = st.tabs(["🍹 מתכוני קוקטיילים", "🌅 צ'קליסט משמרת", "📅 משימות יומיות"])
    
    with tab1:
        cocktails = fetch_data("SELECT * FROM cocktails")
        for c in cocktails:
            # הפיכת הסימן '|' לירידת שורה כדי שיהיה קל ללמוד בעין
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
        st.markdown("<h3>📋 נהלי פתיחה וסגירה מתוך ה-SQL</h3>", unsafe_allow_html=True)
        
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
