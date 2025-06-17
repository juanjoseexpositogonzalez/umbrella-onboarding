from typing import Dict, List

import streamlit as st

from assistant import Assistant


class AssistantGUI:
    """Class to handle the Streamlit GUI for the AI assistant."""

    def __init__(self, assistant: Assistant):
        """Initialize the GUI with an Assistant instance."""
        self.assistant = assistant
        self.messages = assistant.messages
        self.employee_information = assistant.employee_information

    def get_response(self, user_input: str):
        """Get the AI response for the user input."""
        return self.assistant.get_response(user_input)

    def set_state(self, key: str, value: str | List[Dict[str, str]]):
        """Set the state in the Streamlit session."""
        if key not in st.session_state:
            st.session_state[key] = value
        else:
            st.session_state[key] = value

    def render_messages(self):
        """Render the chat messages in the Streamlit app."""
        for message in self.messages:
            if message["role"] == "user":
                st.chat_message("human").markdown(message["content"])
            elif message["role"] == "ai":
                st.chat_message("assistant").markdown(message["content"])
            else:
                st.error(f"Unknown role: {message['role']}")

    def render_user_input(self):
        """Render the user input field and handle message submission."""
        user_input = st.chat_input("Type here...", key="input")

        if user_input and user_input != "":
            st.chat_message("human").markdown(user_input)

            response = self.get_response(user_input)
            st.write(response)  # Display the response directly

            # response_generator = self.get_response(user_input)

            # with st.chat_message("ai"):
            #     response = st.write_stream(response_generator)

            self.messages.append({"role": "user", "content": user_input})
            self.messages.append({"role": "ai", "content": response})  # type: ignore[call-arg]

            self.set_state("messages", self.messages)

    def render(self):
        """Render the Streamlit GUI."""
        with st.sidebar:
            st.logo(
                "https://upload.wikimedia.org/wikipedia/commons/0/0e/Umbrella_Corporation_logo.svg"
            )
            st.title("Umbrella Corporation Assistant")

            st.subheader("Employee Information")
            st.write(self.employee_information)

        self.render_messages()
        self.render_user_input()
