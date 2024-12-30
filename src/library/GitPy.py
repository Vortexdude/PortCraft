from src.lib.common import Crafter


def run_module():

    _args = dict(
        action=dict(type="str", required=True),
        repo=dict(type="str", required=True),
        branch=dict(type="str", required=False)
    )

    _result = dict(
        changed=False,
        message="Nothing_special"
    )

    module = Crafter(module_args=_args)
    module.exit(**_result)

if __name__ == "__main__":
    run_module()
