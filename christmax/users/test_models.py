from django.contrib.auth import get_user_model
User = get_user_model()

# def test_username_auto_generation_from_email(db):
#     """Username should be auto-generated from email if not provided."""
#     user1 = User.objects.create_user(
#         email='john.doe@example.com',
#         password='test123',
#     )
#     assert user1.username == 'john_doe'

#     user2 = User.objects.create_user(
#         email='john.doe@different.com',
#         password='test123',
#     )
#     assert user2.username == 'john_doe_1'

