import google.generativeai as genai
import os
import dotenv
import re
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain

def load_environment_variables():
    dotenv.load_dotenv()
    return os.environ.get('GOOGLE_API_KEY')

def configure_genai(api_key):
    genai.configure(api_key=api_key)

def create_llm_chain():
    llm = ChatGoogleGenerativeAI(model="gemini-pro")
    cure_template = PromptTemplate(
        input_variables=['age', 'weight', 'height', 'country', 'disease', 'allergies', 'country', 'state', 'city'],
        # template="Diet recommendation for a {age} year old, {weight} kg, {height} cm tall, living in the area of {country}, state {state} and city {city} with {disease}, and facing allergies to {allergies}. What should be the best 6 best breakfast, lunch, snacks, dinner, workout and the best budget friendly restaurants and tips for them? Keep it short and crisp. Also mention the exact sectors of the restaurants. You don't have to mention the calories of each category ever."
        template = '''
                        Given the following details:
                        - Age: {age} years
                        - Weight: {weight} kg
                        - Height: {height} cm
                        - Country: {country}    
                        - Known health condition(s): {disease}
                        - Known allergies: {allergies}

                        Please provide a comprehensive diet and lifestyle plan that includes:
                        1. A balanced diet plan covering breakfast, lunch, snacks, and dinner, tailored to the individual's health condition(s) and allergies.
                        2. Suggested daily workouts or physical activities suitable for the individual's age, weight, and health condition.
                        3. Practical tips for maintaining a healthy lifestyle, considering the individual's specific health condition(s) and allergies.
                        FORMAT:
                        BREAKFAST: [List of breakfast options]
                        LUNCH: [List of lunch options]
                        SNACKS: [List of snack options]
                        DINNER: [List of dinner options]
                        WORKOUT: [List of workout recommendations]
                        TIPS: [List of lifestyle tips]
                        (keep all the headings capital)
        
                        Ensure the recommendations are concise, actionable, and tailored to the individual's profile and location.
                        '''
            )
    return LLMChain(llm=llm, prompt=cure_template)

def invoke_chain(chain, input_dict):
    res = chain.invoke(input_dict)
    text = str(res['text'])
    cleaned_text = clean_text(text)
    return extract_data(cleaned_text)

def clean_text(text):
    cleaned_text = text.replace('\n', ' ').replace('**', '').replace('*', '').replace('-', '').replace('   ', ' ')
    print(cleaned_text)
    return cleaned_text

def extract_data(cleaned_text):
    patterns = {
        'breakfast': r'BREAKFAST: (.*?) LUNCH:',
        'lunch': r'LUNCH: (.*?) SNACKS:',
        'snacks': r'SNACKS: (.*?) DINNER:',
        'dinner': r'DINNER: (.*?) WORKOUT:',
        'workout': r'WORKOUT: (.*?) TIPS:',
        'tips': r'TIPS: (.*?)$'
    }
    data = {}
    for key, pattern in patterns.items():
        match = re.findall(pattern, cleaned_text)
        if match:
            data[key] = [name.strip() for name in match[0].strip().split('  ') if name.strip()]
        else:
            data[key] = []
    return data


def main(input_dict):
    api_key = load_environment_variables()
    configure_genai(api_key)
    chain = create_llm_chain()

    # TRIAL INPUT
    # input_dict = {
    #             'age': "45",
    #             'weight': "78",
    #             'height': "171",
    #             'country': "India",
    #             'disease': "Diabetes",
    #             'allergies': "Gluten",
    #             'state': "Haryana",
    #             'city': "Hisar",
    #         }
    data = invoke_chain(chain, input_dict)
    output_lines = []
    for key, value in data.items():
        line = f"{key.capitalize()}: {', '.join(value)}"
        output_lines.append(line)
    return '\n'.join(output_lines)

if __name__ == "__main__":
    main()