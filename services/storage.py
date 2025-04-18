import os
import pandas as pd

EXCEL_FILE = "knowledge_base.xlsx"

# Глобальные переменные базы
knowledge_base = {}
attachments_map = {}
question_id_map = {}
reverse_id_map = {}
id_counter = 0

def load_knowledge_from_excel(filepath: str):
    df = pd.read_excel(filepath)
    kb = {}
    am = {}
    for _, row in df.iterrows():
        section = str(row["Раздел"]).strip()
        question = str(row["Вопрос"]).strip()
        answer = str(row["Ответ"]).strip()
        file = str(row["Файл"]).strip() if pd.notna(row["Файл"]) and row["Файл"] else None
        if section not in kb:
            kb[section] = []
        kb[section].append({"Question": question, "answer": answer})
        if file:
            am[question] = f"attachments/{file}"
    return kb, am

def save_knowledge_to_excel():
    rows = []
    for section, qas in knowledge_base.items():
        for qa in qas:
            question = qa["Question"]
            answer = qa["answer"]
            file = ""
            if question in attachments_map:
                file = os.path.basename(attachments_map[question])
            rows.append({"Раздел": section, "Вопрос": question, "Ответ": answer, "Файл": file})
    df = pd.DataFrame(rows)
    df.to_excel(EXCEL_FILE, index=False)

def rebuild_question_maps():
    global question_id_map, reverse_id_map, id_counter
    question_id_map = {}
    reverse_id_map = {}
    id_counter = 0
    for section, qas in knowledge_base.items():
        for qa in qas:
            qid = f"q{id_counter}"
            question_id_map[qid] = {
                "section": section,
                "question": qa["Question"],
                "answer": qa["answer"]
            }
            reverse_id_map[qa["Question"]] = qid
            id_counter += 1

# Загрузка при старте
knowledge_base, attachments_map = load_knowledge_from_excel(EXCEL_FILE)
rebuild_question_maps()
