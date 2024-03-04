import json
import hashlib
from src.utils.field import Field

class FieldEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Field):
            return obj.val
        return super().default(obj)
    
def id_hash(a: str):
    return int(hashlib.sha256(a.encode('utf-8')).hexdigest(), 16)