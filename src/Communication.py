import sys


class Communication:
    def __init__(self):
        self.req = ""

    def append_req(self, req):
        self.req += req

    def reset_req(self):
        self.req = ""

    @staticmethod
    async def pipe_in():
        return sys.stdin.readline().strip()

    def pipe_out(self):
        if not self.req:
            print("No request sent", file=sys.stderr)
            return
        print(self.req, file=sys.stdout, flush=True)
