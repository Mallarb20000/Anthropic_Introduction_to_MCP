from mcp.server.fastmcp import FastMCP
from pydantic import Field

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}


@mcp.tool(
    name = "read_doc_contents",
    description = "Read the contents of a document and return it as a string."
)
def read_document(
    doc_id:str = Field(description ="ID of the document to read")
):
    if doc_id not in docs:
        raise ValueError(f"Document with ID '{doc_id}' not found.")
    return docs[doc_id]
    

@mcp.tool(
    name = "edit_document",
    description = "Edit the contents of a document and return the updated content."
)
def edit_document(
    doc_id:str = Field(description ="ID of the document to edit"),
    old_str:str = Field(description ="String to be replaced in the document"),
    new_str:str = Field(description ="New string to replace the old string")
):
    if doc_id not in docs:
        raise ValueError(f"Document with ID '{doc_id}' not found.")
    docs[doc_id]= docs[doc_id].replace(old_str, new_str)
    return docs[doc_id]


#Write a rescouce to return all doc ids
@mcp.resource(
     "docs://documents/",
     mime_type = "application/json"
)

def list_docs() -> list[str]:
    return list(docs.keys())
    

# TODO: Write a resource to return the contents of a particular doc

@mcp.resource(
        "docs://documents/{doc_id}",
        mime_type = "text/plain"
    
)
def fetch_docs(doc_id:str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Document with ID '{doc_id}' not found.")
    
    return docs[doc_id]
    


# TODO: Write a prompt to rewrite a doc in markdown format
# TODO: Write a prompt to summarize a doc


if __name__ == "__main__":
    mcp.run(transport="stdio")
