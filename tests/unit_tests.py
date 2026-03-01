import unittest
from unittest.mock import patch
from src.cli.cli_helpdesk import (
    tickets,
    add_ticket_ai,
    update_ticket_ai,
    delete_ticket_with_input,
    close_ticket,
    comment_ticket,
    escalate_ticket_ai,
)

class TestCLIHelpdesk(unittest.TestCase):
    def setup_ticket(self):
        test_id = max(tickets.keys(), default=100) + 1
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
        return test_id

    def teardown_ticket(self, ticket_id):
        tickets.pop(ticket_id, None)

    def test_add_ticket_ai(self):
        inputs = iter(["New AI Ticket", "Description", "", "", "Alice"])
        with patch("builtins.input", lambda _: next(inputs)):
            add_ticket_ai()
        new_id = max(tickets.keys())
        self.assertEqual(tickets[new_id]["Title"], "New AI Ticket")
        self.assertEqual(tickets[new_id]["Assignee"], "Alice")
        self.teardown_ticket(new_id)

    def test_update_ticket_ai(self):
        ticket_id = self.setup_ticket()
        inputs = iter([str(ticket_id), "Updated Title", "Updated description", "", "", "Bob"])
        with patch("builtins.input", lambda _: next(inputs)):
            update_ticket_ai(tickets)
        self.assertEqual(tickets[ticket_id]["Title"], "Updated Title")
        self.assertEqual(tickets[ticket_id]["Assignee"], "Bob")
        self.teardown_ticket(ticket_id)

    def test_delete_ticket_with_input(self):
        ticket_id = self.setup_ticket()
        with patch("builtins.input", lambda _: str(ticket_id)):
            delete_ticket_with_input(tickets)
        self.assertNotIn(ticket_id, tickets)

    def test_close_ticket(self):
        ticket_id = self.setup_ticket()
        with patch("builtins.input", lambda _: str(ticket_id)):
            close_ticket(tickets)
        self.assertEqual(tickets[ticket_id]["Status"], "Closed")
        self.teardown_ticket(ticket_id)

    def test_comment_ticket(self):
        ticket_id = self.setup_ticket()
        inputs = iter([str(ticket_id), "Alice", "This is a test comment"])
        with patch("builtins.input", lambda _: next(inputs)):
            comment_ticket(tickets)
        self.assertEqual(tickets[ticket_id]["Comments"][0]["Content"], "This is a test comment")
        self.teardown_ticket(ticket_id)

    def test_escalate_ticket_ai(self):
        ticket_id = self.setup_ticket()
        tickets[ticket_id]["Severity"] = "Low"
        with patch("builtins.input", lambda _: str(ticket_id)):
            escalate_ticket_ai(tickets)
        self.assertIn(tickets[ticket_id]["Severity"], ["Low", "High"])
        self.teardown_ticket(ticket_id)

if __name__ == "__main__":
    unittest.main()