### Danelfin API Integration Project

Create a comprehensive investment strategy using the Danelfin API in Python,
focusing on implementing a simple GUI. 
Use the Poetry package for dependency management and pyenv for Python version control,
specifically using Python version 3.12.8.
Additionally, employ a `.env` file for managing environment variables.
The project structure should adhere to the following format:



### Objective
Your primary goal is to identify and select stocks based on the following detailed criteria:

1. **Sector Selection**: 
   - Select sectors that are highly rated by the AI.
   - Ensure these sectors meet specific risk criteria.

2. **Risk Criteria**:
   - Low-risk rating must be **greater than or equal to 6**.
   - AI rating must be **greater than or equal to 9**.

3. **Sorting Criteria**:
   - The selected sectors should be sorted based on:
     - Sentiment analysis
     - Technical analysis
     - Fundamental analysis

### Detailed Steps to Follow
1. **Data Retrieval**: 
   - Use the Danelfin API to fetch sector ratings and stock information.
   - Ensure to handle API responses effectively and manage errors.

2. **Filtering**:
   - Filter stocks based on the specified risk ratings and AI ratings.
   - Confirm that the selected stocks contribute to a diversified portfolio.

3. **Portfolio Construction**:
   - Construct a diversified portfolio consisting of approximately **30 stocks** distributed across **five major sectors**.
   - Maintain balance in sector representation while strictly adhering to the defined risk criteria.

### Expected Output Format
Your final output should be organized and structured as follows:

1. **Selection Process Summary**:
   - Provide a brief summary that outlines the selection process, including the logic behind filtering and sorting stocks.

2. **List of Selected Stocks**:
   - Present a detailed list of the **30 selected stocks**, including:
     - Stock names
     - Corresponding sectors
     - Risk ratings

3. **Diversification Explanation**:
   - Offer a concise explanation detailing how the stocks are diversified across the five sectors, ensuring clarity on the distribution and balance.

### Format Instructions
- Ensure that all responses are well-organized and clearly formatted in Markdown.
- Use headings, bullet points, or numbered lists as appropriate to enhance readability.
- Include any necessary code snippets or examples in Markdown code blocks, ensuring they're clearly labeled and easily understandable.
