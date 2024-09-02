import streamlit as st
import time
import uuid
from datetime import datetime
from assistant import get_answer
from llm.utils.helpers.db import (save_conversation, save_feedback, get_recent_conversations)

def print_log(message):
    print(message, flush=True)

def main():
    print_log("Starting the Course Assistant application")
    st.set_page_config(layout="wide")
    st.title("SlackAdemic Advisor")

    # Session state initialization
    if 'conversation_id' not in st.session_state:
        st.session_state.conversation_id = str(uuid.uuid4())
        print_log(f"New conversation started with ID: {st.session_state.conversation_id}")
    if 'count' not in st.session_state:
        st.session_state.count = 0
        print_log("Feedback count initialized to 0")

    # Sidebar for course and model selection
    with st.sidebar:
        st.header("Settings")
        course = st.selectbox(
            "Select a course:",
            ["machine-learning-zoomcamp", "data-engineering-zoomcamp", "llm-zoomcamp"]
        )
        model_choice = st.selectbox(
            "Select a model:",
            ["ollama/tinyllama", "openai/gpt-3.5-turbo", "openai/gpt-4o-mini"]
        )
        print_log(f"User selected course: {course} and model: {model_choice}")

    # Main content area
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("Ask a Question")
        user_input = st.text_input("Enter your question:")
        if st.button("Ask"):
            print_log(f"User asked: '{user_input}'")
            with st.spinner('Processing...'):
                print_log(f"Getting answer from assistant using {model_choice} model")
                start_time = time.time()
                answer_data = get_answer(user_input, course, model_choice)
                end_time = time.time()
                print_log(f"Answer received in {end_time - start_time:.2f} seconds")
                
                st.success("Answer:")
                st.write(answer_data['answer'])
                
                with st.expander("Answer Details"):
                    st.write(f"Response time: {answer_data['response_time']:.2f} seconds")
                    st.write(f"Model used: {answer_data['model_used']}")
                    st.write(f"Total tokens: {answer_data['total_tokens']}")
                    if answer_data['openai_cost'] > 0:
                        st.write(f"OpenAI cost: ${answer_data['openai_cost']:.4f}")

                # Save conversation to database
                print_log("Saving conversation to database")
                save_conversation(st.session_state.conversation_id, user_input, answer_data, course)
                print_log("Conversation saved successfully")

                # User feedback section
                st.subheader("Provide Feedback")
                rating = st.slider("Rate the answer (1-5 stars)", 1, 5, 3)
                relevance = st.selectbox("How relevant was the answer?", 
                                        ["Relevant", "Partly Relevant", "Not Relevant"])
                usefulness = st.selectbox("Was this answer useful?", ["Yes", "Somewhat", "No"])
                comments = st.text_area("Additional comments (optional)")
                
                if st.button("Submit Feedback"):
                    feedback_data = {
                        "user_rating": rating,
                        "user_relevance": relevance,
                        "user_usefulness": usefulness,
                        "user_comments": comments
                    }
                    save_feedback(st.session_state.conversation_id, feedback_data)
                    st.success("Thank you for your feedback!")

                # Generate a new conversation ID for next question
                st.session_state.conversation_id = str(uuid.uuid4())

    with col2:
        st.header("Conversation History")
        relevance_filter = st.selectbox(
            "Filter by relevance:", ["All", "RELEVANT", "PARTLY_RELEVANT", "NON_RELEVANT"]
        )
        recent_conversations = get_recent_conversations(
            limit=10, relevance=relevance_filter if relevance_filter != "All" else None
        )
        
        # Create a dataframe for the table
        if recent_conversations:
            data = []
            for conv in recent_conversations:
                data.append({
                    "Timestamp": conv.get('timestamp', datetime.now()).strftime("%Y-%m-%d %H:%M"),
                    "Question": conv['question'][:30] + "..." if len(conv['question']) > 30 else conv['question'],
                    "Answer": conv['answer'][:30] + "..." if len(conv['answer']) > 30 else conv['answer'],
                    "Relevance": conv['relevance'],
                    "Model": conv['model_used']
                })
            
            st.dataframe(data, use_container_width=True)
            
            # Expandable details for each conversation
            for idx, conv in enumerate(recent_conversations):
                with st.expander(f"Conversation {idx + 1}"):
                    st.write(f"**Question:** {conv['question']}")
                    st.write(f"**Answer:** {conv['answer']}")
                    st.write(f"**Relevance:** {conv['relevance']}")
                    st.write(f"**Model:** {conv['model_used']}")
                    st.write(f"**Timestamp:** {conv.get('timestamp', datetime.now()).strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            st.write("No recent conversations found.")

    print_log("Streamlit app loop completed")

if __name__ == "__main__":
    print_log("Course Assistant application started")
    main()