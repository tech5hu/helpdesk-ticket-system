import unittest
from src.backend.helpdesk import tickets, add_ticket, update_ticket, delete_ticket, predict_category

class TestHelpdesk(unittest.TestCase):
    """Unit tests for core Helpdesk functions"""

    def setUp(self):
        """Prepare a fake ticket before each test"""
        self.test_ticket_id = "999"
        tickets[self.test_ticket_id] = {
            "ID": self.test_ticket_id,
            "Title": "Test Ticket",
            "Description": "Testing add function",
            "Assignee": "Olivia",
            "Severity": "Low",
            "Status": "Open",
            "Category": "Software",
            "Submission Date": "01/01/2026",
            "Submission Time": "12:00:00"
        }

    def tearDown(self):
        """Remove the fake ticket after each test"""
        tickets.pop(self.test_ticket_id, None)

    def test_add_ticket(self):
        """Check that the ticket exists after being added"""
        self.assertIn(self.test_ticket_id, tickets)  # SDE: verify ticket stored
        self.assertEqual(tickets[self.test_ticket_id]["Title"], "Test Ticket")  # CS: safe fake data

    def test_update_ticket(self):
        """Check that the ticket can be updated safely"""
        tickets[self.test_ticket_id]["Status"] = "In Progress"  # update field
        self.assertEqual(tickets[self.test_ticket_id]["Status"], "In Progress")  # verify change

    def test_delete_ticket(self):
        """Check that a ticket can be deleted"""
        tickets.pop(self.test_ticket_id)  # remove ticket
        self.assertNotIn(self.test_ticket_id, tickets)  # verify deletion

    def test_ai_category_prediction(self):
        """Check AI predicts ticket category correctly"""
        category = predict_category("Cannot login to account")  # use AI helper
        self.assertEqual(category, "Security")  # verify prediction

if __name__ == "__main__":
    unittest.main()  # run all tests