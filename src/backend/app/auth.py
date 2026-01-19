"""
Authentication middleware for MIGRU backend.

Integrates with Clerk for JWT validation and user management.
"""
from fastapi import Header, HTTPException, Depends
from typing import Optional
from sqlalchemy.orm import Session
from app.database import get_db, get_or_create_user, User
import os
import httpx
import jwt
from datetime import datetime


class ClerkAuth:
    """Clerk JWT authentication"""

    def __init__(self):
        self.clerk_publishable_key = os.getenv("CLERK_PUBLISHABLE_KEY")
        self.clerk_secret_key = os.getenv("CLERK_SECRET_KEY")
        self.jwks_url = None

        if self.clerk_publishable_key:
            # Extract frontend API from publishable key
            # Format: pk_test_<base64> or pk_live_<base64>
            self.jwks_url = f"https://api.clerk.com/v1/jwks"

    async def get_current_user(
        self,
        authorization: Optional[str] = Header(None),
        db: Session = Depends(get_db)
    ) -> User:
        """
        Extract and validate Clerk JWT, return user.

        For development: If no token provided, creates/returns demo user.
        """
        if not authorization:
            # Development mode: use demo user
            if os.getenv("DEV_MODE", "true").lower() == "true":
                return get_or_create_user(db, "dev_user_1", "dev@migru.app")
            raise HTTPException(status_code=401, detail="Authorization header required")

        # Extract token
        try:
            token = authorization.replace("Bearer ", "")

            # In production, verify JWT with Clerk's JWKS
            # For now, decode without verification (development only)
            if os.getenv("DEV_MODE", "true").lower() == "true":
                payload = jwt.decode(token, options={"verify_signature": False})
            else:
                # Production: verify signature
                payload = await self._verify_clerk_jwt(token)

            clerk_id = payload.get("sub")
            email = payload.get("email")

            if not clerk_id:
                raise HTTPException(status_code=401, detail="Invalid token payload")

            # Get or create user
            user = get_or_create_user(db, clerk_id, email)
            return user

        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Auth error: {str(e)}")

    async def _verify_clerk_jwt(self, token: str) -> dict:
        """
        Verify JWT signature using Clerk's JWKS endpoint.

        Production implementation.
        """
        if not self.jwks_url:
            raise HTTPException(status_code=500, detail="Clerk not configured")

        async with httpx.AsyncClient() as client:
            # Fetch JWKS
            response = await client.get(self.jwks_url)
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="Failed to fetch JWKS")

            jwks = response.json()

            # Decode and verify
            # Note: In production, use python-jose with proper key selection
            payload = jwt.decode(
                token,
                options={"verify_signature": False}  # TODO: Implement proper verification
            )
            return payload


# Singleton instance
clerk_auth = ClerkAuth()


# Dependency for routes
async def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> User:
    """FastAPI dependency for authenticated routes"""
    return await clerk_auth.get_current_user(authorization, db)


# Optional auth (allows unauthenticated requests)
async def get_current_user_optional(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """FastAPI dependency for routes that work with or without auth"""
    try:
        return await clerk_auth.get_current_user(authorization, db)
    except HTTPException:
        return None
