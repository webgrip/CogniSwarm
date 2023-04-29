# Cross-Network Agent Protocol (cNAP)

Individual agents with local permissions want to be able to coordinate arbitrary 
tasks across the network. If I want to plan a coffee meeting with someone, that 
involves access to my calendar, my favorite places, etc.

Inspired by Generative Agents. Like agents, but across the network.

## What We Are Building

- [] Self-owned Agent (SOA) (linked to domain e.g.)
  - [] SOA exposes it's tools (like 'ToolName: Calendar ToolEffect:Schedule Something On My Calendar') 
  - [] SOA exposes a task runner interface (like 'Run: <ToolName> Task UUID: <Sent b>')
  - [] SOA exposes a task listener interface
  - [] SOA has a task list, queue, whatever where it orchestrates it's own plans/motivations

### Task Running

Agent 1:
Sends task run request to **agent2/run**

```json
{
  "Run": {
    ToolName: Schedule a Meeting,
    TaskId: UUID,
    Payload: Tool Input (like I have these days/times available)
  }
}
```

Agent 2:

1. Recieves task run request and responds with some status code (200). This status signals that Agent2 is working and Agent1 can expect a response
2. Run tool asynchronously
3. Return result based on TaskId to **agent1/listen/{id}**