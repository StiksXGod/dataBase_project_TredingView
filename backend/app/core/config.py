"""

Config settings 

"""




ALLOWED_CHARACTERS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_")
SECRET_KEY_ACCESS = "SOUOqvSs2v1Jc0d28bWBiRh05PEuOIrPDImzaJ9u"
SECRET_KEY_REFRESH = "IGiqd668Fc9bwp7HrSs8UKcBnRk1Y4uRxWYQYWvH"

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1
REFRESH_TOKEN_EXPIRE_DAYS = 3
DATABASE_URL = "postgresql://stiks:13072332@localhost:5432/tredingview"