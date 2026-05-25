# from datetime import datetime

# def log_event(event_type, message):

#     with open("audit_log.txt", "a", encoding="utf-8") as file:

#         time = datetime.now().strftime(
#             "%Y-%m-%d %H:%M:%S"
#         )

#         file.write(
#             f"[{time}] [{event_type}] {message}\n"
#         )





from datetime import datetime

def log_event(event_type, question, sql_query, insight=""):
    # بنفتح الملف في وضع الإضافة "a" عشان منمسحش القديم
    with open("audit_log.txt", "a", encoding="utf-8") as file:
        
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # بنجهز الرسالة بشكل منظم عشان تكون سهلة في القراءة
        log_message = (
            f"[{time}] [{event_type}]\n"
            f"Question: {question}\n"
            f"SQL: {sql_query}\n"
            f"Insight: {insight}\n"
            f"--------------------------------------------------\n"
        )
        
        # بنكتب الرسالة في الملف
        file.write(log_message)
        