# AI Agents POC
A simple set of AI agents examples using the Phidata Python Framework served in a Django web server.

# Table of Contents

- [About the project](#about-the-project)
- [Agent Examples](#agent-examples)
- [Run the project on your machine](#run-the-project-on-your-machine)
- [Author](#author)
- [License](#license)

# About the project
This is a quick and simple personal project that was built to experiment with Agentic AI. The Phidata framework was chosen to build quick simple AI agents and explore key features like memory usage, persistance, external conections and RAG tecnologies.

# Agent Examples

## Paco
A simple selling agent for an optic center. It answers questions about the available products which are queried in real time from an external API. Aditionally it understands when the client wants to end the conversation, or talk to a human agent, so it can be easyly integrated in a existing chatbot aplication through the REST API.

The agent has memory implemented in order for the agent to recall information from previous prompts. It uses a inmemory SQLite database for this purpose.

## Weby
A simple web scraping agent that is able to anwswer questions about any web page.

⚠️ **Disclaimer:** Its scraping capabilities are limmited by Phidata Framework, for example it cannot retrieve information from social networks due to the restrictions they have on web crawling.

The agent has a knowledge base to store the information that is scraped from the websites, and is later queried depending on the user´s prompt in a ver agentic manner. It uses a postgres as a vector database for this purpose.

---

> 🤖 **Coming Soon:** More agent examples will be added in the future

# Run the project on your machine
As a prerequisite you need to have Node JS installed on your computer, and Metamask installed on your browser.

Install dependencies
```shell
npm i
```

# Author

[__Mateo Devia__](https://github.com/mateodevia) -> [__Check out my personal web page!__](https:mateodevia.com)

# License
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository has the standard MIT license. You can find it [here.](https://github.com/mateodevia/homePage/blob/master/LICENSE)
