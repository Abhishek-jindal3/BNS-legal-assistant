import re
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import PDF_PATH, CHUNK_SIZE, CHUNK_OVERLAP


def load_bns_sections():

    # Load PDF
    loader = PyPDFLoader(PDF_PATH)
    docs = loader.load()

    # Combine all pages
    full_text = "\n".join(
        page.page_content
        for page in docs
    )

    # Find BNS section headings
    pattern = r"(?m)^\s*(\d{1,3})\.\s*(?=[A-Z(“])"

    matches = list(
        re.finditer(pattern, full_text)
    )

    # Keep first occurrence of each section
    valid_matches = []
    seen = set()

    for match in matches:

        section_no = int(
            match.group(1)
        )

        if section_no not in seen:

            valid_matches.append(match)
            seen.add(section_no)

    # Create one Document for each BNS section
    sections = []

    for index in range(len(valid_matches)):

        start_pos = valid_matches[index].start()

        if index + 1 < len(valid_matches):

            end_pos = valid_matches[index + 1].start()

        else:

            end_pos = len(full_text)

        section_text = full_text[
            start_pos:end_pos
        ].strip()

        section_no = int(
            valid_matches[index].group(1)
        )

        sections.append(
            Document(
                page_content=section_text,
                metadata={
                    "source": "BNS_2023.pdf",
                    "section": section_no
                }
            )
        )

    return sections


def create_chunks(sections):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=[
            "\n\n",
            "\n",
            " ",
            ""
        ]
    )

    final_chunks = []

    for section in sections:

        # Keep small sections intact
        if len(section.page_content) <= CHUNK_SIZE:

            final_chunks.append(section)

        else:

            # Split only large sections
            chunks = splitter.split_documents(
                [section]
            )

            final_chunks.extend(chunks)

    return final_chunks


def load_and_chunk_bns():

    sections = load_bns_sections()

    chunks = create_chunks(sections)

    return chunks