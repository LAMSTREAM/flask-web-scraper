
from authlib.integrations.flask_oauth2 import ResourceProtector
from api.utils import safe_get_env_var
from api.security.validator import Auth0JWTBearerTokenValidator


auth0_audience = safe_get_env_var("AUTH0_AUDIENCE")
auth0_domain = safe_get_env_var("AUTH0_DOMAIN")

require_auth = ResourceProtector()
validator = Auth0JWTBearerTokenValidator(
    auth0_domain,
    auth0_audience
)
require_auth.register_token_validator(validator)
