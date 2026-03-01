# Import the Flask web framework and helper functions
from flask import Flask, render_template, request, url_for, redirect, flash  # render_template displays HTML pages, request gets the form input
from src.backend.helpdesk import tickets, save_tickets  # existing helpdesk ticket data and the save function
from operator import itemgetter  # for sorting dicts by key
from datetime import datetime # enables recording dates and times for tickets and logs
import json
import os
import csv

# Creating a new web app
app = Flask(__name__)

# Set the secret key for sessions (needed for flash messages)
# Use environment variable if set, otherwise fallback to a dev key
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

# Home page - shows dashboard with stats and recent tickets
@app.route("/")
def home():
    # Convert tickets dict to a list and sort by ID descending
    ticket_list = list(tickets.values())
    ticket_list.sort(key=lambda t: int(t["ID"]), reverse=True)  # newest first

    # Take the first 5 tickets
    recent_tickets = ticket_list[:5]

    severity_order = {"High": 0, "Medium": 1, "Low": 2}
    # Sort the 5 tickets only
    recent_tickets.sort(key=lambda t: severity_order.get(t["Severity"], 3))

    return render_template(
        "home.html",
        tickets=tickets.values(),
        recent_tickets=recent_tickets
    )

# All tickets page with optional filtering
@app.route("/tickets")
def all_tickets():
    filter_type = request.args.get("filter")  # read ?filter=Open or ?filter=High
    tickets_list = list(tickets.values())

    # Apply filter if needed
    if filter_type == "Open":
        tickets_list = [t for t in tickets_list if t["Status"] == "Open"]
    elif filter_type == "High":
        tickets_list = [t for t in tickets_list if t["Severity"] == "High"]

    # Always send full tickets for the stats cards
    return render_template("all_tickets.html", tickets=tickets_list, filter_type=filter_type, all_tickets=tickets.values())

# Add a new ticket
@app.route("/add", methods=["GET", "POST"])
def add_ticket_web():
    # Dynamically generate a list of unique assignees from existing tickets
    assignees = sorted({ticket["Assignee"] for ticket in tickets.values()})

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        assignee = request.form["assignee"]
        severity = request.form["severity"]
        status = request.form["status"]

        ticket_id = str(max(map(int, tickets.keys()), default=100) + 1)

        tickets[ticket_id] = {
            "ID": ticket_id,
            "Title": title,
            "Description": description,
            "Assignee": assignee,
            "Severity": severity,
            "Status": status,
            "Category": "Software",
            "Submission Date": "25/02/2026",  # can be updated dynamically
            "Submission Time": "19:30:10"
        }

        save_tickets(tickets)
        return render_template("add_success.html", ticket_id=ticket_id, title=title)

    return render_template("add.html", assignees=assignees)

# View a ticket in detail
@app.route("/ticket/<ticket_id>")
def view_ticket_web(ticket_id):
    ticket = tickets.get(ticket_id)
    if not ticket:
        return render_template("message.html", message=f"Ticket {ticket_id} not found.", back_url=url_for("home"))

    comments = ticket.get("Comments", [])  # get the list of comments
    assignees = get_assignees()
    return render_template("view.html", ticket=ticket, comments=comments, assignees=assignees)

# Update an existing ticket
@app.route("/update/<ticket_id>", methods=["GET", "POST"])
def update_ticket_web(ticket_id):
    ticket = tickets.get(ticket_id)
    if not ticket:
        flash(f"Ticket {ticket_id} not found.", "error")
        return redirect(url_for("home"))

    assignees = get_assignees()

    if request.method == "POST":
        # Update ticket fields
        ticket.update({
            "Title": request.form["title"],
            "Description": request.form["description"],
            "Assignee": request.form["assignee"],
            "Severity": request.form["severity"],
            "Status": request.form["status"],
            "Category": request.form["category"]
        })
        save_tickets(tickets)

        # Flash success message and redirect to view_ticket
        flash(f"Ticket {ticket_id} updated successfully!", "success")
        return redirect(url_for("view_ticket_web", ticket_id=ticket_id))

    # GET request → render the update form
    return render_template("update.html", ticket=ticket, assignees=assignees)

# Delete a ticket
@app.route("/delete/<ticket_id>", methods=["GET", "POST"])
def delete_ticket_web(ticket_id):
    ticket = tickets.get(ticket_id)
    if not ticket:
        return render_template(
            "message.html",
            message=f"Ticket {ticket_id} not found.",
            back_url=url_for("home"),
            card_class="error",
        )

    if request.method == "POST":
        confirm = request.form.get("confirm")
        if confirm == "yes":
            tickets.pop(ticket_id)
            save_tickets(tickets)
            return render_template(
                "message.html",
                message=f"Ticket {ticket_id} deleted successfully!",
                back_url=url_for("home"),
                card_class="success",
            )
        else:
            return render_template(
                "message.html",
                message="Deletion cancelled.",
                back_url=url_for("view_ticket_web", ticket_id=ticket_id),
                card_class="info",
            )

    return render_template("delete.html", ticket=ticket)

# Add a comment to a ticket
@app.route("/comment/<ticket_id>", methods=["GET", "POST"])
def comment_ticket_web(ticket_id):
    ticket = tickets.get(ticket_id)
    if not ticket:
        return render_template(
            "message.html",
            message=f"Ticket {ticket_id} not found.",
            back_url=url_for("home")
        )

    comment_text = None  

    if request.method == "POST":
        comment_text = request.form.get("comment", "").strip()
        if comment_text:
            ticket.setdefault("Comments", [])
            ticket["Comments"].append({
                "Author": "Web User", 
                "Date": datetime.now().strftime("%d/%m/%Y"),
                "Time": datetime.now().strftime("%H:%M:%S"),
                "Content": comment_text
            })
            save_tickets(tickets)
            flash(f"Comment added to ticket {ticket_id}!", "success")
            return redirect(url_for("view_ticket_web", ticket_id=ticket_id))

    return render_template("comment.html", ticket=ticket)

# Close a ticket (auto-redirect after closing)
@app.route("/close/<ticket_id>", methods=["POST"])
def close_ticket_web(ticket_id):
    ticket = tickets.get(ticket_id)
    if not ticket:
        return render_template(
            "message.html",
            message=f"Ticket {ticket_id} not found.",
            back_url=url_for("home"),
            card_class="error",
        )
    ticket["Status"] = "Closed"
    save_tickets(tickets)
    flash(f"Ticket {ticket_id} closed successfully!", "success")
    return redirect(url_for("view_ticket_web", ticket_id=ticket_id))

# helper function to get all unique assignees
def get_assignees():
    return sorted(set(ticket["Assignee"] for ticket in tickets.values()))

# Escalate a ticket (assign + set severity)
@app.route("/escalate/<ticket_id>", methods=["GET", "POST"])
def escalate_ticket_web(ticket_id):
    ticket = tickets.get(ticket_id)
    if not ticket:
        return render_template(
            "message.html",
            message=f"Ticket {ticket_id} not found.",
            back_url=url_for("home")
        )

    assignees = get_assignees() 

    if request.method == "POST":
        new_assignee = request.form["assignee"].strip()
        if new_assignee:
            ticket["Assignee"] = new_assignee
            ticket["Severity"] = "High"
            save_tickets(tickets)
            flash(f"Ticket {ticket_id} escalated to {new_assignee}!", "success")
            return redirect(url_for("view_ticket_web", ticket_id=ticket_id))

    return render_template("escalate.html", ticket=ticket, assignees=assignees)  

# Run the app
if __name__ == "__main__":
    print("Starting Flask app at http://127.0.0.1:5050")
    app.run(debug=True, port=5050)