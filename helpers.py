import base64
import os

class Helper:
  @staticmethod
  def get_encryption_key():
    return os.environ.get('MODEL_ENCRYPTION_KEY')
  
  @staticmethod
  def get_model_id(encrypted_id: str) -> int:
    id_secret_key = base64.b64decode(encrypted_id).decode('utf-8')
    id = id_secret_key.split(os.environ.get('MODEL_ENCRYPTION_KEY'))[0]
    return int(id)
  