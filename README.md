# Library Management System

This project is a Python Tkinter desktop app for basic library management.

## Setup

Install the dependency:

```bash
pip install -r requirements.txt
```

Set these environment variables before running the app:

```bash
SUPABASE_URL=your-project-url
SUPABASE_KEY=your-supabase-key
```

## Required Supabase Tables

The app expects these tables:

- `books` with `book_id`, `title`, `author`, `isbn`, `quantity`, `borrowed_time`, `return_time`
- `users` with `username`, `password`
- `admins` with `admin_username`, `admin_password`
