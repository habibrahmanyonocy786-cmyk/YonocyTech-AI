import os
import json
import hashlib
import secrets
import time
from typing import Optional, Dict, Any

import httpx
from authlib.integrations.httpx_client import OAuth2Client
from authlib.oauth2 import OAuth2Error


class GoogleAuth:
    def __init__(self):
        self.client_id = os.getenv("GOOGLE_CLIENT_ID", "")
        self.client_secret = os.getenv("GOOGLE_CLIENT_SECRET", "")
        self.redirect_uri = os.getenv(
            "GOOGLE_REDIRECT_URI",
            "http://localhost:8501"
        )
        self.discovery_url = "https://accounts.google.com/.well-known/openid-configuration"

    @property
    def is_configured(self) -> bool:
        return bool(self.client_id and self.client_secret)

    def get_login_url(self) -> str:
        state = secrets.token_urlsafe(32)
        # Store state in session for verification
        import streamlit as st
        st.session_state["oauth_state"] = state

        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": "openid email profile",
            "state": state,
            "access_type": "offline",
            "prompt": "select_account",
        }
        from urllib.parse import urlencode
        return f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"

    async def handle_callback(self, code: str, state: str) -> Optional[Dict[str, Any]]:
        import streamlit as st

        # Verify state
        saved_state = st.session_state.pop("oauth_state", None)
        if not saved_state or saved_state != state:
            return None

        try:
            async with httpx.AsyncClient() as client:
                # Exchange code for tokens
                token_response = await client.post(
                    "https://oauth2.googleapis.com/token",
                    data={
                        "code": code,
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                        "redirect_uri": self.redirect_uri,
                        "grant_type": "authorization_code",
                    },
                    headers={"Accept": "application/json"},
                )
                token_response.raise_for_status()
                tokens = token_response.json()

                if "id_token" not in tokens:
                    return None

                # Decode ID token (it's a JWT, just decode the payload)
                import base64
                payload = tokens["id_token"].split(".")[1]
                # Add padding
                payload += "=" * (4 - len(payload) % 4)
                try:
                    user_info = json.loads(base64.b64decode(payload))
                except Exception:
                    # Fallback: get user info from Google API
                    user_response = await client.get(
                        "https://www.googleapis.com/oauth2/v2/userinfo",
                        headers={"Authorization": f"Bearer {tokens['access_token']}"},
                    )
                    user_response.raise_for_status()
                    user_info = user_response.json()

                return {
                    "name": user_info.get("name", "User"),
                    "email": user_info.get("email", ""),
                    "picture": user_info.get("picture", ""),
                    "sub": user_info.get("sub", ""),
                    "login_time": time.time(),
                }

        except Exception as e:
            print(f"OAuth callback error: {e}")
            return None

    def get_user(self) -> Optional[Dict[str, Any]]:
        import streamlit as st
        return st.session_state.get("user", None)

    def is_admin(self) -> bool:
        admin_email = os.getenv("ADMIN_EMAIL", "")
        user = self.get_user()
        if not user or not admin_email:
            return False
        return user.get("email", "") == admin_email

    def logout(self):
        import streamlit as st
        st.session_state.pop("user", None)
        st.session_state.pop("oauth_state", None)
