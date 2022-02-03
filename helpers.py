import os

class Helper:
  
  @staticmethod
  def get_encryption_key():
    return os.environ.get('MODEL_ENCRYPTION_KEY')