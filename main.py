from agent.graph import build_graph


def run(query: str):
    app = build_graph()

    config = {"configurable": {"thread_id": "cli-session-1"}}

    initial_state = {
        "query": query,
        "sources": [],
        "iterations": 0,
    }

    result = app.invoke(initial_state, config=config)
    return result["final_answer"]


if __name__ == "__main__":
    user_query = input("What would you like to research? ")
    print("\nResearching...\n")
    answer = run(user_query)
    print(answer)