import streamlit as st
import pandas as pd

from fpdf import FPDF

def clean_text(text:str) -> str:
    # find and replace the unicode character for an apostrophe with a regular apostrophe
    text = text.replace('\u2019', "'")
    # do this for any other special characters that you find
    text = text.replace('\u2014', '-')
    text = text.replace('\u201c', '"')
    text = text.replace('\u201d', '"')
    # remove uneccessary whitespace
    text = ' '.join(text.split())
    return text

class CustomPDF(FPDF):

    def __init__(self, title = ''):
        super().__init__()
        self.title = title

    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, f'{self.title}', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(10)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()



def load_questions() -> pd.DataFrame:
    kumite_questions = pd.read_csv("data/kumite_questions.csv")
    kata_questions = pd.read_csv("data/kata_questions.csv")
    return kumite_questions, kata_questions

def page_config():
    st.set_page_config(
        page_title="Judge/Referee Test Generator",
        page_icon="🥋"
        )
    st.title("Judge/Referee Test Generator")
    st.write("Welcome to the Judge/Referee Test Generator. This tool will help you generate a test for your prospective judges and referees. Please select the number of questions and the type of questions you would like to include in the test.")

def test_config():
    with st.form(key="test_config"):
        st.write("Select the number of questions for the test:")
        num_questions = st.number_input("Number of Questions", min_value=1, max_value=50, value=10)
        
        st.write("Select whether this is a Kumite or Kata test:")
        question_type = st.selectbox("Question Type", ["Kumite", "Kata"])
        
        submit_button = st.form_submit_button(label="Generate Test")
        
        return num_questions, question_type, submit_button
    
def generate_test_response(num_questions, question_type):
    with st.spinner("Generating Test..."):
        with st.expander("Test Questions preview", expanded=False):
            kumite_questions, kata_questions = load_questions()
            if question_type == "Kumite":
                questions = kumite_questions
            else:
                questions = kata_questions
            test = questions.sample(num_questions)
            count = 1
            for index, row in test.iterrows():
                st.markdown(f"**Question {count}**: {row['question']}")
                # these are true or false questions
                # so we can display a radio button for the answer
                st.markdown(' [  ] True   [  ] False')
                count += 1
        # generate the pdf
        pdf = generate_test_pdf(test)
        pdf_file = pdf.output(dest='S').encode('latin1')
        st.download_button("Download Test PDF", pdf_file, file_name=f"{question_type}_test.pdf", mime="application/pdf", key="download_pdf")

def generate_test_pdf(random_questions: pd.DataFrame):
    pdf = CustomPDF('Kumite Questions')
    pdf.add_page()

    pdf.set_font('Arial', 'B', 16)
    pdf.chapter_title('True/False Questions')

    pdf.set_font('Arial', '', 12)
    question_count = 1
    for index, row in random_questions.iterrows():
        clean_question = clean_text(row['question'])
        line = f'{question_count}. {clean_question}'
        pdf.multi_cell(0, 10, f'{line}', 0, 1)
        pdf.cell(0, 10, ' [  ] True   [  ] False', 0, 1)
        pdf.ln(5)
        question_count += 1

    st.write("PDF generated successfully!")
    return pdf

def main():
    page_config()
    num_questions, question_type, submit_button = test_config()
    if submit_button:
        generate_test_response(num_questions, question_type)

if __name__ == "__main__":
    main()
