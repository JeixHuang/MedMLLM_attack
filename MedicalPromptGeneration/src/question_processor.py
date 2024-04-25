import os
def process_questions(model, image, questions_file):
    answers = []
    questions_path = os.path.join(os.path.dirname(__file__), '..', questions_file)
    with open(questions_path, 'r') as file:
        questions = file.readlines()
    
    for question in questions:
        question = question.strip()
        if question:
            answer = model.answer_question(image, question)
            answers.append({"question": question, "answer": answer})
    return answers
