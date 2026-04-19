import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-insecure-change-me")
DEBUG = os.environ.get("DJANGO_DEBUG", "true").lower() in ("1", "true", "yes")

ALLOWED_HOSTS = [h.strip() for h in os.environ.get("DJANGO_ALLOWED_HOSTS", "*").split(",") if h.strip()]

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "corsheaders",
    "rest_framework",
    "drf_spectacular",
    "api",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "api.urls"
WSGI_APPLICATION = "api.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.environ.get("DJANGO_SQLITE_PATH", str(BASE_DIR / "db.sqlite3")),
    }
}

AUTH_PASSWORD_VALIDATORS: list = []

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CORS_ALLOW_ALL_ORIGINS = os.environ.get("CORS_ALLOW_ALL_ORIGINS", "true").lower() in ("1", "true", "yes")

FILE_UPLOAD_ENABLED = os.environ.get("FILE_UPLOAD_ENABLED", "true").lower() in ("1", "true", "yes")
TMP_UPLOADED_FILES = os.environ.get("TMP_UPLOADED_FILES")
if FILE_UPLOAD_ENABLED and TMP_UPLOADED_FILES:
    FILE_UPLOAD_TEMP_DIR = TMP_UPLOADED_FILES

# Force disk-backed uploads so validators and audiometa always see a real path (matches larger uploads).
FILE_UPLOAD_MAX_MEMORY_SIZE = 0

UPLOADED_TRACK_FILE_EXTENSIONS = [e.strip().lower() for e in os.environ.get(
    "UPLOADED_TRACK_FILE_EXTENSIONS", ".mp3,.wav,.flac,.ogg"
).split(",") if e.strip()]
UPLOADED_TRACK_FILE_SIZE_MAX_IN_MO = float(os.environ.get("UPLOADED_TRACK_FILE_SIZE_MAX_IN_MO", "100"))
UPLOADED_TRACK_FILE_SIZE_MIN_IN_MO = float(os.environ.get("UPLOADED_TRACK_FILE_SIZE_MIN_IN_MO", "0"))
UPLOADED_TRACK_FILENAME_LEN_MAX = int(os.environ.get("UPLOADED_TRACK_FILENAME_LEN_MAX", "255"))

METADATA_SESSION_DIR: Path | None = None
if FILE_UPLOAD_ENABLED:
    _ms = os.environ.get("METADATA_SESSION_DIR")
    METADATA_SESSION_DIR = Path(_ms).resolve() if _ms else (BASE_DIR / "metadata-sessions").resolve()

MEDIA_ROOT = Path(os.environ.get("MEDIA_ROOT", str(BASE_DIR / "media"))).resolve()
MEDIA_URL = "/media/"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "audiometa-api-cache",
    }
}

API_ROOT_BASE = os.environ.get("API_ROOT_BASE", "v1/")

AFP_BASE_URL = os.environ.get("AFP_BASE_URL", "localhost")
AFP_PORT = os.environ.get("AFP_PORT", "3002")
AFP_POST_ENDPOINT = os.environ.get("AFP_POST_ENDPOINT", "fingerprint-audio")
ACOUSTID_API_KEY = os.environ.get("ACOUSTID_API_KEY", "")

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_RENDERER_CLASSES": ("djangorestframework_camel_case.render.CamelCaseJSONRenderer",),
    "DEFAULT_PARSER_CLASSES": (
        "djangorestframework_camel_case.parser.CamelCaseJSONParser",
        "djangorestframework_camel_case.parser.CamelCaseMultiPartParser",
        "djangorestframework_camel_case.parser.CamelCaseFormParser",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": os.environ.get("APP_TITLE", "AudioMeta API"),
    "DESCRIPTION": "Public metadata session API (upload, read metadata, download with tags).",
    "VERSION": os.environ.get("APP_VERSION", "0.0.0"),
    "SERVE_INCLUDE_SCHEMA": False,
}
