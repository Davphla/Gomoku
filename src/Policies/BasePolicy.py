from abc import ABC, abstractmethod

from Agent import Agent


class BasePolicy(ABC):
    MAX_CMD = 15

    def __init__(self, agent: Agent):
        self.agent = agent
        self.executed_cmd = 0

    def __del__(self):
        pass

    def run_interval(self):
        if self.executed_cmd > self.MAX_CMD:
            return
        self.executed_cmd += 1

    @abstractmethod
    def run_policy(self):
        pass
