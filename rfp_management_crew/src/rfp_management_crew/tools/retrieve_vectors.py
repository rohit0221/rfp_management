import os
import chromadb
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from crewai.tools import tool

# Load environment variables (ensure OPENAI_API_KEY is set)
load_dotenv()

# ✅ Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_collection(name="rfp_proposals")

# ✅ Initialize LLM and Embeddings
embedding_function = OpenAIEmbeddings()
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

# ✅ Retrieve all unique vendors from metadata
def get_unique_suppliers():
    results = collection.get(include=["metadatas"])
    suppliers = {metadata["supplier"] for metadata in results["metadatas"] if "supplier" in metadata}
    return list(suppliers)

# ✅ Retrieve all proposal chunks for a given supplier using metadata filtering
def retrieve_chunks_for_supplier(supplier_name):
    results = collection.get(
        where={"supplier": supplier_name}, 
        include=["documents"]
    )
    return results["documents"] if results and "documents" in results else []

# ✅ Generate structured output using LLM
def generate_structured_output(supplier_name, documents):
    context = "\n".join(documents)
    
    prompt_template = PromptTemplate(
        input_variables=["supplier", "context"],
        template="""
        Given the following supplier proposal documents for {supplier}, extract and structure the key details:
        
        - **Pricing**
        - **Contract Terms**
        - **Compliance**
        - **Technical Capabilities**
        - **Support & SLAs**
        - **Implementation Timeline**
        - **Past Performance**
        - **Customization & Flexibility**
        
        Provide a clear and structured output in markdown format.
        
        Context:
        {context}
        """
    )
    chain = LLMChain(llm=llm, prompt=prompt_template)
    return chain.run(supplier=supplier_name, context=context)

@tool
def retrieve_relevant_proposals(query: str) -> str:
    """
    Retrieves and structures supplier proposals from ChromaDB, ensuring each supplier's data
    is correctly grouped under subheaders.
    """
    suppliers = get_unique_suppliers()
    final_output = ""  # Store structured outputs
    
    for supplier in suppliers:
        print(f"Processing {supplier}...")
        documents = retrieve_chunks_for_supplier(supplier)
        if not documents:
            print(f"⚠️ No data found for {supplier}, skipping.")
            continue
        structured_data = generate_structured_output(supplier, documents)
        final_output += f"\n## {supplier}\n" + structured_data + "\n\n"
    
    print("✅ Finished processing all vendors.")
    return final_output
