
from models.database import DatabaseConnection


class UserModel:
    
    def __init__(self):
        self.db = DatabaseConnection()
        self.collection = self.db.db.users
    
    def authenticate(self, username: str, password: str) -> dict:

        user = self.collection.find_one({
            'username': username,
            'password': password
        })
        return user
    
    def get_user_by_id(self, user_id: str) -> dict:
        from bson import ObjectId
        return self.collection.find_one({'_id': ObjectId(user_id)})
    
    def get_user_by_username(self, username: str) -> dict:
        return self.collection.find_one({'username': username})
    
    def update_user(self, user_id: str, data: dict) -> bool:
        from bson import ObjectId
        result = self.collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': data}
        )
        return result.modified_count > 0

    def get_user_balance(self, user_id:str):
        return self.collection.find_one({'user_id': user_id})['balance']