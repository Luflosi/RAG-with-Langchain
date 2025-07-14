# RAG-Powered Chatbot and Conversational AI System with LangChain & ChromaDB

## Project Overview

A **RAG-Powered Chatbot** built with **LangChain** and **ChromaDB**. It answers questions by retrieving context from the **Nixpkgs Reference Manual** ([https://nixos.org/manual/nixpkgs/stable/](https://nixos.org/manual/nixpkgs/stable/)). Caching is used for faster responses and cost efficiency.

## Key Functionality

* Processes **Nixpkgs Reference Manual** content.
* Engages in **conversational Q&A**, augmented by retrieved knowledge.
* Utilizes **LangChain** for pipeline orchestration.
* Stores data in **ChromaDB** for efficient retrieval.

## Get Started

1.  Clone this repo.
2.  Install dependencies: `pip install -r requirements.txt`
3.  Set `OPENAI_API_KEY` in a `.env` file.
4.  Run `jupyter notebook` and open `RAG.ipynb` to process documentation and start the chatbot.

## Tech Stack

* Python 3.9+
* LangChain
* ChromaDB
* OpenAI API
* Jupyter Notebook