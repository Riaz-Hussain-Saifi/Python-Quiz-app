import streamlit as st
import time
from datetime import timedelta, datetime
import random
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch
import io
import base64

# Custom CSS for beautiful design with animations
def apply_styles():
    st.markdown("""
    <style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideIn {
        from { transform: translateX(-20px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes pulseGlow {
        0% { box-shadow: 0 0 5px rgba(76, 175, 80, 0.5); }
        50% { box-shadow: 0 0 20px rgba(76, 175, 80, 0.8); }
        100% { box-shadow: 0 0 5px rgba(76, 175, 80, 0.5); }
    }
    
    .main {
        background: linear-gradient(135deg, #e0e7ff, #f0f2f6);
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        animation: fadeIn 0.8s ease-out;
        margin: 20px;
        color: black;
    }
    
    .stRadio > label {
        background-color: #dbeafe;
        padding: 12px;
        border-radius: 8px;
        margin: 8px 0;
        transition: all 0.3s ease;
        animation: slideIn 0.5s ease-out;
    }
    
    .stRadio > label:hover {
        background-color: #bfdbfe;
        transform: translateX(5px);
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .stButton > button {
        background: linear-gradient(to right, #4CAF50, #45a049);
        color: white;
        border-radius: 8px;
        padding: 12px 25px;
        border: none;
        font-weight: bold;
        transition: all 0.3s ease;
        animation: fadeIn 0.5s ease-out;
    }
    
    .stButton > button:hover {
        background: linear-gradient(to right, #45a049, #4CAF50);
        transform: scale(1.05);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        animation: pulseGlow 2s infinite;
    }
    
    .stSidebar {
        background: linear-gradient(to bottom, #c7d2fe, #e0e7ff);
        padding: 20px;
        border-radius: 10px;
        animation: slideIn 0.8s ease-out;
    }
    
    .timer {
        font-size: 26px;
        color: #dc2626;
        font-weight: bold;
        text-align: center;
        animation: pulseGlow 2s infinite;
    }
    
    .sidebar-text {
        font-size: 16px;
        color: #1e40af;
        font-family: 'Arial', sans-serif;
        margin: 10px 0;
    }
    
    .result-header {
        font-size: 24px;
        color: #1e3a8a;
        font-weight: bold;
        text-align: center;
        margin: 20px 0;
        animation: fadeIn 1s ease-out;
    }
    
    .certificate-container {
        text-align: center;
        margin: 20px 0;
        padding: 20px;
        border: 2px solid #4CAF50;
        border-radius: 10px;
        background: white;
        animation: fadeIn 1s ease-out;
    }
    
    .download-button {
        background: linear-gradient(to right, #2563eb, #1d4ed8);
        color: white !important; /* Ensure text is white */
        padding: 12px 25px;
        border-radius: 8px;
        text-decoration: none;
        display: inline-block;
        margin: 15px 0;
        transition: all 0.3s ease;
        font-weight: bold;
    }
    
    .download-button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        animation: pulseGlow 2s infinite;
    }
    
    h1 {
        color: #1e3a8a;
        text-align: center;
        font-family: 'Arial', sans-serif;
        animation: fadeIn 0.8s ease-out;
    }
    
    .question-container {
        background: white;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        animation: fadeIn 0.5s ease-out;
    }
    
    .progress-bar {
        height: 10px;
        background: #e0e7ff;
        border-radius: 5px;
        margin: 10px 0;
        overflow: hidden;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(to right, #4CAF50, #45a049);
        transition: width 0.3s ease;
    }
    </style>
    """, unsafe_allow_html=True)

def update_timer():
    if 'start_time' in st.session_state and st.session_state.timer_running:
        current_time = time.time()
        elapsed_time = current_time - st.session_state.start_time
        remaining_time = max(0, 10 * 60 - elapsed_time)
        st.session_state.remaining_time = remaining_time
        if remaining_time <= 0:
            st.session_state.timer_running = False
            st.session_state.current_question = 20

