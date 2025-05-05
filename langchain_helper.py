from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import init_chat_model
import os
from groq_keys import GROQ_API_KEY

# Set Groq API key
if not os.environ.get("GROQ_API_KEY"):
    os.environ["GROQ_API_KEY"] = GROQ_API_KEY

# Initialize the language model
llm = init_chat_model("llama-3.3-70b-versatile", model_provider="groq")

# First prompt template for restaurant name
prompt_template_name = ChatPromptTemplate.from_messages(
    [("system", "I want to open a restaurant for {country} food. Just give one fancy name for restaurant only not other details")]
)

# Second prompt template for menu items
prompt_template_menu_items = ChatPromptTemplate.from_messages(
    [("system", "Suggest me some food menu items for {restaurant_name}. Give me comma separated items.")]
)

# Create the first chain to generate restaurant name
name_chain = LLMChain(
    llm=llm,
    prompt=prompt_template_name,
    output_key="restaurant_name"  # This will be used as input for the next chain
)

# Create the second chain to generate menu items
menu_chain = LLMChain(
    llm=llm,
    prompt=prompt_template_menu_items
)


# Create the overall chain that connects both
def generate_restaurant_info(inputs):
    # First get the restaurant name
    name_result = name_chain.invoke(inputs)
    restaurant_name = name_result["restaurant_name"]

    # Then get menu items using the restaurant name
    menu_result = menu_chain.invoke({"restaurant_name": restaurant_name})

    # Return both results
    return {
        "restaurant_name": restaurant_name,
        "menu_items": menu_result["text"]
    }


# Example usage
if __name__ == "__main__":
    # Test just the model directly
    # direct_response = llm.invoke("I want to open a restaurant for pakistani food. Suggest one fancy name for restaurant")
    # print("Direct model test:")
    # print(direct_response.content)
    # print("\n---\n")

    # Test the full chain
    result = generate_restaurant_info({"country": "pakistani"})
    print(f"Restaurant Name: {result['restaurant_name']}")
    print(f"Menu Items: {result['menu_items']}")
