from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

llm = ChatGroq(
    api_key="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",
    model="llama-3.3-70b-versatile"
)

# ضفنا جزء القواعد (CRITICAL RULES) هنا عشان الموديل يفهم المشكلة
template = """
You are an expert SQL Server developer.

Table Name:
retail_orders

Columns:
Order_Id,
Order_Date,
Ship_Mode,
Segment,
Country,
City,
State,
Postal_Code,
Region,
Category,
Sub_Category,
Product_Id,
cost_price,
List_Price,
Quantity,
Discount_Percent

CRITICAL RULES TO AVOID ARITHMETIC OVERFLOW:
1. The columns List_Price, Quantity, cost_price, and Discount_Percent are stored as smallint.
2. You MUST ALWAYS explicitly CAST these columns to FLOAT before performing ANY multiplication, division, subtraction, or aggregation (like SUM).
3. Example: NEVER write `SUM(List_Price * Quantity)`. ALWAYS write `SUM(CAST(List_Price AS FLOAT) * CAST(Quantity AS FLOAT))`.
4. Always divide percentages by 100.0 (not 100) to avoid integer division.

Question:
{question}

Return ONLY SQL query.
"""

prompt = ChatPromptTemplate.from_template(template)

chain = prompt | llm

def generate_sql(question):

    sql = chain.invoke({
        "question": question
    }).content

    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")
    sql = sql.strip()

    return sql