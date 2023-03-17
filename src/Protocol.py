import os
import sys

from Agent import Agent
from Communication import Communication

DEBUG = os.getenv('DEBUG', False)
INFO_TEXT = 'name="gomoku-ai", version="1.0", author="David Gozlan, Lisa Glaziou and Alexandre Calmels", ' \
            'country="France" '
MULTILINE_CMD = {"BOARD": {"end_cmd": "DONE"}}


class Protocol:

    def __init__(self, agent: Agent):
        self.cmds = {"ABOUT": self.cmd_about, "START": self.cmd_start, "TURN": self.cmd_turn, "BEGIN": self.cmd_begin,
                     "BOARD": self.cmd_board, "INFO": self.cmd_info, "END": self.cmd_end, "PRINT": None}
        self.agent = agent
        self.comm = Communication()

    def send_res(self):
        self.comm.pipe_out()
        self.comm.reset_req()

    async def receive_req(self):
        req = await self.comm.pipe_in()
        parsed_req = await self.parse_req(req)
        return parsed_req

    def treat_req(self, key, req_data):
        if key in self.cmds:
            if self.cmds[key]:
                return self.cmds[key](*req_data)
        else:
            if DEBUG:
                print(f"Unknown command : \"{key}\"", file=sys.stderr)

    def cmd_start(self, err, value):
        if err:
            self.comm.append_req("ERROR message - unsupported size or other error")
        else:
            self.comm.append_req("OK - everything is good")

    def cmd_turn(self, err, value):
        if err:
            if DEBUG:
                print("Case already played or board empty", file=sys.stderr)
            return
        if DEBUG:
            self.agent.print_board()
            print(f"Turn : {value[0]},{value[1]}", file=sys.stderr)
        self.comm.append_req(f"{value[0]},{value[1]}")

    def cmd_begin(self, err, value):
        self.cmd_turn(err, value)

    def cmd_board(self, err, value):
        """Update the board"""
        if err:
            if DEBUG:
                print("Board empty or bad parameters", file=sys.stderr)
            return
        self.comm.append_req(f"{value[0]},{value[1]}")

    def cmd_info(self, err, value):
        pass

    def cmd_end(self, err, value):
        pass

    def cmd_about(self, err, value):
        """AI identification (copyright, version)"""
        self.comm.append_req(INFO_TEXT)

    async def parse_multi_line_req(self, key):
        end_cmd = MULTILINE_CMD[key]["end_cmd"]
        data = []
        while True:
            line = await self.comm.pipe_in()
            if line == end_cmd:
                break
            data.append(line)
        return data

    async def parse_req(self, req):
        """Parse the request sent by the server"""
        if DEBUG:
            print(f"Received request : \"{req}\"", file=sys.stderr)
        if not req:
            return "ERROR", "Empty request"
        req = req.split()
        key = req[0]
        if key in MULTILINE_CMD:
            data = await self.parse_multi_line_req(key)
        else:
            data = req[1:]
        return key, data
