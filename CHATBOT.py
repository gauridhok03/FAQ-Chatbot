from flask import Flask, request, jsonify, render_template
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# ---------------- FAQ DATA ----------------

FAQS = [

    # ---------------- AI & TECHNOLOGY ----------------

    {
        "question": "What is Artificial Intelligence?",
        "answer": "Artificial Intelligence, or AI, is technology that allows computers to perform tasks that normally require human intelligence, such as learning, understanding language, and making decisions."
    },

    {
        "question": "What does AI stand for?",
        "answer": "AI stands for Artificial Intelligence."
    },

    {
        "question": "What is Machine Learning?",
        "answer": "Machine Learning is a part of AI where computers learn patterns from data and improve their performance without being explicitly programmed for every situation."
    },

    {
        "question": "What is Deep Learning?",
        "answer": "Deep Learning is a type of Machine Learning that uses neural networks with multiple layers to learn complex patterns from data."
    },

    {
        "question": "What is Natural Language Processing?",
        "answer": "Natural Language Processing, or NLP, helps computers understand, process, and respond to human language."
    },

    {
        "question": "What is a chatbot?",
        "answer": "A chatbot is a computer program that communicates with people through text or voice and provides useful responses."
    },

    {
        "question": "What is technology?",
        "answer": "Technology is the use of scientific knowledge, tools, and techniques to solve problems and make our lives easier."
    },

    {
        "question": "What is the difference between AI and Machine Learning?",
        "answer": "AI is the broader concept of making machines intelligent, while Machine Learning is one method used to achieve AI by allowing computers to learn from data."
    },


    # ---------------- PROGRAMMING ----------------

    {
        "question": "What is Python?",
        "answer": "Python is a popular and beginner-friendly programming language used for web development, automation, data science, Artificial Intelligence, and many other applications."
    },

    {
        "question": "Why should I learn Python?",
        "answer": "Python has simple syntax, is easy to learn, and is widely used in AI, Machine Learning, automation, web development, and data science."
    },

    {
        "question": "What is programming?",
        "answer": "Programming is the process of writing instructions that tell a computer how to perform a task."
    },

    {
        "question": "How can I learn programming?",
        "answer": "Start with one programming language, learn the basics, practice simple problems, and build small projects. Consistent practice is more important than trying to learn everything at once."
    },

    {
        "question": "What is HTML?",
        "answer": "HTML stands for HyperText Markup Language. It is used to create the structure of web pages."
    },

    {
        "question": "What is CSS?",
        "answer": "CSS stands for Cascading Style Sheets. It is used to style and design web pages, including colors, layouts, fonts, and spacing."
    },

    {
        "question": "What is JavaScript?",
        "answer": "JavaScript is a programming language commonly used to make websites interactive and dynamic."
    },

    {
        "question": "What is Flask?",
        "answer": "Flask is a lightweight Python web framework used to create web applications and connect Python code with web pages."
    },


    # ---------------- STUDY ----------------

    {
        "question": "How can I study better?",
        "answer": "Create a simple study schedule, focus on one topic at a time, practice regularly, and revise what you learn."
    },

    {
        "question": "Give me a study tip",
        "answer": "Try studying in focused sessions, keep your phone away, understand concepts instead of only memorizing them, and revise regularly."
    },

    {
        "question": "How can I concentrate while studying?",
        "answer": "Remove distractions, keep your phone away, choose one topic at a time, and study in short focused sessions with small breaks."
    },

    {
        "question": "How can I avoid distractions?",
        "answer": "Put your phone on silent, close unnecessary tabs, keep your study area clean, and set a small goal for each study session."
    },

    {
        "question": "How can I prepare for exams?",
        "answer": "Start early, make a realistic timetable, understand important concepts, practice questions, and revise regularly."
    },

    {
        "question": "What should I do if I don't understand a topic?",
        "answer": "Don't panic. Break the topic into smaller parts, find a simple explanation, practice examples, and ask for help if needed."
    },

    {
        "question": "How can I remember what I study?",
        "answer": "Use active recall, practice questions, make short notes, and revise the topic multiple times instead of reading it only once."
    },


    # ---------------- MOTIVATION ----------------

    {
        "question": "Motivate me",
        "answer": "You can do this! 🌟 You don't have to be perfect. Just keep moving forward one small step at a time. Your future self will thank you for not giving up."
    },

    {
        "question": "I need motivation",
        "answer": "Remember: small progress is still progress. 💪 You don't need to finish everything today. Just start with one small task and keep going."
    },

    {
        "question": "I feel like giving up",
        "answer": "Take a breath and give yourself a moment. A difficult day doesn't mean you are failing. Rest if you need to, then try again. You are stronger than you think. ❤️"
    },

    {
        "question": "Tell me something motivating",
        "answer": "Don't compare your beginning with someone else's middle. Keep learning, keep improving, and trust your own journey. 🌱"
    },

    {
        "question": "Can you encourage me?",
        "answer": "Of course! 😊 Believe in yourself and focus on the next step instead of worrying about the entire journey. You are doing better than you think."
    },

    {
        "question": "What should I do when I fail?",
        "answer": "Learn from what went wrong, make a small improvement, and try again. Failure is a part of learning, not the end of the journey."
    },


    # ---------------- GREETINGS ----------------

    {
        "question": "Hello",
        "answer": "Hello! 👋 Nice to meet you. How can I help you today?"
    },

    {
        "question": "Hi",
        "answer": "Hi! 😊 What would you like to ask me?"
    },

    {
        "question": "Hey",
        "answer": "Hey! 👋 I'm ready to chat. Ask me anything from my FAQ topics."
    },

    {
        "question": "Good morning",
        "answer": "Good morning! ☀️ I hope you have a great day. What can I help you with?"
    },

    {
        "question": "Good afternoon",
        "answer": "Good afternoon! 😊 What would you like to know?"
    },

    {
        "question": "Good evening",
        "answer": "Good evening! 🌆 How can I help you?"
    },

    {
        "question": "How are you?",
        "answer": "I'm doing great! 🤖 Thanks for asking. How can I help you?"
    },

    {
        "question": "What can you do?",
        "answer": "I can answer questions about AI, Machine Learning, programming, studies, motivation, and a few fun questions too!"
    },


    # ---------------- JOKES ----------------

    {
        "question": "Tell me a joke",
        "answer": "Why do programmers prefer dark mode? Because light attracts bugs! 😂"
    },

    {
        "question": "Tell me another joke",
        "answer": "Why did the computer go to the doctor? Because it had a virus! 😂💻"
    },

    {
        "question": "Make me laugh",
        "answer": "Why was the math book sad? Because it had too many problems! 😂📚"
    },

    {
        "question": "Do you know any jokes?",
        "answer": "Yes! Why did the programmer quit his job? Because he didn't get arrays! 😄"
    },

    {
        "question": "Give me a programming joke",
        "answer": "There are only 10 kinds of people in the world: those who understand binary and those who don't. 😂"
    },

    {
        "question": "Tell me something funny",
        "answer": "I told my computer I needed a break... and now it won't stop sending me vacation advertisements! 😂"
    },


    # ---------------- GENERAL FUN ----------------

    {
        "question": "What is your name?",
        "answer": "I'm your FAQ Chatbot! 🤖 You can call me your study and technology buddy."
    },

    {
        "question": "Who are you?",
        "answer": "I'm a simple FAQ chatbot created using Python, Flask, TF-IDF, and cosine similarity."
    },

    {
        "question": "Are you a human?",
        "answer": "Nope! 🤖 I'm a chatbot. I use programmed logic and text similarity to find the best answer to your question."
    },

    {
        "question": "Do you like programming?",
        "answer": "I don't have feelings, but programming is definitely one of my favorite things to talk about! 💻"
    },

    {
        "question": "Do you like AI?",
        "answer": "AI is a fascinating field! 🤖 It can help computers learn, understand information, and solve many different problems."
    },

    {
        "question": "What is your favorite programming language?",
        "answer": "Python is a great choice for beginners and is especially popular for AI and Machine Learning! 🐍"
    },

    {
        "question": "Are you smart?",
        "answer": "I'm good at finding answers from the information I've been given, but I'm definitely still learning! 🤖"
    },

    {
        "question": "Thank you",
        "answer": "You're welcome! 😊 I'm always happy to help."
    },

    {
        "question": "Thanks",
        "answer": "You're welcome! 🌟 Good luck with your studies and projects!"
    },

    {
        "question": "Bye",
        "answer": "Goodbye! 👋 Keep learning and keep smiling. See you next time!"
    },


    # ---------------- FUN QUESTIONS ----------------

    {
        "question": "What is the meaning of life?",
        "answer": "That's a big question! 😄 Maybe it's about learning, growing, enjoying the little things, and making meaningful memories."
    },

    {
        "question": "What should I do when I'm bored?",
        "answer": "Try learning something new, listening to music, taking a walk, working on a small project, or simply taking a relaxing break."
    },

    {
        "question": "Give me a fun fact",
        "answer": "Fun fact: Honey never spoils when stored properly. Archaeologists have even found ancient honey that was still preserved! 🍯"
    },

    {
        "question": "Tell me a fun fact about computers",
        "answer": "The first computer mouse was made of wood! 🖱️ It was invented in the 1960s."
    },

    {
        "question": "Give me a random fact",
        "answer": "Here's one: Octopuses have three hearts! 🐙"
    }

]


