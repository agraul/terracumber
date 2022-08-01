from fabric import Connection

def run_unit():
    Connection("root:linux@salt-test-node.tf.local") .run(
        "cd salt_repo && nox --session 'pytest-3(coverage=False)' -- tests/pytests/unit"
    )

def run_setup():
    Connection("root:linux@salt-test-node.tf.local") .run(
        "[ ! -e salt_repo ] && git clone https://github.com/opensuse/salt salt_repo || true"
    )
