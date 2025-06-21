from LAM.default.agents.comm_agent.src.interfaces.com_agent_interface import ComAgent
from LAM.default.agents.codex_agent.src.codex_agent.core import Core

# инициализируем два объекта
comm = ComAgent()
codex = Core()

# регистрируем Codex в реестре Communication-агента
comm.register_agent("codex", codex)

# Codex отправляет "ping" через ComAgent
comm.send_data("codex", {"msg": "ping"})

# Communication-агент читает сообщение
agent_name, data = comm.receive_data()
print(f"CommAgent получил от {agent_name}: {data}")

# Ответ Codex-агента
reply = codex.answer(data["msg"])
print(f"Codex ответил: {reply}")
