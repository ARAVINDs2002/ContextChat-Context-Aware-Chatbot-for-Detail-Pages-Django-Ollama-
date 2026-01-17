import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realestate_chatbot.settings')
django.setup()

from django.core.management import call_command
from chatbot.models import House, Place, HouseDistance

class TestChatbot(unittest.TestCase):
    def setUp(self):
        # Setup specific test data separate from the main DB if possible, 
        # but for this simple verifying script, we can rely on create_data or just create fresh here.
        # To be safe and independent, let's create our own.
        House.objects.all().delete()
        Place.objects.all().delete()
        HouseDistance.objects.all().delete()

        self.house = House.objects.create(name="Test House", location="Loc", price="100")
        self.hospital = Place.objects.create(name="Test Hosp", category="medical")
        HouseDistance.objects.create(house=self.house, place=self.hospital, distance_in_meters=100)

    @patch('chatbot.management.commands.chat.generate_response')
    def test_ai_flow(self, mock_ai):
        """Test that AI is called when data exists"""
        mock_ai.return_value = "AI Response"
        
        out = StringIO()
        call_command('chat', self.house.id, 'Is there a hospital?', stdout=out)
        
        # Verify AI was called
        mock_ai.assert_called_once()
        # Verify output contains AI response
        self.assertIn("AI Response", out.getvalue())

    @patch('chatbot.management.commands.chat.generate_response')
    def test_manual_fallback_missing_data(self, mock_ai):
        """Test manual fallback when specific category is missing"""
        out = StringIO()
        # We didn't create a school
        call_command('chat', self.house.id, 'Is there a school?', stdout=out)
        
        # Verify AI was NOT called
        mock_ai.assert_not_called()
        # Verify manual response
        self.assertIn("Sorry, that information isn’t available", out.getvalue())

    @patch('chatbot.management.commands.chat.generate_response')
    def test_manual_fallback_unknown_intent(self, mock_ai):
        """Test manual fallback for unknown intent"""
        out = StringIO()
        call_command('chat', self.house.id, 'Is there a gym?', stdout=out)
        
        mock_ai.assert_not_called()
        self.assertIn("I can help with nearby hospitals", out.getvalue())

if __name__ == '__main__':
    unittest.main()
