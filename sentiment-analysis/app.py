from chalice import Chalice
from sense_ai import SenseAI
from chaice import Chaice

# Initialize Chalice app
app = Chalice(app_name="sentiment-analysis")

# Initialize Sense AI client (replace with your API key)
sense_ai_client = SenseAI(api_key="your-sense-ai-api-key")

# Define Chaice decision-making workflow
chaice_workflow = Chaice()
chaice_workflow.add_node("start", decision="sentiment_check", children=["positive", "neutral", "negative"])
chaice_workflow.add_node("positive", result="Positive sentiment detected. Take optimistic action.")
chaice_workflow.add_node("neutral", result="Neutral sentiment detected. Proceed cautiously.")
chaice_workflow.add_node("negative", result="Negative sentiment detected. Take corrective action.")

@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    try:
        # Parse the input from the request
        request = app.current_request
        input_data = request.json_body.get("input", "No text provided")

        # Step 1: Analyze sentiment using Sense AI
        sentiment_response = sense_ai_client.analyze_text(input_data)
        sentiment = sentiment_response.get("sentiment", "neutral")  # Possible: positive, neutral, negative

        # Step 2: Make a decision using Chaice based on sentiment
        decision = chaice_workflow.traverse("start", decision=sentiment)

        # Return the result
        return {
            "input_text": input_data,
            "sentiment": sentiment,
            "decision": decision
        }

    except Exception as e:
        return {"error": str(e)}


