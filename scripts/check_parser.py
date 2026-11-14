import sys
sys.path.insert(0, '.')
from app.services.md_quiz_parser import DirectMDQuizParser

with open('dist/Olympic_Portable/data/uploads/DOC_d7d53406_annamluccu.md', encoding='utf-8') as f:
    content = f.read()

questions, topics = DirectMDQuizParser.parse_document(content, 'D1', 'Title')
print('Total parsed questions:', len(questions))

has_cau = []
for q in questions:
    for opt in q.options:
        if 'câu ' in opt.lower() or 'phần ' in opt.lower():
            has_cau.append((q.question_id, opt))

print(f"Options containing 'câu' or 'phần': {len(has_cau)}")
for item in has_cau:
    print('  ', item)
