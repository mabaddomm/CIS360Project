# CIS360Project

# 📚 Research AI Agent

This project is an AI-powered agent that answers research queries using OpenAI and stores/retrieves data from MongoDB.

---

## 🚀 Getting Started

Follow these steps to set up the project locally.

---

## 🛠️ 1. Clone the Repository

## 2. In .env use your own open-ai api.

## 3. Set up virtual environment by running the linux command:
         # python3 -m venv venv
         # source venv/bin/activate
## 4. Install the dependencies by the command:
        # pip install -r requirements.txt

## 5. Set Up MongoDB Compass (Local Database):
    Step 1: Install MongoDB

    Download MongoDB Community Server:
    https://www.mongodb.com/try/download/community

    Step 2: Install MongoDB Compass

    Download MongoDB Compass:
    https://www.mongodb.com/try/download/compass

## 6. Start MongoDB server:
        # mongod
## 7. To convert our xlx files into mongodb database:
     step 1: download the excel_reader.py file and save the xl files in the same derectory
     step 2: run this file into your terminal as follows:
     # python3 excel_reader.py xlx_file_name

Then database with three collection will be created locally in your Compass

## 8. Run the applicaion by opening two terminals:
    
    # backend: cd backend
                python3 run.py

    # Frontend:
                cd frontend
                npm install
                npm run dev

    Follow the error message if problem occurs.
