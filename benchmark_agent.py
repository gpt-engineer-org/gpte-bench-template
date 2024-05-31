import tempfile
import os
from typing import Optional

from gpt_engineer.core.ai import AI
from gpt_engineer.core.base_execution_env import BaseExecutionEnv
from gpt_engineer.core.base_memory import BaseMemory
from gpt_engineer.core.default.disk_execution_env import DiskExecutionEnv
from gpt_engineer.core.default.disk_memory import DiskMemory
from gpt_engineer.core.default.paths import (
    PREPROMPTS_PATH,
    memory_path,
)
from gpt_engineer.core.prompt import Prompt
from gpt_engineer.core.default.steps import improve_fn as improve
from gpt_engineer.core.files_dict import FilesDict
from gpt_engineer.core.preprompts_holder import PrepromptsHolder


# THIS METHOD IS USED BY "bench" TO SET UP THE AGENT AND MUST BE IMPLEMENTED.
# THE ONLY OTHER REQUIREMENT IS THAT THE AGENT IMPLEMENTS "improve".
def default_config_agent():
    """
    Creates an instance of BenchmarkAgent with default configuration.

    Returns
    -------
    BenchmarkAgent
    """
    return BenchmarkAgent.with_default_config(tempfile.mkdtemp())


class BenchmarkAgent:
    """
    A template agent for BenchmarkAgents. The only method that MUST BE IMPLEMENTED to run "bench" is "improve".
    The below implementation uses the standard improve in gpt-engineer.

    Attributes
    ----------
    memory : BaseMemory
        The memory interface where the code and related data are stored.
    execution_env : BaseExecutionEnv
        The execution environment in which the code is executed.
    ai : AI
        The AI model used for generating and improving code.
    preprompts_holder : PrepromptsHolder
        The holder for preprompt messages that guide the AI model.
    """

    def __init__(
        self,
        memory: BaseMemory,
        execution_env: BaseExecutionEnv,
        ai: AI = None,
        preprompts_holder: PrepromptsHolder = None,
    ):
        self.preprompts_holder = preprompts_holder or PrepromptsHolder(PREPROMPTS_PATH)
        self.memory = memory
        self.execution_env = execution_env
        self.ai = ai or AI(
            model_name=os.environ.get("MODEL_NAME", "gpt-4-turbo"),
        )

    @classmethod
    def with_default_config(
        cls, path: str, ai: AI = None, preprompts_holder: PrepromptsHolder = None
    ):
        """
        Convenience method to create a BenchmarkAgent with default configuration.
        :param path:
        :param ai:
        :param preprompts_holder:
        :return: BenchmarkAgent
        """
        return cls(
            memory=DiskMemory(memory_path(path)),
            execution_env=DiskExecutionEnv(),
            ai=ai,
            preprompts_holder=preprompts_holder or PrepromptsHolder(PREPROMPTS_PATH),
        )

    def improve(
        self,
        files_dict: FilesDict,
        prompt: Prompt,
        execution_command: Optional[str] = None,
    ) -> FilesDict:
        """
        A required function that existing code, a prompt and optionally a command for executing the code (used for self-heal).
        :param files_dict:
        :param prompt:
        :param execution_command:
        :return: FilesDict
        """
        files_dict = improve(
            self.ai, prompt, files_dict, self.memory, self.preprompts_holder
        )

        return files_dict
