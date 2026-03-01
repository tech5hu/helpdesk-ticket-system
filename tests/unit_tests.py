import unittest
from unittest.mock import patch  # allows to fake user input()
from src.cli.cli_helpdesk import (
    tickets,
    add_ticket_ai,
    update_ticket_ai,
    delete_ticket_with_input,
    close_ticket,
    comment_ticket,
    escalate_ticket_ai,
)

# class to group all CLI tests together
class TestCLIHelpdesk(unittest.TestCase):

    # Helper method - creating a temp ticket for testing
    def setup_ticket(self):
        # creating a new unique ticket ID
        test_id = max(tickets.keys(), default=100) + 1

        # adding a fake ticket into the tickets dictionary
        tickets[test_id] = {
            "ID": test_id,
            "Title": "Initial Ticket",
            "Description": "Initial description",
            "Assignee": "Olivia",
            "Severity": "Low",
            "Status": "Open",
            "Category": "Software",
            "Submission DateTime": "2026-01-01 12:00:00",
            "Comments": []
        }

        return test_id  # return ID so tests can use it

    # helper method - removing the test ticket after test finishes
    def teardown_ticket(self, ticket_id):
        tickets.pop(ticket_id, None)  # safely delete ticket if it exists


    # TEST - Add ticket
    def test_add_ticket_ai(self):
        # simulating user typing inputs in the CLI
        inputs = iter([
            "New AI Ticket",      # title
            "Description",        # description
            "",                   # accept suggested category
            "",                   # accept suggested severity
            "Alice"               # assignee
        ])

        # replacing input() with fake inputs
        with patch("builtins.input", lambda _: next(inputs)):
            add_ticket_ai()

        # getting the newest ticket that was just added
        new_id = max(tickets.keys())

        # checking that values were saved correctly
        self.assertEqual(tickets[new_id]["Title"], "New AI Ticket")
        self.assertEqual(tickets[new_id]["Assignee"], "Alice")

        # cleaning up test data
        self.teardown_ticket(new_id)


    # TEST - Update ticket
    def test_update_ticket_ai(self):
        ticket_id = self.setup_ticket()  # create ticket to update

        inputs = iter([
            str(ticket_id),       # ticket ID to update
            "Updated Title",      # new title
            "Updated description",
            "",                   # accept suggested category
            "",                   # accept suggested severity
            "Bob"                 # new assignee
        ])

        with patch("builtins.input", lambda _: next(inputs)):
            update_ticket_ai(tickets)

        # verify ticket was updated
        self.assertEqual(tickets[ticket_id]["Title"], "Updated Title")
        self.assertEqual(tickets[ticket_id]["Assignee"], "Bob")

        self.teardown_ticket(ticket_id)


    # TEST - Delete ticket
    def test_delete_ticket_with_input(self):
        ticket_id = self.setup_ticket()

        # simulate entering the ticket ID to delete
        with patch("builtins.input", lambda _: str(ticket_id)):
            delete_ticket_with_input(tickets)

        # confirm ticket no longer exists
        self.assertNotIn(ticket_id, tickets)


    # TEST - Close ticket
    def test_close_ticket(self):
        ticket_id = self.setup_ticket()

        with patch("builtins.input", lambda _: str(ticket_id)):
            close_ticket(tickets)

        # confirm status changed to Closed
        self.assertEqual(tickets[ticket_id]["Status"], "Closed")

        self.teardown_ticket(ticket_id)


    # TEST - Comment on ticket
    def test_comment_ticket(self):
        ticket_id = self.setup_ticket()

        inputs = iter([
            str(ticket_id),           # ticket ID
            "Alice",                  # comment author
            "This is a test comment"  # comment content
        ])

        with patch("builtins.input", lambda _: next(inputs)):
            comment_ticket(tickets)

        # confirm comment was added correctly
        self.assertEqual(
            tickets[ticket_id]["Comments"][0]["Content"],
            "This is a test comment"
        )

        self.teardown_ticket(ticket_id)


    # TEST - Escalate ticket
    def test_escalate_ticket_ai(self):
        ticket_id = self.setup_ticket()

        # start with low severity
        tickets[ticket_id]["Severity"] = "Low"

        with patch("builtins.input", lambda _: str(ticket_id)):
            escalate_ticket_ai(tickets)

        # severity may stay low or change to high depending on AI suggestion
        self.assertIn(
            tickets[ticket_id]["Severity"],
            ["Low", "High"]
        )

        self.teardown_ticket(ticket_id)


# allowing the file to run directly
if __name__ == "__main__":
    unittest.main()