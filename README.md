# M-Simpler

## Description

M-Simpler is an innovative AI application designed to simplify the interpretation of medical documents, addressing the complex nature of medical terminology that often hinders effective communication in healthcare. By leveraging advanced AI capabilities, M-Simpler streamlines the comprehension of medical information for both professionals and patients, thus enhancing healthcare communication, empowering individuals, and facilitating medical research. This report explores the potential of M-Simpler to revolutionize medical document interpretation, highlighting its role in bridging communication gaps and advancing the accessibility of critical healthcare information. Additionally, it examines the challenges and considerations involved in integrating AI-driven solutions into healthcare practices, offering insights into the opportunities and obstacles in realizing the full potential of AI in healthcare communication.

## Usage
1. Access the application through your browser at https://healthcare-chatbot-vhzr.onrender.com(It may take upto 1 min to load the webpage for the first time run). Or the  
2. Register or log in to your account.
3. Interact with the chatbot by typing your message in the input field and  uploading an image and lastly pressing Enter or clicking the send button.
4. Logout when finished

## Getting Started

## Technologies Used
- Bootstrap 4 for styling
- Gemini Pro API key(LLM Model)
- PostgreSQL (Database)

### Dependencies
- Python==3.12.1
- Flask
- Pillow (Python Imaging Library)
- Gunicorn (WSGI HTTP Server for Python)
- Google GenerativeAI API
- Flask-SQLAlchemy
- psycopg2 (PostgreSQL adapter for Python)
- Python-dotenv (Python-dotenv reads key-value pairs from a .env file)


## Executing program
1. Install Dependencies:  
- Ensure you have Python installed on your system.
- Install the required dependencies by running:
```
pip install -r requirements.txt
```

2. Set Up Environment Variables
- Create a .env file in the root directory of the project.
- Add your own Google Gemini Pro API key to the .env file:
```
GOOGLE_API_KEY=your_api_key_here
```
3. Make sure PostgreSQL is installed and running on your system.
Create a database named user_e3f9 (or modify the SQLALCHEMY_DATABASE_URI in app.py according to your database configuration).
4. Run the Application
- Start the Flask server by running in the terminal for development side
```
python app.py
```
5. Access the Application:

- Open your web browser and navigate to http://localhost:8000.
- Register or log in to your account to interact with the chatbot.


## Authors

Rashik Mahmud Orchi(rs868141@dal.ca)



## Acknowledgments

The following code snippets were used as reference to generate our project. 


* Krisnaik06[github](https://github.com/krishnaik06/End-To-End-Gemini-Project/blob/main/vision.py)- to use the api key and get response from the the inputs

```
import google.generativeai as genai


os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,image):
    model = genai.GenerativeModel('gemini-pro-vision')
    if input!="":
       response = model.generate_content([input,image])
    else:
       response = model.generate_content(image)
    return response.text


```
