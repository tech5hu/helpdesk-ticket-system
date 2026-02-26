# Import the Flask web framework and helper functions
from flask import Flask, render_template, request  # render_template displays HTML pages, request gets the form input
from helpdesk import tickets, save_tickets  # existing helpdesk ticket data and the save function
from operator import itemgetter  # for sorting dicts by key

# Creating a new web app
app = Flask(__name__)

# Home page - shows dashboard with stats and recent tickets
@app.route("/")
def home():
    # Sort tickets by Submission Date descending (latest first)
    recent_tickets = sorted(
        tickets.values(),
        key=itemgetter('Submission Date', 'Submission Time'),  # sort by date+time
        reverse=True
    )[:5]  # show last 5 tickets
    return render_template("home.html", tickets=tickets.values(), recent_tickets=recent_tickets)

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
    return render_template("index.html", tickets=tickets_list, filter_type=filter_type, all_tickets=tickets.values())

# Add a new ticket
@app.route("/add", methods=["GET", "POST"])
def add_ticket_web():
    if request.method == "POST":
        # Get form data
        title = request.form["title"]
        description = request.form["description"]
        assignee = request.form["assignee"]
        severity = request.form["severity"]
        status = request.form["status"]

        # Automatically assign a new unique ticket ID
        ticket_id = str(max(map(int, tickets.keys()), default=100) + 1)

        # Create a new ticket
        tickets[ticket_id] = {
            "ID": ticket_id,
            "Title": title,
            "Description": description,
            "Assignee": assignee,
            "Severity": severity,
            "Status": status,
            "Category": "Software",
            "Submission Date": "25/02/2026",  # update dynamically if needed
            "Submission Time": "19:30:10"
        }

        save_tickets(tickets)
        return "Ticket added!"

    return render_template("add.html")

# View a ticket in detail
@app.route("/view/<ticket_id>")
def view_ticket_web(ticket_id):
    ticket = tickets.get(ticket_id)
    if not ticket:
        return f"Ticket {ticket_id} not found."
    return render_template("view.html", ticket=ticket)

# Update an existing ticket
@app.route("/update/<ticket_id>", methods=["GET", "POST"])
def update_ticket_web(ticket_id):
    ticket = tickets.get(ticket_id)
    if not ticket:
        return f"Ticket {ticket_id} not found."

    if request.method == "POST":
        ticket.update({
            "Title": request.form["title"],
            "Description": request.form["description"],
            "Assignee": request.form["assignee"],
            "Severity": request.form["severity"],
            "Status": request.form["status"],
            "Category": request.form["category"]
        })
        save_tickets(tickets)
        return f"Ticket {ticket_id} updated successfully!"

    return render_template("update.html", ticket=ticket)

# Delete a ticket
@app.route("/delete/<ticket_id>", methods=["GET", "POST"])
def delete_ticket_web(ticket_id):
    ticket = tickets.get(ticket_id)
    if not ticket:
        return f"Ticket {ticket_id} not found."

    if request.method == "POST":
        confirm = request.form.get("confirm")
        if confirm == "yes":
            tickets.pop(ticket_id)
            save_tickets(tickets)
            return f"Ticket {ticket_id} deleted successfully!"
        return "Deletion cancelled."

    return render_template("delete.html", ticket=ticket)

# Run the app
if __name__ == "__main__":
    print("Starting Flask app at http://127.0.0.1:5050")
    app.run(debug=True, port=5050)