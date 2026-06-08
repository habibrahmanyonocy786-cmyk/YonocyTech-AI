"""
Sample Google Sheets data display module.
In production, replace with actual Google Sheets API integration.
"""
import streamlit as st


SAMPLE_DATA = {
    "products": {
        "name": "📋 محصولات / Products",
        "columns": ["نام / Name", "قیمت / Price", "دسته / Category", "موجودی / Stock"],
        "rows": [
            ["لپ‌تاپ دل XPS 15", "$1,299", "الکترونیک", "۴۲"],
            ["هدفون بلوتوث", "$79", "الکترونیک", "۱۵۶"],
            ["صندلی اداری", "$349", "مبلمان", "۲۸"],
            ["مانیتور ۴K", "$599", "الکترونیک", "۶۳"],
            ["کیبورد مکانیکی", "$129", "لوازم جانبی", "۸۹"],
            ["ماوس بی‌سیم", "$49", "لوازم جانبی", "۲۰۱"],
        ],
        "image_column": None,
        "image_urls": {},
    },
    "users": {
        "name": "👥 کاربران / Users",
        "columns": ["نام / Name", "ایمیل / Email", "نقش / Role", "وضعیت / Status"],
        "rows": [
            ["Habibur Rahman", "habib@example.com", "ادمین", "✅ فعال"],
            ["Sara Ahmadi", "sara@example.com", "کاربر", "✅ فعال"],
            ["Mohammad Reza", "m.reza@example.com", "کاربر", "❌ غیرفعال"],
            ["Zahra Hosseini", "z.hosseini@example.com", "کاربر ویژه", "✅ فعال"],
            ["Ali Karimi", "ali@example.com", "کاربر", "✅ فعال"],
        ],
        "image_column": None,
        "image_urls": {},
    },
    "analytics": {
        "name": "📈 آمار ماهانه / Monthly Analytics",
        "columns": ["ماه / Month", "فروش / Sales", "بازدید / Visitors", "رشد / Growth"],
        "rows": [
            ["فروردین", "$12,400", "۴,۲۰۰", "+۸%"],
            ["اردیبهشت", "$14,100", "۵,۱۰۰", "+۱۴%"],
            ["خرداد", "$13,800", "۴,۹۰۰", "-۲%"],
            ["تیر", "$16,200", "۵,۸۰۰", "+۱۷%"],
            ["مرداد", "$18,500", "۶,۴۰۰", "+۱۴%"],
            ["شهریور", "$21,300", "۷,۲۰۰", "+۱۵%"],
        ],
        "image_column": None,
        "image_urls": {},
    },
}


def render_sheets_demo():
    from i18n.translator import Translator
    t = Translator()

    tabs = st.tabs([s["name"] for s in SAMPLE_DATA.values()])

    for idx, (key, sheet) in enumerate(SAMPLE_DATA.items()):
        with tabs[idx]:
            col_count = len(sheet["columns"])
            cols = st.columns([1] * col_count)
            for ci, col_name in enumerate(sheet["columns"]):
                cols[ci].markdown(
                    f"**{col_name}**",
                )

            for row in sheet["rows"]:
                cols = st.columns([1] * col_count)
                for ci, cell in enumerate(row):
                    cols[ci].write(cell)

            st.caption(f"📊 {len(sheet['rows'])} رکورد / records  ·  {col_count} ستون / columns")
