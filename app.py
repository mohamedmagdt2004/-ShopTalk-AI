# import streamlit as st
# import pandas as pd
# import plotly.express as px

# from sql_agent import generate_sql
# from db import run_query
# from analyzer_agent import generate_insight
# from cache import save_cache, get_cache

# # ================= PAGE CONFIG =================

# st.set_page_config(
#     page_title="ShopTalk AI",
#     page_icon="🛒",
#     layout="wide"
# )

# st.title("🛒 ShopTalk AI - Multi Agent System")

# # ================= SESSION =================

# # بدل المتغيرات الفردية، هنعمل ليستة نحفظ فيها كل المحادثات
# if "history" not in st.session_state:
#     st.session_state.history = []


# # ================= USER INPUT =================

# question = st.chat_input(
#     "Ask anything about your data..."
# )

# # ================= NEW QUESTION =================

# if question:

#     # ===== CACHE =====
#     cached_result = get_cache(question)

#     if cached_result is not None:
#         df = cached_result
#         sql = "Loaded From Cache"
#     else:
#         sql = generate_sql(question)
#         df = run_query(sql)
#         save_cache(question, df)

#     # ===== INSIGHT =====
#     insight = generate_insight(df)

#     # ===== SAVE TO SESSION HISTORY =====
#     # بنضيف السؤال وإجابته كقاموس (Dictionary) في الليستة
#     st.session_state.history.append({
#         "question": question,
#         "sql": sql,
#         "df": df,
#         "insight": insight
#     })


# # ================= DISPLAY HISTORY =================

# # هنعمل Loop عشان نعرض كل الأسئلة والإجابات اللي متسجلة
# for i, chat in enumerate(st.session_state.history):
    
#     # عرض سؤال المستخدم
#     with st.chat_message("user"):
#         st.write(chat["question"])

#     # عرض إجابة السيستم
#     with st.chat_message("assistant"):
        
#         df = chat["df"]
        
#         if df is not None:
#             # ===== SQL =====
#             st.subheader("Generated SQL")
#             st.code(
#                 chat["sql"],
#                 language="sql"
#             )

#             # ===== RESULT =====
#             st.subheader("Result")
#             st.dataframe(
#                 df,
#                 use_container_width=True
#             )

#             # ===== INSIGHT =====
#             st.subheader("AI Insight")
#             st.write(
#                 chat["insight"]
#             )

#             # ===== CHART =====
#             numeric_cols = df.select_dtypes(
#                 include="number"
#             ).columns

#             if len(numeric_cols) > 0:
#                 # ضفنا key هنا واعتمدنا على رقم الاندكس (i) عشان ميبقاش فيه تكرار
#                 chart_type = st.selectbox(
#                     "Choose Chart Type",
#                     [
#                         "bar",
#                         "line",
#                         "pie",
#                         "scatter",
#                         "histogram"
#                     ],
#                     key=f"chart_type_{i}" 
#                 )

#                 x_col = df.columns[0]
#                 y_col = numeric_cols[0]

#                 # ===== BAR =====
#                 if chart_type == "bar":
#                     fig = px.bar(
#                         df,
#                         x=x_col,
#                         y=y_col
#                     )

#                 # ===== LINE =====
#                 elif chart_type == "line":
#                     fig = px.line(
#                         df,
#                         x=x_col,
#                         y=y_col,
#                         markers=True
#                     )

#                 # ===== PIE =====
#                 elif chart_type == "pie":
#                     fig = px.pie(
#                         df,
#                         names=x_col,
#                         values=y_col
#                     )

#                 # ===== SCATTER =====
#                 elif chart_type == "scatter":
#                     fig = px.scatter(
#                         df,
#                         x=x_col,
#                         y=y_col
#                     )

#                 # ===== HISTOGRAM =====
#                 # ===== HISTOGRAM =====

#         elif chart_type == "histogram":

#             fig = px.histogram(
#                 df,
#                 x=x_col
#             )

#         # التعديل هيكون هنا 👇
#         st.plotly_chart(
#             fig,
#             use_container_width=True,
#             key=f"plotly_chart_{i}"  # ضفنا السطر ده عشان ندي لكل شارت ID مختلف
#         )



























import streamlit as st
import pandas as pd
import plotly.express as px

from sql_agent import generate_sql
from db import run_query
from analyzer_agent import generate_insight
from cache import save_cache, get_cache
from audit import log_event  # 👈 (التعديل الأول) استدعينا دالة المراقبة هنا

# ================= PAGE CONFIG =================

st.set_page_config(
    page_title="ShopTalk AI",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 ShopTalk AI - Multi Agent System")

# ================= SESSION =================

if "history" not in st.session_state:
    st.session_state.history = []

# ================= USER INPUT =================

question = st.chat_input(
    "Ask anything about your data..."
)

# ================= NEW QUESTION =================

if question:

    # ===== CACHE =====
    cached_result = get_cache(question)

    if cached_result is not None:
        df = cached_result
        sql = "Loaded From Cache"
    else:
        sql = generate_sql(question)
        df = run_query(sql)
        save_cache(question, df)

    # ===== INSIGHT =====
    insight = generate_insight(df)

    # ===== SAVE TO SESSION HISTORY =====
    st.session_state.history.append({
        "question": question,
        "sql": sql,
        "df": df,
        "insight": insight
    })
    
    # ===== AUDITING SYSTEM =====
    # 👈 (التعديل التاني) تسجيل المحادثة في الملف بعد ما تخلص
    log_event("SUCCESS", question, sql, insight) 


# ================= DISPLAY HISTORY =================

for i, chat in enumerate(st.session_state.history):
    
    # عرض سؤال المستخدم
    with st.chat_message("user"):
        st.write(chat["question"])

    # عرض إجابة السيستم
    with st.chat_message("assistant"):
        
        df = chat["df"]
        
        if df is not None:
            # ===== SQL =====
            st.subheader("Generated SQL")
            st.code(
                chat["sql"],
                language="sql"
            )

            # ===== RESULT =====
            st.subheader("Result")
            st.dataframe(
                df,
                use_container_width=True
            )

            # ===== INSIGHT =====
            st.subheader("AI Insight")
            st.write(
                chat["insight"]
            )

            # ===== CHART =====
            numeric_cols = df.select_dtypes(
                include="number"
            ).columns

            if len(numeric_cols) > 0:
                chart_type = st.selectbox(
                    "Choose Chart Type",
                    [
                        "bar",
                        "line",
                        "pie",
                        "scatter",
                        "histogram"
                    ],
                    key=f"chart_type_{i}" 
                )

                x_col = df.columns[0]
                y_col = numeric_cols[0]

                # ===== BAR =====
                if chart_type == "bar":
                    fig = px.bar(
                        df,
                        x=x_col,
                        y=y_col
                    )

                # ===== LINE =====
                elif chart_type == "line":
                    fig = px.line(
                        df,
                        x=x_col,
                        y=y_col,
                        markers=True
                    )

                # ===== PIE =====
                elif chart_type == "pie":
                    fig = px.pie(
                        df,
                        names=x_col,
                        values=y_col
                    )

                # ===== SCATTER =====
                elif chart_type == "scatter":
                    fig = px.scatter(
                        df,
                        x=x_col,
                        y=y_col
                    )

                # ===== HISTOGRAM =====
                elif chart_type == "histogram":
                    fig = px.histogram(
                        df,
                        x=x_col
                    )

                # 👈 (التعديل التالت) ظبطنا المسافات هنا عشان الكود ميضربش إيرور
                st.plotly_chart(
                    fig,
                    use_container_width=True,
                    key=f"plotly_chart_{i}"  
                )