# online_store_service.py
from Online_Store.data import Member, OerderItem, Payment, Product
from Online_Store.online_store_dao import OnlineStorDAO

class OnlineStroeService:
    def __init__(self):
        self.dao = OnlineStorDAO()
        self.login_membership = None