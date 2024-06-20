from django.test import TestCase
from .models import Submission
from django.utils import timezone
from django.core.exceptions import ValidationError

class SubmitTest(TestCase):
    def test_valid_submission(self):
        # Create a valid submission
        submission = Submission.objects.create(
            title="Valid submission",
            description="Valid description",
            background_info="Valid background info",
            involved_students="Valid student",
            submit_date=timezone.now()
        )
        # Check that the submission was created
        self.assertEqual(Submission.objects.count(), 1)
        self.assertEqual(Submission.objects.first(), submission)

    def test_invalid_submission(self):
        # Attempt to create an invalid submission with a missing title
        submission = Submission(
            title="", 
            description="Invalid description",
            background_info="Invalid background",
            involved_students="Invalid Student",
            submit_date=timezone.now()
        )
        # Check that the submission raises a ValidationError
        with self.assertRaises(ValidationError):
            submission.full_clean()