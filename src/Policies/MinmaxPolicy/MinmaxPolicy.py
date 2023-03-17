from Agent import Agent
from .MinmaxActions import MinmaxActions
from ..BasePolicy import BasePolicy


class MinmaxPolicy(BasePolicy):
    def __init__(self, agent: Agent):
        super().__init__(agent)
        self.action = MinmaxActions(agent)
        self.agent = agent
        self.executed_cmd = 0

    def run_policy(self):
        return self.action.gestion()

