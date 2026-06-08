# PDF Editor

A web application built with React and FastAPI that allows users to process PDF files directly from their browser.

## Features

* Merge PDF pages by cropping and combining halves
* Delete selected pages from a PDF
* Automatic PDF download after processing
* Simple and responsive web interface
* Temporary file cleanup after processing

## Tech Stack

### Frontend

* React
* Vite

### Backend

* FastAPI
* PyPDF2

## Project Structure

pdf-editor/

├── backend/

│   ├── main.py

│   ├── pdf_processor.py

│   └── uploads/

├── frontend/

└── README.md

## How to Run Locally

### Backend

Navigate to the backend folder:

```bash
cd backend
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the server:

```bash
uvicorn main:app --reload
```

Backend runs on:

```text
http://127.0.0.1:8000
```

### Frontend

Navigate to the frontend folder:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Run the frontend:

```bash
npm run dev
```

Frontend runs on:

```text
http://localhost:5173
```

## Future Improvements

* PDF rotation
* PDF splitting
* Better UI design
* Drag-and-drop file upload
* PDF compression

## Author

Built as a personal project to learn React, FastAPI, and full-stack development.
