from py2neo import Graph, Node

graph = Graph("bolt://localhost:7687", auth=("neo4j", "admin123"))

def search_neo4j(query):
    results = []

    state, year, field = extract_query_parameters(query)
    print(state, year, field)

    if not field:
        return [{"text": "I'm sorry, I couldn't understand your query. Please ask about tax rates, income, deductions, etc.", 
                 "document_index": "neo4j_result", "score": 0.0}]

    if not year:
        latest_year_query = graph.run("MATCH (t:TaxRecord) RETURN MAX(t.tax_year) AS latest_year").data()
        year = latest_year_query[0]["latest_year"] if latest_year_query else "Unknown"

    if not state:
        return [{"text": "Please specify a state in your query.", "document_index": "neo4j_result", "score": 0.0}]

    query_str = f"""
    MATCH (t:TaxRecord) 
    WHERE t.tax_year = {year} AND t.state = '{state}'
    RETURN t.{field} AS result
    """
    query_result = graph.run(query_str).data()

    if query_result and query_result[0]["result"] is not None:
        response_text = f"{field.replace('_', ' ').capitalize()} in {state} for {year}: {query_result[0]['result']}"
        results.append({"text": response_text, "document_index": "neo4j_result", "score": 1.0})  # ✅ Add a score
    else:
        results.append({"text": f"No data found for {field} in {state} for {year}.", "document_index": "neo4j_result", "score": 0.0})

    return results

def extract_query_parameters(query):
    words = query.split()
    state, year, field = None, None, None

    field_mapping = {
        "tax rate": "tax_rate",
        "income": "income",
        "deductions": "deductions",
        "taxable income": "taxable_income",
        "tax owed": "tax_owed"
    }

    for word in words:
        if word.isdigit() and len(word) == 4:
            year = word
        elif word in ["CA", "TX", "NY", "FL"]:  # TODO: Extend for more states
            state = word

    for key in field_mapping.keys():
        if key in query.lower():
            field = field_mapping[key]
            break

    return state, year, field