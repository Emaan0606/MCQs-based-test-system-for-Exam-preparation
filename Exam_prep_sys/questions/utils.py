import spacy
from random import sample, shuffle

nlp = spacy.load("en_core_web_sm")

def generate_mcq_questions(paragraph, num_questions=5):
    doc = nlp(paragraph)
    sentences = list(doc.sents)  # Break paragraph into individual sentences
    questions = []

    for sentence in sentences:
        sent_doc = nlp(sentence.text)
        nouns = [token.text for token in sent_doc if token.pos_ == "NOUN"]
        if not nouns:
            continue

        answer = nouns[0]  # Take the first noun
        question_text = sentence.text.replace(answer, "_____")
        
        # Get distractors from other nouns in paragraph (excluding answer)
        all_nouns = list(set([token.text for token in doc if token.pos_ == "NOUN" and token.text != answer]))
        distractors = sample(all_nouns, min(3, len(all_nouns)))
        options = distractors + [answer]
        shuffle(options)

        questions.append({
            "question": question_text,
            "answer": answer,
            "options": options
        })

        if len(questions) >= num_questions:
            break
        
    return questions
