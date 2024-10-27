# URL Shortener

A simple URL shortener application built with Flask for the backend and React.js for the frontend. This project was created in 2 days as a quick and functional tool to generate and manage shortened URLs.

## Showcase

https://files.offshore.cat/XNd4Vk2e.mp4

## Features

- Shorten long URLs to easy-to-share links.
- Store shortened URLs in a database for easy access.
- React-based frontend for a modern and responsive user interface.
- Custom alias for your shortened links.
- Edit shortened links to change source URL any time, using link passwords.

## Tech Stack

- **Backend:** Flask (Python)
- **Frontend:** React.js
- **Database:** SQLite3

## Prerequisites

- [Git](https://git-scm.com/)
- [Python](https://www.python.org/downloads/)
- [Node.js and npm](https://nodejs.org/)

## Installation

To get started with the project, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/tadas-vnc/url-shortener.git
   cd url-shortener
   ```

2. **Run the Backend (Flask):**
   ```bash
   python app.py
   ```

3. **Run the Frontend (React):**
   ```bash
   cd front-end
   npm install
   npm start
   ```

4. Open [localhost:3000](http://localhost:3000) in your browser to access the frontend.

## Project Structure

- **Backend** (Flask): Handles URL shortening logic and database operations.
- **Frontend** (React): Provides a simple, user-friendly interface to interact with the URL shortener.
