from pydantic import Field

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

# Write a tool to read a doc
@mcp.tool(
    name="read_doc_contents",
    description="Reads the contents of a document and returns it as a string.",
)
def read_document(doc_id: str = Field(description="The ID of the document to read.")) -> str:
    if doc_id not in docs:
        raise ValueError(f"Document with ID '{doc_id}' not found.")
    
    return docs[doc_id]

# Write a tool to edit a doc
@mcp.tool(
    name="edit_doc_contents",
    description="Edits the contents of a document and returns the updated content as a string.",
)
def edit_document(doc_id: str = Field(description="The ID of the document to edit."),
                   new_content: str = Field(description="The new content to replace the existing document content."),
                   old_content: str = Field(description="The old content of the document.")) -> str:
    if doc_id not in docs:
        raise ValueError(f"Document with ID '{doc_id}' not found.")
    
    docs[doc_id] = docs[doc_id].replace(old_content, new_content)

# Write a resource to return all doc id's
@mcp.resource(
    "docs://documents",
    mime_type="application/json",
)
def list_docs() -> list[str]:
    return list(docs.keys())

# Write a resource to return the contents of a particular doc
@mcp.resource(
    "docs://documents/{doc_id}",
    mime_type="text/plain",
)
def get_doc_contents(doc_id: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Document with ID '{doc_id}' not found.")
    
    return docs[doc_id]

# Write a prompt to rewrite a doc in markdown format
@mcp.prompt(
    name="rewrite_doc_markdown",
    description="Rewrites the contents of a document in markdown format.",
)
def format_document(doc_id: str = Field(description="The ID of the document to rewrite.")) -> list[base.Message]:
    if doc_id not in docs:
        raise ValueError(f"Document with ID '{doc_id}' not found.")
    
    prompt = f"""
    Your goal is to rewrite the following document in markdown format. Use appropriate markdown syntax for headings, lists, and other formatting as needed.
    
    The id of the document you need to reformat is:
    <doc_id>
    {doc_id}
    </doc_id>
    
    Add in headers, bullet points, or other markdown formatting as you see fit to make the document more readable. Here is the content of the document:
    """
    
    return [base.UserMessage(prompt)]

# Write a prompt to summarize a doc


if __name__ == "__main__":
    mcp.run(transport="stdio")
