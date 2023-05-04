from django.test import TestCase
from .models import Hotels, Comment, Type
# Create your tests here.
#

#
# class TestModels(TestCase):
#     def test_Types_model(self):
#         rname = Type.objects.create(Rname="Mexican")
#         self.assertEqual(str(rname), "Mexican")


from django.contrib.auth.models import User


# class ModelTest(TestCase):
#     def setUp(self):
#         # Create some users
#         self.user_1 = User.objects.create_user('Chevy Chase', 'chevy@chase.com', 'chevyspassword')
#         self.user_2 = User.objects.create_user('Jim Carrey', 'jim@carrey.com', 'jimspassword')
