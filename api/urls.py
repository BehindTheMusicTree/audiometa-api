from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from api import settings
from api.view.AudioMetadataView import AudioMetadataView
from api.view.AudioMetadataSessionDownloadView import AudioMetadataSessionDownloadView
from api.view.AudioMetadataSessionView import AudioMetadataSessionView
from api.view.health import HealthCheckView

urlpatterns = [
    path(settings.API_ROOT_BASE + settings.API_METADATA_ROUTE_PREFIX + "full/", AudioMetadataView.as_view(), name="audio-metadata-full"),
    path(settings.API_ROOT_BASE + settings.API_METADATA_ROUTE_PREFIX + "session/", AudioMetadataSessionView.as_view(), name="audio-metadata-session"),
    path(
        settings.API_ROOT_BASE + settings.API_METADATA_ROUTE_PREFIX + "session-download/",
        AudioMetadataSessionDownloadView.as_view(),
        name="audio-metadata-session-download",
    ),
    path("health/", HealthCheckView.as_view(), name="health-check"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
