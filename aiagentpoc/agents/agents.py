
from aiagentpoc.agents.paco import get_paco

"""
Dictionary to dinamically export all available agents
"""
available_agents = {
    "paco": get_paco,
}