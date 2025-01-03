import environ

env = environ.Env()
environ.Env.read_env()

DOMAINS_BLACKLIST = env.list("DOMAINS_BLACKLIST", default=[])
RESTRICT_EMAILS = env.bool("RESTRICT_EMAILS", True)