# ---------------- TEXT PROCESSING ----------------

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text


# Prepare FAQ questions
questions = [clean_text(faq["question"]) for faq in FAQS]

# Create TF-IDF model
vectorizer = TfidfVectorizer()
faq_vectors = vectorizer.fit_transform(questions)


# ---------------- CHATBOT ----------------

def get_answer(user_question):

    if not user_question.strip():
        return {
            "answer": "Please type a question.",
            "matched_question": None,
            "score": 0
        }

    cleaned_question = clean_text(user_question)

    user_vector = vectorizer.transform([cleaned_question])

    similarity = cosine_similarity(
        user_vector,
        faq_vectors
    )

    best_index = similarity.argmax()
    best_score = similarity[0][best_index]

    # Minimum similarity required
    if best_score < 0.20:
        return {
            "answer": "Sorry, I don't have an answer for that question. Please try asking something related to our FAQ topics.",
            "matched_question": None,
            "score": float(best_score)
        }

    return {
        "answer": FAQS[best_index]["answer"],
        "matched_question": FAQS[best_index]["question"],
        "score": float(best_score)
    }


# ---------------- WEB ROUTES ----------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    user_question = data.get("question", "")

    result = get_answer(user_question)

    return jsonify(result)


# ---------------- RUN APPLICATION ----------------

if __name__ == "__main__":
    app.run(debug=True)