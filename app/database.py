import logging
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Debugging ---
logger.info("--- Starting Database Initialization ---")
db_path = "/app/data/margaritas.db"
logger.info(f"Expected database file path: {db_path}")

# Check if the data directory exists and what its permissions are
data_dir = os.path.dirname(db_path)
if os.path.isdir(data_dir):
    logger.info(f"Data directory '{data_dir}' exists.")
    try:
        logger.info(f"Permissions for '{data_dir}': {oct(os.stat(data_dir).st_mode)[-3:]}")
        logger.info(f"Owner of '{data_dir}': {os.stat(data_dir).st_uid}:{os.stat(data_dir).st_gid}")
    except Exception as e:
        logger.error(f"Could not stat directory '{data_dir}': {e}")
else:
    logger.warning(f"Data directory '{data_dir}' does not exist.")

# Check if the database file exists and what its permissions are
if os.path.isfile(db_path):
    logger.info(f"Database file '{db_path}' exists.")
    try:
        logger.info(f"Permissions for '{db_path}': {oct(os.stat(db_path).st_mode)[-3:]}")
        logger.info(f"Owner of '{db_path}': {os.stat(db_path).st_uid}:{os.stat(db_path).st_gid}")
    except Exception as e:
        logger.error(f"Could not stat file '{db_path}': {e}")
else:
    logger.info(f"Database file '{db_path}' does not exist. It will be created on first connection.")
# --- End Debugging ---


DATABASE_URL = f"sqlite+aiosqlite:///{db_path}"
logger.info(f"Connecting to database with URL: {DATABASE_URL}")


try:
    logger.info("Creating async engine...")
    en_async = create_async_engine(DATABASE_URL, echo=True)
    logger.info("Async engine created successfully.")

    logger.info("Creating session maker...")
    AsyncSessionLocal = sessionmaker(en_async, class_=AsyncSession, expire_on_commit=False)
    logger.info("Session maker created successfully.")

except Exception as e:
    logger.error(f"An error occurred during database initialization: {e}", exc_info=True)
    raise

logger.info("--- Database Initialization Complete ---")

async def get_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()
