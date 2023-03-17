from Agent import Agent
from .RandomActions import RandomActions
from ..BasePolicy import BasePolicy


class RandomPolicy(BasePolicy):
    def __init__(self, agent: Agent):
        super().__init__(agent)
        self.action = RandomActions(agent)
        self.agent = agent
        self.executed_cmd = 0

    def run_policy(self):
        return self.action.random_move()

