import re
import json

def parse_exam_questions(text_content):
    # Remove the "" noise and page headers
    clean_text = re.sub(r'\', '', text_content)
    clean_text = re.sub(r'--- PAGE \d+ ---', '', clean_text)
    
    # Split by "Question #" to separate items
    raw_questions = re.split(r'Question #\d+', clean_text)
    
    quiz_data = {
        "quizTitle": "AWS SAA-C03 Exam Practice",
        "quizSynopsis": "Practice questions generated from exam dump.",
        "questions": []
    }

    for raw_q in raw_questions:
        if not raw_q.strip(): continue
        
        # Extract Question Text (everything before the options)
        # We look for patterns like "A." to start the options
        match_options = re.search(r'(A\..*?)(Correct Answer:.*)', raw_q, re.DOTALL)
        
        if match_options:
            q_text_part = raw_q[:match_options.start()].strip()
            options_part = match_options.group(1).strip()
            correct_part = match_options.group(2).strip()
            
            # Extract options (A, B, C, D)
            options = []
            # Regex to find "A. text", "B. text" etc
            opt_matches = re.findall(r'([A-E]\.)(.*?)(?=[A-E]\.|$)', options_part + "\nZ.", re.DOTALL)
            
            for _, opt_text in opt_matches:
                options.append(opt_text.strip())
            
            # Extract Correct Answer
            correct_match = re.search(r'Correct Answer:\s*([A-E]+)', correct_part)
            correct_answer_indices = []
            if correct_match:
                ans_letters = list(correct_match.group(1))
                # Map 'A'->1, 'B'->2 for the quiz app format
                char_map = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5}
                correct_answer_indices = [char_map[char] for char in ans_letters if char in char_map]

            if options and correct_answer_indices:
                question_obj = {
                    "question": q_text_part,
                    "questionType": "text",
                    "answerSelectionType": "multiple" if len(correct_answer_indices) > 1 else "single",
                    "answers": options,
                    "correctAnswer": correct_answer_indices[0] if len(correct_answer_indices) == 1 else correct_answer_indices,
                    "messageForCorrectAnswer": "Correct!",
                    "messageForIncorrectAnswer": "Incorrect."
                }
                quiz_data["questions"].append(question_obj)

    return json.dumps(quiz_data, indent=2)

# Copy the text from your PDF file into a file named 'raw_questions.txt'
# Then run this script.
# with open('raw_questions.txt', 'r', encoding='utf-8') as f:
#     print(parse_exam_questions(f.read()))