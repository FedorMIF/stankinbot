from diagrams import Diagram, Cluster
from diagrams.programming.language import Python
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.client import User, Users
with Diagram("Telegram Bot UML", show=True, direction="TB"):
    with Cluster("User"):
        user = User("User")
        role = Users("Role")
        user - role

    with Cluster("TelegramBot"):
        telegram_bot = Python("TelegramBot")
        user << telegram_bot >> role

    with Cluster("Database"):
        database = PostgreSQL("Users")
        telegram_bot - database

    with Cluster("Way"):
        route_calculator = Python("way.py")
        telegram_bot - route_calculator

    with Cluster("Schedule"):
        schedule_scraper = Python("scheduleParse.py")
        telegram_bot - schedule_scraper
