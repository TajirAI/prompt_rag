import os
import openai
import streamlit as st
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationSummaryBufferMemory
from langchain_core.prompts.prompt import PromptTemplate
import json

# Set page config
st.set_page_config(page_title="Chatbot", page_icon="💬")

# Display the title and description
st.title("DigitEarn")

# Set GPT API key
GPT_API_KEY = st.secrets["api"]["key"]  # or st.secrets.api.key

# Configure LLM
def configure_llm():
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.5, streaming=True, openai_api_key=GPT_API_KEY)
    return llm

# Load JSON data from file
with open('form_data.json', 'r') as f:
    data = json.load(f)

# Store JSON data in variables
name = data['name']
role = data['role']
location = data['location']
language = data['language']
support_number = data['support_number']
communication_style = data['communication_style']
primary_objectives = data['primary_objectives']
platform_keypoints = data['platform_keypoints']
response_guidelines = data['response_guidelines']

# Create chatbot class
class EnhancedChatbot:
    def __init__(self):
        self.llm = configure_llm()
        template = f"""
        *Name*:  {name}
        *Role*: {role}
        *Location*: {location}  
        *Language*: {language}
        *Communication Style*: {communication_style}
        *Support team contact number*: {support_number}
                    
        ### Platform Key Points:

        {platform_keypoints}

        ## Primary Objectives:
        {primary_objectives}

        ## Response Guidelines:
        {response_guidelines}

        ## Conversation Flow:
        {{history}}
    
        ## Current Interaction:
        User: {{input}}
        DigitEarn Guide: [Respond naturally in Romanized Urdu]
        """
        self.PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)
        self.memory = ConversationSummaryBufferMemory(llm=self.llm, max_token_limit=25, human_prefix="Client", verbose=False)  # Memory will store full conversation history

    def setup_chain(self):
        # Define a prompt template for the conversation chain
        chain = ConversationChain(llm=self.llm, prompt=self.PROMPT, memory=self.memory, verbose=True)
        return chain

    def main(self):
        # Initialize session state for memory
        if "memory" not in st.session_state:
            st.session_state["memory"] = self.memory  # or some initial value

        # Initialize session state for messages
        if "messages" not in st.session_state:
            st.session_state["messages"] = []

        chain = ConversationChain(llm=self.llm, prompt=self.PROMPT, memory=st.session_state["memory"], verbose=True)  # Assuming you have a function setup_chain() to initialize your chain

        # Display previous chat messages
        for msg in st.session_state["messages"]:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        # Chat input
        user_query = st.chat_input(placeholder="Ask me anything!")
        if user_query:
            # Append user query to session state messages
            st.session_state["messages"].append({"role": "user", "content": user_query})

            # Display the current user query
            with st.chat_message("user"):
                st.write(user_query)

            # Run the query through the chain and retrieve the response
            result = chain.invoke(input=user_query)
            response = result["response"]

            # Append assistant response to session state messages
            st.session_state["messages"].append({"role": "assistant", "content": response})
            print(st.session_state["messages"])
            # Display the assistant response
            with st.chat_message("assistant"):
                st.write(response)

# Run chatbot
if __name__ == "__main__":
    # Handle query params
    query_params = st.query_params
    if "page" in query_params and query_params["page"] == "prompt":
        from form_page import form_page
        form_page()  # form_page no longer calls set_page_config
    else:
        obj = EnhancedChatbot()
        obj.main()
