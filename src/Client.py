import sys

from Agent import Agent, DEBUG
from Protocol import Protocol
from Policies import RandomPolicy
from Policies import MinmaxPolicy
from Policies import MinmaxRbPolicy

import os

CURRENT_POLICY = os.getenv('GMK_POLICY', "MinMaxRb")

# TODO : Add a policy manager to load the policy dynamically
POLICIES = {"None": None, "Random": RandomPolicy.RandomPolicy,
            "MinMax": MinmaxPolicy.MinmaxPolicy, "MinMaxRb": MinmaxRbPolicy.MinmaxPolicy}

class Client:

    def __init__(self):
        self.agent = Agent()
        self.protocol = Protocol(self.agent)
        policy = POLICIES[CURRENT_POLICY]
        if policy is None:
            print("No policy selected.", file=sys.stderr)
            exit(1)
        self.policy = policy(self.agent)
        try:
            self.connect_client()
        except Exception as e:
            print("Error while connecting : ", e, file=sys.stderr)
            exit(1)

    def __del__(self):
        pass

    def setup_handshake(self):
        pass

    def connect_client(self):
        self.setup_handshake()
        print("Client connected !", file=sys.stderr)

    def treat_req(self, cmd, data=None):
        err = self.agent.eval_state(cmd, data)
        if self.agent.game_state == self.agent.GameState.MY_TURN:
            if DEBUG:
                print("Agent turns", file=sys.stderr)
            action = self.policy.run_policy()
            self.agent.game_state = self.agent.GameState.NOT_MY_TURN
        else:
            action = None
        self.protocol.treat_req(cmd, (err, action))

    async def loop_client(self):
        async_req = self.protocol.receive_req()
        while True:
            cmd, data = await async_req
            self.treat_req(cmd, data)
            async_req = self.protocol.receive_req()
            self.protocol.send_res()
