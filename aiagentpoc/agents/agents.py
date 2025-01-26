from aiagentpoc.agents.paco import get_paco
from aiagentpoc.agents.weby import get_weby

"""
Dictionary to dinamically export all available agents
"""
available_agents = {
    "paco": get_paco,
    "weby": get_weby,
}