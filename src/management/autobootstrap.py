from sqlalchemy import select, exists
from models.users import User
from db.database import get_session
from services.auth import AuthService
from schemas.user import UserRegister

from core.conf import settings

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def create_default_user():
    session = next(get_session())

    default_user = None

    try: 
        if session is None:
            raise ValueError("Session must be provided or created within the function.")

        #[TODO]
        existing_user = session.scalar(select(exists().where(User.username == "admin_1")))
        if existing_user:
            logger.info("Default user already exists, skipping creation.")
            return

        # use auth service to create user also give him super-admin role having all the permissions
        user_payload = UserRegister(username='admin_1', email='admin1@ecom.com', password="123456")
        default_user = AuthService.register_user(user_payload, session)
        logger.info(f"Default user created: {default_user.data.username}")
    except Exception as e:
        session.rollback()
        logger.error(f"Error creating default user: {e}")
        raise

if __name__ == "__main__":
    create_default_user()