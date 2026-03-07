"""Command-line argument parsing for L4D2 Archipelago Companion.
"""
from pydantic import BaseModel, Field


class CommandLineArgs(BaseModel):
    """Parsed command line arguments."""

    slot_name: str = Field(default="", description="Player slot name")
    server_address: str = Field(default="", description="Server address")
    password: str = Field(default="", description="Server password")

    @classmethod
    def from_sys_argv(cls, args: list[str]) -> "CommandLineArgs":
        """Parse arguments from sys.argv.

        Args:
            args: sys.argv list

        Returns:
            Parsed command line arguments
        """
        return cls(
            slot_name=args[1] if len(args) > 1 else "",
            server_address=args[2] if len(args) > 2 else "",
            password=args[3] if len(args) > 3 else "",
        )

    def is_valid(self) -> tuple[bool, str]:
        """Validate that required arguments are present.

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self.slot_name:
            return False, "Slot name is required (first argument)"
        if not self.server_address:
            return False, "Server address is required (second argument)"
        return True, ""


def parse_command_line_args(args: list[str]) -> CommandLineArgs:
    """Parse command line arguments using Pydantic model.

    Args:
        args: Command line arguments (sys.argv)

    Returns:
        CommandLineArgs model with parsed values
    """
    return CommandLineArgs.from_sys_argv(args)
