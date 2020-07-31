import os
import dotenv

dotenv.load_dotenv()

try:
    os.mkdir('/root/.aws', )
except FileExistsError:
    pass

with open('/root/.aws/credentials', 'w+') as f:
    f.writelines(f'''[default]\naws_access_key_id={os.environ["AWSAccessKeyId"]}\naws_secret_access_key={os.environ["AWSSecretKey"]}\n ''')