def generate_certificate(name, roll_number, slot, score, date_completed, time_taken):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(A4))
    width, height = landscape(A4)
    
    # Background with gradient effect
    c.setFillColorRGB(0.95, 0.95, 1)
    c.rect(0, 0, width, height, fill=True)
    
    # Decorative border
    c.setStrokeColorRGB(0.2, 0.5, 0.3)
    c.setLineWidth(3)
    c.rect(30, 30, width-60, height-60)
    
    # Add decorative corners
    corner_size = 40
    for x, y in [(30, 30), (width-30-corner_size, 30), 
                 (30, height-30-corner_size), (width-30-corner_size, height-30-corner_size)]:
        c.rect(x, y, corner_size, corner_size)
    
    # Title
    c.setFont("Helvetica-Bold", 40)
    c.setFillColorRGB(0.2, 0.3, 0.7)
    c.drawCentredString(width/2, height-100, "Certificate of Completion")
    
    # Decorative line under title
    c.setLineWidth(2)
    c.line(width/4, height-120, width*3/4, height-120)
    
    # Content
    c.setFont("Helvetica", 24)
    c.setFillColorRGB(0.2, 0.2, 0.2)
    c.drawCentredString(width/2, height-180, f"This is to certify that")
    
    # Name
    c.setFont("Helvetica-Bold", 32)
    c.setFillColorRGB(0.1, 0.3, 0.5)
    c.drawCentredString(width/2, height-230, name)
    
    # Roll Number
    c.setFont("Helvetica", 24)
    c.setFillColorRGB(0.2, 0.2, 0.2)
    c.drawCentredString(width/2, height-270, f"Roll Number: {roll_number}")
    
    # Slot
    c.drawCentredString(width/2, height-310, f"Slot: {slot}")
    
    # Course details
    c.drawCentredString(width/2, height-350, f"has successfully completed the")
    c.drawCentredString(width/2, height-390, "Python & Next.js 15 Assessment")
    
    # Score
    c.setFont("Helvetica-Bold", 24)
    c.setFillColorRGB(0.2, 0.5, 0.3)
    c.drawCentredString(width/2, height-440, f"with a score of {score}%")
    
    # Time Taken
    c.setFont("Helvetica", 20)
    c.setFillColorRGB(0.4, 0.4, 0.4)
    c.drawCentredString(width/2, height-490, f"Time Taken: {time_taken}")
    
    # Date
    c.drawCentredString(width/2, height-530, f"Completed on {date_completed}")
    
    # Developer and Senior Student Info
    c.setFont("Helvetica", 16)
    c.setFillColorRGB(0.2, 0.2, 0.2)
    c.drawCentredString(width/2, height-580, "Developed by Riaz Hussain, Senior Student of Quarter 2 at GIAIC")
    
    # Signatures
    c.setFont("Helvetica-Bold", 20)
    c.drawString(100, 100, "Instructor")
    c.line(70, 90, 200, 90)
    
    c.drawString(width-200, 100, "Date")
    c.line(width-230, 90, width-100, 90)
    
    # Add QR code placeholder
    c.rect(width-100, height-100, 70, 70)
    
    c.save()
    buffer.seek(0)
    return buffer

def get_certificate_download_link(pdf_bytes, filename):
    b64 = base64.b64encode(pdf_bytes.read()).decode()
    return f'<a href="data:application/pdf;base64,{b64}" download="{filename}" class="download-button">Download Certificate</a>'

