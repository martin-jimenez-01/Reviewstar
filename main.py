import time
import openai
import pandas as pd
import csv

# Set the API key
openai.api_key = "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"

#initialize the variable that will hold all responses
allResponses = ""

#initialize the variable that will hold the response number
responseNum = 0

# Define the function to get a response from GPT-3
def generate_response(prompt):
    completions = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.9,
    )

    message = completions.choices[0].text
    return message

with open('cities.csv', 'r') as file:
    csv_reader = csv.reader(file)
    for line in csv_reader:
        city = ','.join(line)
        print(city)
        # Read the .csv file
        df = pd.read_csv(city + "-reviews.csv")

        # Create a new csv file named "output.csv"
        with open("output.csv", "w", newline="") as f:
            writer = csv.writer(f)
    
            # Iterate over the rows
            for index, row in df.iterrows():
                # Iterate over the columns
                for column in df.columns:
                    # Get the cell value
                    user_input = df.at[index, column]

                    # Check if the cell is empty
                    if pd.isna(user_input):
                        # If the cell is empty, move on to the next column
                        continue

                    user_input = user_input.replace("\"", "")
                    user_input = user_input.replace("\n", "")
                    # Get the response from GPT-3
                    prompt = user_input + "(Summarize the negative reviews of American Airlines while replacing the positive ones with ""Positive"" in one short sentence while maintaining its main point and removing any redundant or unnecessary information. Ignore the lines that only contain the text more or less.)"
                    response = generate_response(prompt)
                    
                    response = response.replace("\"", "")
                    response = response.replace("\n", "")
                    response = response.strip()

                    allResponses += str(responseNum) + " " + response + " "
                    responseNum += 1
          
                    time.sleep(.4)
          
                    # Write the response to the csv file
                    if(len(response) > 5):
                        print(response)
                        writer.writerow([response])

        print(allResponses)

        finalResponse = ""

        #finalResponse = generate_response(allResponses + "(In a few words, what is the first main concern of the reviewers? What is the second main concern? What is the third main concern?)")

        finalResponse = generate_response(allResponses + "(In BULLET points, write the top 8 main concerns of these reviews. THIS MUST BE DONE IN BULLET POINTS OR IT IS A FAILURE. Only account for the negative reviews. BULLET POINTS NECESSARY)")

        print("\n\n\n\n\n\nDONE\n\n\n\n\n\n")
        with open(city + "-summary.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([finalResponse])

        allResponses = ""
        responseNum = 0


#finalResponse = generate_response(allResponses + "(Give a short summary of the top 8 problems that originate from these reviews. Group these reviews based on what the customer is complaining about. These are the 8 groups, Delayed/Canceled Flights, Poor Customer Service, Uncomfortable Seats, Dirty Planes, Lost/Delayed Luggage, Too Expensive, Long wait times and Baggage Fees. . Then rank these 8 groups on how common each type of complaint appeared in a list 1-8 and output the number of each review next to the group. The list can change based on types of reviews")

#finalResponse = generate_response(allResponses + "(Give a short summary of the top 8 negative problems that originate from these reviews, and classify them into groups. *MANDATORY* Place the negative reviews that classify under each group. Then rank these 8 groups on how common each type of complaint appeared in a list 1-8)")

#finalResponse = generate_response(allResponses + "(Summarize the top 8 most commonly mentioned issues in negative sounding reviews of American Airlines with a MAXIMUM of 8 words per each of the 8 ranked issues. Output each of the issues in a ranked list from 1-8 vertically)")