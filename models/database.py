
import certifi
from pymongo.mongo_client import MongoClient
from config.settings import MONGODB_URI, DATABASE_NAME


class DatabaseConnection:
    
    _instance = None
    _client = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance._connect()
        return cls._instance
    
    def _connect(self):
        try:
            self._client = MongoClient(MONGODB_URI, tlsCAFile=certifi.where())
            self._db = self._client[DATABASE_NAME]
            self._client.admin.command('ping')
            print("kết nối MongoDB")
        except Exception as e:
            print(f"Lỗi MongoDB: {e}")
            raise
    
    @property
    def db(self):
        return self._db
    
    @property
    def client(self):
        return self._client
    
    def close(self):
        if self._client:
            self._client.close()
            print("🔌 Đã đóng kết nối MongoDB")
