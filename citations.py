#!/usr/bin/env python3
import argparse
from semanticscholar import SemanticScholar


def get_citations_excluding_self(paper):
    paper_author_id_set = set([author["authorId"] for author in paper.authors])
    citations = []

    for citation in paper.citations:
        citation_author_id_set = set(
            [author["authorId"] for author in citation.authors]
        )

        if not paper_author_id_set.intersection(citation_author_id_set):
            citations.append(citation.title)
        else:
            print("Excluding self-citation: ", citation.title)

    return citations


def retrieve_papers_for_author(sch, author_id):
    sch = SemanticScholar()
    author = sch.get_author(author_id)

    return author.papers


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Retrieve citations for an author.")
    parser.add_argument(
        "author_id", type=str, help="The Semantic Scholar author ID (e.g., 1805991958)."
    )
    parser.add_argument(
        "--print-citations",
        action="store_true",
        help="Print all the titles of the citations.",
    )
    args = parser.parse_args()

    sch = SemanticScholar()
    author_papers = retrieve_papers_for_author(sch, args.author_id)

    for paper_info in author_papers:
        paper_id = paper_info["paperId"]
        paper_title = paper_info["title"]
        paper = sch.get_paper(paper_id)

        print("=" * 80)
        print(paper_title)
        print("-" * 80)

        citations_excluding_self = get_citations_excluding_self(paper)

        print("Citations: ", len(paper.citations))
        print("Citations (excluding self-citations): ", len(citations_excluding_self))

        if args.print_citations:
            for citation in citations_excluding_self:
                print(citation)
