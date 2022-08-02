from flask_restx.reqparse import RequestParser

pr_movie: RequestParser = RequestParser()
pr_movie.add_argument(name='page', type=int, location='args', required=False)
pr_movie.add_argument(name='status', type=str, location='args', required=False)

pr_page: RequestParser = RequestParser()
pr_page.add_argument(name='page', type=int, location='args', required=False)

pr_user: RequestParser = RequestParser()
pr_user.add_argument('email', type=str, required=True)
pr_user.add_argument('password', type=str, required=True)

pr_profile: RequestParser = RequestParser()
pr_profile.add_argument('name', type=str)
pr_profile.add_argument('surname', type=str)
pr_profile.add_argument('favourite_genre', type=int)

pr_passwords: RequestParser = RequestParser()
pr_passwords.add_argument('old_password', type=str, required=True)
pr_passwords.add_argument('new_password', type=str, required=True)

pr_refresh_token: RequestParser = RequestParser()
pr_refresh_token.add_argument('RefreshToken', type=str, location='cookies')
