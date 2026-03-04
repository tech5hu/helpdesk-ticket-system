
---

# Helpdesk Ticketing System (CLI + Flask Web App)

A Full Stack Helpdesk Ticket Management System built with Python and Flask.

This project began as a command line application and was later extended into a web application. It demonstrates backend logic, CRUD operations, data persistence, AI integration, and web development using Flask and Jinja templates.

---

## Table of Contents

* [Overview](#overview)
* [AI Integration (CLI Version Only)](#ai-integration-cli-version-only)
* [Key Features](#key-features)

  * [Ticket Management](#ticket-management)
  * [Dashboard & Filtering](#dashboard--filtering)
  * [Data Integrity & Validation](#data-integrity--validation)
* [Project Documentation](#project-documentation)
* [Tech Stack](#tech-stack)
* [Running the Application](#running-the-application)

  * [Clone the Repository](#1-clone-the-repository)
  * [Create a Virtual Environment](#2-create-a-virtual-environment)
  * [Install Dependencies](#3-install-dependencies)
  * [Run the Flask Web App](#4-run-the-flask-web-app)
  * [Open in Browser](#5-open-in-browser)
  * [Run the CLI Version](#running-the-cli-version)
  * [Optional: Enable AI Features (CLI Only)](#optional-enable-ai-features-cli-only)
* [Data Storage](#data-storage)
* [Skills Demonstrated](#skills-demonstrated)
* [Potential Future Improvements](#potential-future-improvements)
* [Author](#author)

---

## Overview

The Helpdesk system allows users to create, manage, and track support tickets. It supports ticket creation, updates, filtering, escalation, commenting, and status management.

The application uses CSV based storage for persistence and implements data normalisation to maintain consistent and validated assignee records.

The project is split into two interfaces:

* CLI Application (with AI assisted classification)
* Flask Web Application (GUI interface)

---

## AI Integration (CLI Version Only)

The command line version integrates the OpenAI API to provide intelligent ticket classification.

When creating or updating a ticket, the system:

* Analyses the ticket title and description
* Suggests an appropriate category: Hardware, Software, Network, Security
* Suggests a severity level: Low, Medium, High
* Validates AI output against predefined allowed values
* Falls back to default values if the API key is not configured or if an error occurs

The AI suggestions are advisory — users can review and override them before saving the ticket.

This demonstrates practical AI integration using:

* Prompt engineering
* API request handling
* Response parsing and validation
* Error handling and fallback logic
* Controlled AI assisted decision support

---

## Key Features

### Ticket Management

* Create new tickets
* View all tickets
* View individual ticket details
* Update ticket information
* Delete tickets (with confirmation)
* Close tickets
* Escalate tickets 
* Add timestamped comments

### Dashboard & Filtering

* Homepage dashboard displaying:

  * Most recent tickets
  * Severity based prioritisation
* Filter tickets by:

  * Open status
  * High severity

### Data Integrity & Validation

* Enforced list of valid assignees
* Automatic normalisation of partial or inconsistent names
* Controlled category and severity values
* Persistent storage via CSV file
* Flash messaging for user feedback

---

## Project Documentation

This project includes formal software documentation:

* Design Document
* Test Plan
* UML Activity Diagram
* UML Navigation Diagram
* UML Use Case Diagram

These documents demonstrate structured software planning, system modelling, and testing strategy.

---

## Tech Stack

* Python 3
* Flask
* Jinja2 templating
* HTML
* CSS
* CSV for data storage
* OpenAI API (CLI AI classification)
* python-dotenv (environment variable management)

---

## Running the Application

### 1. Clone the Repository


git clone https://github.com/tech5hu/helpdesk-ticket-system.git

cd helpdesk-ticket-system


### 2. Create a Virtual Environment


python -m venv venv


Activate it:

**macOS / Linux**


source venv/bin/activate


**Windows**


venv\Scripts\activate


### 3. Install Dependencies


pip install flask python-dotenv openai


### 4. Run the Flask Web App


python -m src.web.web_app


### 5. Open in Browser


http://127.0.0.1:5050


---

### Running the CLI Version

From the project root:


python -m src.cli.cli_helpdesk


(The CLI version includes optional AI assisted ticket classification.)

---

### Optional: Enable AI Features (CLI Only)

To enable AI powered ticket suggestions:

1. Create a `.env` file in the project root
2. Add your OpenAI API key:


OPENAI_API_KEY=your_api_key_here


If no API key is configured, the system will default to predefined category and severity values.

---

## Data Storage

* Tickets are stored in `data/helpdesk.csv`
* Data is loaded into memory at startup
* All modifications are written back to the CSV file
* Comments are stored as structured lists within each ticket

---

## Skills Demonstrated

* Backend architecture design
* Full CRUD application development
* Flask routing and template rendering
* Form handling (GET/POST)
* Session management and flash messaging
* Data validation and normalisation
* Persistent file based storage
* Modular project structure
* CLI to web application evolution
* Practical AI integration with external APIs
* System modelling using UML diagrams
* Test planning and documentation

---

## Potential Future Improvements

* Replace CSV storage with SQLite or PostgreSQL
* Add authentication and role based access control
* Implement search functionality
* Add REST API endpoints
* Integrate AI classification into the web interface

---

## Author

Developed as a Full Stack Python project to strengthen backend architecture, structured data handling, AI integration, and web application development skills.