def main():
    apply_styles()
    
    st.title("Python & Next.js Quiz Challenge")
    st.write(f"### Created by Riaz Hussain")
    
    # Quiz information with enhanced styling
    st.markdown("""
    <div class="main">
        <h3>Quiz Details</h3>
        <ul>
            <li>Total Questions: 20</li>
            <li>Time Limit: 10 Minutes</li>
            <li>Score: 5 Points per Question (Total 100)</li>
            <li>Topics: Python and Next.js 15</li>
            <li>Note: Questions are randomized!</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Session state initialization
    if 'user_details_submitted' not in st.session_state:
        st.session_state.user_details_submitted = False
    if 'questions' not in st.session_state:
        st.session_state.questions = []
    if 'timer_running' not in st.session_state:
        st.session_state.timer_running = False
    if 'remaining_time' not in st.session_state:
        st.session_state.remaining_time = 10 * 60
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'total_time' not in st.session_state:
        st.session_state.total_time = 0
    if 'correct_answers' not in st.session_state:
        st.session_state.correct_answers = 0

    # Quiz questions
    fixed_questions = [
        {"q": "What does Python's print() do?", "options": ["Input", "Output", "Loop", "Condition"], "correct": "Output"},
        {"q": "In Next.js 15, App Router is for?", "options": ["Styling", "Routing", "Database", "Auth"], "correct": "Routing"},
        {"q": "Python function keyword?", "options": ["def", "fun", "func", "define"], "correct": "def"},
        {"q": "Next.js static site method?", "options": ["getServerSideProps", "getStaticProps", "useEffect", "fetch"], "correct": "getStaticProps"},
        {"q": "Are Python lists mutable?", "options": ["Yes", "No", "Sometimes", "Never"], "correct": "Yes"},
        {"q": "Next.js pages folder?", "options": ["app", "pages", "src", "public"], "correct": "pages"},
        {"q": "Python range() purpose?", "options": ["Random", "Sequence", "String", "List"], "correct": "Sequence"},
        {"q": "Next.js 15 React version?", "options": ["16", "17", "18", "19"], "correct": "18"},
        {"q": "Immutable Python type?", "options": ["List", "Dict", "Tuple", "Set"], "correct": "Tuple"},
        {"q": "Next.js client-side hook?", "options": ["useEffect", "useServer", "useClient", "useFetch"], "correct": "useEffect"},
        {"q": "Python 'if' purpose?", "options": ["Looping", "Condition", "Function", "Class"], "correct": "Condition"},
        {"q": "Next.js global CSS file?", "options": ["global.css", "_app.js", "styles.css", "index.css"], "correct": "_app.js"},
        {"q": "Python len() returns?", "options": ["Length", "Sum", "Average", "Max"], "correct": "Length"},
        {"q": "Next.js 15 performance feature?", "options": ["Server Components", "Client Components", "Static", "All"], "correct": "All"},
        {"q": "Python 'for' loop purpose?", "options": ["Condition", "Iteration", "Function", "Error"], "correct": "Iteration"},
        {"q": "Next.js automatic feature?", "options": ["Code splitting", "Database", "Auth", "Testing"], "correct": "Code splitting"},
        {"q": "Python equality operator?", "options": ["=", "==", "===", "!="], "correct": "=="},
        {"q": "Next.js dynamic route syntax?", "options": ["[param]", "{param}", "<param>", "(param)"], "correct": "[param]"},
        {"q": "Python's None means?", "options": ["Zero", "Null", "Empty", "False"], "correct": "Null"},
        {"q": "Next.js 15 enhances what?", "options": ["Server-side", "Client-side", "Static", "None"], "correct": "Server-side"}
    ]

    # User Details Form
    if not st.session_state.user_details_submitted:
        with st.form(key='user_details'):
            st.markdown('<div class="question-container">', unsafe_allow_html=True)
            name = st.text_input("Enter Your Name", placeholder="Your Name Here")
            roll_number = st.text_input("Enter Your Roll Number", placeholder="Your Roll Number Here")
            slot = st.selectbox("Select Your Slot", ["Monday 9AM-12AM", "Monday 2PM-5PM", "Monday 7PM-10PM",
                                                    "Tuesday 9AM-12AM", "Tuesday 2PM-5PM", "Tuesday 7PM-10PM",
                                                    "Wednesday 9AM-12AM", "Wednesday 2PM-5PM", "Wednesday 7PM-10PM",
                                                    "Thursday 9AM-12AM", "Thursday 2PM-5PM", "Thursday 7PM-10PM",
                                                    "Friday 9AM-12AM", "Friday 2PM-5PM", "Friday 7PM-10PM",
                                                    "Saturday 9AM-12AM", "Saturday 2PM-5PM", "Saturday 7PM-10PM",
                                                    "Sunday 9AM-12AM", "Sunday 2PM-5PM", "Sunday 7PM-10PM"])
            ready = st.checkbox("I am ready to start the quiz!")
            submit_details = st.form_submit_button("Start Quiz")
            st.markdown('</div>', unsafe_allow_html=True)
            
            if submit_details and name and roll_number and slot and ready:
                st.session_state.user_details_submitted = True
                st.session_state.name = name
                st.session_state.roll_number = roll_number
                st.session_state.slot = slot
                st.session_state.start_time = time.time()
                st.session_state.current_question = 0
                st.session_state.user_answers = []
                st.session_state.timer_running = True
                st.session_state.score = 0
                st.session_state.total_time = 0
                st.session_state.correct_answers = 0
                st.session_state.questions = fixed_questions.copy()
                random.shuffle(st.session_state.questions)
                st.rerun()

    # Sidebar Content
    if st.session_state.get('user_details_submitted', False):
        st.sidebar.markdown('<div class="sidebar">', unsafe_allow_html=True)
        if st.session_state.timer_running:
            st.sidebar.markdown(f"<p class='sidebar-text'>Name: {st.session_state.name}</p>", unsafe_allow_html=True)
            st.sidebar.markdown(f"<p class='sidebar-text'>Roll Number: {st.session_state.roll_number}</p>", unsafe_allow_html=True)
            st.sidebar.markdown(f"<p class='sidebar-text'>Slot: {st.session_state.slot}</p>", unsafe_allow_html=True)
            update_timer()
            st.sidebar.markdown(f"<p class='timer'>Time Remaining: {timedelta(seconds=int(st.session_state.remaining_time))}</p>", unsafe_allow_html=True)
            st.sidebar.markdown(f"<p class='sidebar-text'>Questions Left: {20 - st.session_state.current_question}</p>", unsafe_allow_html=True)
            
            # Progress bar
            progress = (st.session_state.current_question / 20) * 100
            st.sidebar.markdown(f"""
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {progress}%;"></div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.sidebar.markdown("<p class='result-header'>Quiz Results</p>", unsafe_allow_html=True)
            st.sidebar.markdown(f"<p class='sidebar-text'>Name: {st.session_state.name}</p>", unsafe_allow_html=True)
            st.sidebar.markdown(f"<p class='sidebar-text'>Roll Number: {st.session_state.roll_number}</p>", unsafe_allow_html=True)
            st.sidebar.markdown(f"<p class='sidebar-text'>Slot: {st.session_state.slot}</p>", unsafe_allow_html=True)
            st.sidebar.markdown(f"<p class='sidebar-text'>Score: {st.session_state.score}/100</p>", unsafe_allow_html=True)
            st.sidebar.markdown(f"<p class='sidebar-text'>Correct Answers: {st.session_state.correct_answers}/20</p>", unsafe_allow_html=True) 
        st.sidebar.markdown('</div>', unsafe_allow_html=True)

    # Main Quiz Area
    if st.session_state.get('user_details_submitted', False):
        total_questions = 20
        points_per_question = 5

        # Show Question
        if st.session_state.current_question < total_questions and st.session_state.remaining_time > 0:
            q = st.session_state.questions[st.session_state.current_question]
            st.markdown('<div class="question-container">', unsafe_allow_html=True)
            st.write(f"### Question {st.session_state.current_question + 1}/{total_questions} (5 Points)")
            st.write(q["q"])
            
            with st.form(key=f'question_{st.session_state.current_question}'):
                answer = st.radio("Choose your answer:", q["options"], key=f"q{st.session_state.current_question}")
                submit_answer = st.form_submit_button("Next Question")
                
                if submit_answer:
                    st.session_state.user_answers.append(answer)
                    if answer == q["correct"]:
                        st.session_state.correct_answers += 1
                        st.session_state.score += points_per_question
                    st.session_state.current_question += 1
                    if st.session_state.current_question >= total_questions:
                        st.session_state.timer_running = False
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Show Results
        elif st.session_state.current_question >= total_questions or st.session_state.remaining_time <= 0:
            end_time = time.time()
            total_time = min(end_time - st.session_state.start_time, 10 * 60)
            st.session_state.total_time = total_time
            percentage = (st.session_state.score / 100) * 100

            st.markdown('<div class="result-container">', unsafe_allow_html=True)
            st.write(f"## 🎉 Quiz Completed, {st.session_state.name}!")
            
            # Results with animations
            st.markdown(f"""
                <div class="result-stats">
                    <p class='main-result'>Final Score: {st.session_state.score}/100 ({percentage:.1f}%)</p>
                    <p class='main-result'>Correct Answers: {st.session_state.correct_answers}/20</p>
                    <p class='main-result'>Time Taken: {timedelta(seconds=int(total_time))}</p>
                </div>
            """, unsafe_allow_html=True)

            # Generate and show certificate
            st.markdown("### 🏆 Your Certificate")
            st.markdown('<div class="certificate-container">', unsafe_allow_html=True)
            
            date_completed = datetime.now().strftime("%B %d, %Y")
            time_taken = str(timedelta(seconds=int(total_time)))
            pdf_buffer = generate_certificate(
                st.session_state.name,
                st.session_state.roll_number,
                st.session_state.slot,
                percentage,
                date_completed,
                time_taken
            )
            
            certificate_html = get_certificate_download_link(
                pdf_buffer,
                f"certificate_{st.session_state.name.replace(' ', '_')}.pdf"
            )
            st.markdown(certificate_html, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # Performance Feedback
            if percentage == 100:
                st.success(f"🌟 Perfect Score! Exceptional work, {st.session_state.name}!")
                st.balloons()
            elif percentage >= 80:
                st.success(f"🎉 Excellent Performance, {st.session_state.name}!")
            elif percentage >= 60:
                st.warning(f"👍 Good Effort, {st.session_state.name}!")
            else:
                st.error(f"Keep Learning, {st.session_state.name}! You'll do better next time.")

            # Show Wrong Answers
            if st.session_state.correct_answers < 20:
                with st.expander("📝 Review Your Answers"):
                    st.markdown('<div class="review-container">', unsafe_allow_html=True)
                    for i, (q, user_ans, correct_ans) in enumerate(zip(
                        st.session_state.questions,
                        st.session_state.user_answers,
                        [q["correct"] for q in st.session_state.questions]
                    )):
                        if user_ans != correct_ans:
                            st.markdown(f"""
                                <div class="wrong-answer">
                                    <p><strong>Question {i+1}:</strong> {q['q']}</p>
                                    <p style="color: #dc2626;">Your Answer: {user_ans}</p>
                                    <p style="color: #059669;">Correct Answer: {correct_ans}</p>
                                </div>
                            """, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.success("🎯 Perfect Score! You answered all questions correctly!")

            st.markdown('</div>', unsafe_allow_html=True)

        # Timer refresh
        if st.session_state.timer_running and st.session_state.current_question < total_questions:
            time.sleep(1)
            st.rerun()

if __name__ == "__main__":
    st.set_page_config(
        page_title="Enhanced Quiz by Riaz Hussain",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    main()