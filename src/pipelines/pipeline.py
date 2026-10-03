from src.agents.agents import search_agent, reader_agent, writer_chain, critic_chain
from src.tools.tools import *
import os
from langchain_core.messages import ToolMessage,AIMessage
from pydantic import BaseModel,Field

MAX_OUTER_ATTEMPTS = 3   # maximum number of different sources
MAX_INNER_ATTEMPTS = 3   # maximum writer/critic attempts on the same source

def research_pipeline(topic: str) -> dict:
    state = {}
    state["rejected_urls"] = []

    for outer_attempt in range(1, MAX_OUTER_ATTEMPTS + 1):
        print("\n" + "#" * 50)
        print(f"OUTER ATTEMPT {outer_attempt}/{MAX_OUTER_ATTEMPTS}")
        print("#" * 50)

        # step 1 - search agent
        print("\n" + "=" * 50)
        print("Search agent is working...")
        print("=" * 50)

        search_agt = search_agent()
        result = search_agt.invoke({"messages": [("user",f"Find recent and reliable information on the topic: {topic}")]})

        tool_msg = "\n".join([m.content for m in result["messages"] if isinstance(m, ToolMessage)])
        state["search_result"] = tool_msg

        print("\nSearch result:\n", state["search_result"])

        # step 2 - reader agent
        print("\n" + "=" * 50)
        print("Step 2 - Reader agent is scraping top resources...")
        print("=" * 50)

        rejected_note = ""
        if state["rejected_urls"]:
            rejected_note = (
                "\n\nDo NOT use these previously rejected URLs:\n"
                + "\n".join(state["rejected_urls"]))

        reader_agt = reader_agent()

        reader_result = reader_agt.invoke(
        {"messages": [("user",f"""Based on the following search results about '{topic}', 
        pick the most relevant and credible URL(s) and scrape it for deeper content.

        {rejected_note}

        Search Results:
        {state["search_result"][:800]}""")]})

        reader_output = reader_result["structured_response"]

        state["picked_urls"] = reader_output.picked_urls
        state["scraped_content"] = reader_output.scraped_content

        print("\nPicked URLs list: ",state["picked_urls"])
        print("\nScrapped Content: ",state["scraped_content"])

        # step 3 - Writer chain 
        score = 0
        inner_attempt = 0
        source_problem = False
        state["feedback"] = "No feedback yet — this is the first draft."

        while score < 7 and inner_attempt < MAX_INNER_ATTEMPTS:
            inner_attempt += 1
            print("\n" + "=" * 50)
            print(
                f"Inner attempt "
                f"{inner_attempt}/{MAX_INNER_ATTEMPTS}")
            print("=" * 50)

            print("\nStep 3 - Writer is drafting the report...")
            print("=" * 50)

            research_combined = (
                f"SEARCH RESULTS:\n{state['search_result']}\n\n"
                f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}\n\n"
                f"FEEDBACK:\n{state['feedback']}"
            )

            state["report"] = writer_chain.invoke({
                "topic": topic,
                "research": research_combined})

            print("\nReport:\n", state["report"])

            print("\nStep 4 - Critic is reviewing the report...")
            print("=" * 50)

            feedback = critic_chain.invoke({"report": state["report"]})

            score = feedback["score"]

            state["feedback"] = (
                f"Score: {feedback['score']}/10\n"
                f"Strengths: {feedback['strengths']}\n"
                f"Areas to Improve: {feedback['areas_to_improve']}\n"
                f"Verdict: {feedback['verdict']}"
            )

            print("\nCritic report:\n", state["feedback"])

            source_problem = (feedback["needs_new_source"] or feedback["source_credibility_concern"])

            if source_problem:
                print("\nCritic rejected the current source.")
                break

        if score >= 7 and not source_problem:
            print(
                f"\nAccepted report after "
                f"outer attempt {outer_attempt}, "
                f"inner attempt {inner_attempt}.")
            break

        print("\nCurrent source did not produce a sufficient report.")

        state["rejected_urls"].extend(state["picked_urls"])
        print("\nRejected URLs:",state["rejected_urls"])
    else:
        print(
            f"\nExhausted all {MAX_OUTER_ATTEMPTS} "
            f"outer attempts.")

    print("\nFinal Report:\n", state["report"])
    return state
