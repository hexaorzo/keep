import dataclasses

import pydantic
from openai import OpenAI

from keep.contextmanager.contextmanager import ContextManager
from keep.providers.base.base_provider import BaseProvider
from keep.providers.models.provider_config import ProviderConfig


@pydantic.dataclasses.dataclass
class OpenaiProviderAuthConfig:
    api_key: str = dataclasses.field(
        metadata={
            "required": True,
            "description": "OpenAI Platform API Key",
            "sensitive": True,
        },
    )
    organization_id: str | None = dataclasses.field(
        metadata={
            "required": False,
            "description": "OpenAI Platform Organization ID",
            "sensitive": False,
        },
        default=None,
    )


class OpenaiProvider(BaseProvider):
    PROVIDER_DISPLAY_NAME = "OpenAI"

    def __init__(
        self, context_manager: ContextManager, provider_id: str, config: ProviderConfig
    ):
        super().__init__(context_manager, provider_id, config)

    def validate_config(self):
        self.authentication_config = OpenaiProviderAuthConfig(
            **self.config.authentication
        )

    def dispose(self):
        pass

    def validate_scopes(self) -> dict[str, bool | str]:
        scopes = {}
        return scopes

    def _query(self, prompt, model="gpt-3.5-turbo"):
        client = OpenAI(
            api_key=self.authentication_config.api_key,
            organization=self.authentication_config.organization_id,
        )
        response = client.chat.completions.create(
            model=model, messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
