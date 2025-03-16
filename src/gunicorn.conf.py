import multiprocessing
from dotenv import read_dotenv

read_dotenv()

bind: str = "0.0.0.0:8000"
workers: int = int(multiprocessing.cpu_count())
accesslog: str = "-"  # Use stdout for access logs
errorlog: str = "-"  # Use stdout for error logs
