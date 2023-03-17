from .BasePolicy import BasePolicy


def main_ai(policy: BasePolicy):
    """
    This function is called by the main function to run the policy.
    """
    policy.run_policy()
    policy.run_interval()
