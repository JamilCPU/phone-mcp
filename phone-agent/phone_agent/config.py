from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    phone_agent_key: str = ""
    phone_agent_port: int = 8080
    phone_agent_host: str = "0.0.0.0"
    max_shell_timeout: int = 300
    default_shell_timeout: int = 30
    max_file_size_mb: int = 50
    blocked_commands: str = ""
    log_level: str = "INFO"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    @property
    def blocked_command_list(self) -> list[str]:
        if not self.blocked_commands:
            return ["rm -rf /", "reboot", "shutdown", "mkfs", "dd if="]
        return [c.strip() for c in self.blocked_commands.split(",") if c.strip()]


settings = Settings()
