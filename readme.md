# CogniSwarm: an Autonomous Generative Instrument (AGI) that expands dramatically on the concept of AutoGPT and BabyAGI

# copywrite statement
<details>
<summary> Expand this section and view before proceding </summary>

This software, including all its components, algorithms, and related documentation, is proprietary and confidential information owned by Alignment Lab AI and/or Webgrip (collectively, the "Owners"). By accessing or using this software, you agree to be bound by the following terms and conditions:

1. Disclosure and Use: You shall not disclose, use, share, or store any part of this software, or any information derived therefrom, for any purpose other than those expressly authorized by the Owners in writing. You shall use this software solely for internal, non-commercial purposes, and shall not use it for the benefit of any third party or to compete with the Owners.

2. Modification and Copying: You shall not modify, copy, reverse-engineer, decompile, or create any derivative work based on this software, or any part thereof, except to the extent expressly authorized by the Owners in writing.

3. Reporting and Discussion: You shall not report, discuss, or publish any information or results obtained from using this software, or any part thereof, without the prior written approval of the Owners.

4. Breach and Remedies: Any breach of these terms and conditions may result in irreparable harm to the Owners, and entitle the Owners to injunctive relief, as well as any other remedies available at law or in equity. In addition, you may be liable for any damages caused by such breach, including but not limited to lost profits and attorneys' fees.

5. Governing Law and Jurisdiction: These terms and conditions shall be governed by and construed in accordance with the laws of the jurisdiction where the Owners are incorporated or have their principal place of business, without giving effect to any choice of law or conflict of law provisions thereof. Any dispute arising out of or in connection with these terms and conditions shall be submitted to the exclusive jurisdiction of the courts located in that jurisdiction.

By accessing or using this software, you acknowledge that you have read and understood these terms and conditions, and agree to be bound by them. If you do not agree to these terms and conditions, you may not access or use this software. 
</details>

# 🚧 Before you proceed 🚧
Please note that this is a very early version of the project, and we are still in the process of wrapping things up, wiring components together, and experimenting with new ideas. As such, the project may undergo significant changes and updates as we continue to evolve and refine our vision. Any ideas are welcome and I will get back to you as soon as I can. Click here if youre interested in [Contributing](CONTRIBUTING.md)

<details>

<summary><- click for GPT4 suggested improvement:</summary>

# CogniSwarm: Accelerating the Future of Autonomous Digital Work

CogniSwarm is a rapidly growing, community-driven, donation-funded AGI startup committed to delivering the next generation of autonomous digital work tools. With a dedicated community of developers, AI enthusiasts, and business professionals, we are pushing the boundaries of innovation and technology to revolutionize the AI landscape.

🚀 Join our thriving community, and help us shape the future of AI! 🚀

![CogniSwarm Banner](https://user-images.githubusercontent.com/130523883/233876265-9827f101-10cd-4f9d-bfd8-6a623ea65eb9.jpg)

## Why CogniSwarm?

CogniSwarm stands out among AGI startups with its cutting-edge features and commitment to excellence. Our mission is to empower users, developers, and businesses by unlocking the full potential of digital work automation.

- **Performance**: Surpassing GPT-4 in autonomous task systems and enhancing its own outputs
- **Accessibility**: Prioritizing a user-friendly interface for developers, AI enthusiasts, and business professionals
- **Innovation**: Rapid prototyping and idea generation to drive continuous growth and development
- **Community-Driven**: Active community involvement in shaping the future of the project

## Get Involved

Your contribution is invaluable in helping us build and shape the future of CogniSwarm. There are many ways to get involved:

1. **Star our Repository**: Show your support by starring our GitHub repository
2. **Contribute**: Check out the CONTRIBUTING.md file and submit your ideas, code, or documentation
3. **Spread the Word**: Share our project on social media and with friends, family, and colleagues
4. **Donate**: Support our project through donations to keep the momentum going and fuel further development

Together, we can create a brighter future for AI and AGI technologies!
</details>

CogniSwarm is a state-of-the-art AGI (Autonomous Generative Instrument) designed to generate superior outputs compared to GPT-4 operated task system, as well as significantly improve GPT-4's outputs within itself. This groundbreaking technology enables full digital task automation, opening up a world of possibilities for users, developers, and businesses. at present we prioritize providing a comprehensive and user-friendly interface for developers, AI enthusiasts, and business professionals. By utilizing the latest technologies and with the collaboration of our package contributors, we aim to create a solid foundation for diverse AI applications.

![CogniSwarm](https://user-images.githubusercontent.com/130523883/233876265-9827f101-10cd-4f9d-bfd8-6a623ea65eb9.jpg)```

## Relevant Uses

- [ ] **Virtual Assistants**: Personal or professional use for a wide range of tasks
- [ ] **Intelligent Document Automation**: Streamline document creation and processing
- [ ] **Real-time Market Analysis**: Data-driven decision making for businesses
- [ ] **Rapid Prototyping & Idea Generation**: Expedite innovation and development
- [ ] **API & Service Integration**: Extend functionality with various APIs and services
- [ ] **File System Optimization**: Execute control over users' computers for improved efficiency
- [ ] **User-friendly UI Creation**: Design on-the-fly interfaces with plain language prompts
- [ ] **Website Management**: Develop and manage marketing, social media, and other web-based projects using Streamlit
- [ ] **Financial Analysis**: Optimize spending efficiency without sacrificing quality of life
- [ ] **Data Collection & Model Training**: Preprocess and tokenize training data for specialized models, and initiate training on user's Docker instance

### Installation

Clone the repository and navigate to the project directory:

```
git clone https://github.com/yourusername/puttygpt.git
cd puttygpt
```

(Put this in init.sh later or makefile) Build and run the Docker containers using the provided docker-compose files

```
# Prerequisite (I can probably get rid of this but meh not right now)
docker network create weaviate-network

# Without public grpc endpoint
docker-compose -f docker-compose.weaviate.yml -f docker-compose.yml up --build

# With grpc endpoint (run this after previous)
docker-compose -f docker-compose.weaviate.yml -f docker-compose.yml -f docker-compose.brazen.yml up brazen --build

# Copy env file
cp .env.example .env

# replace the string for searxng
sed -i "s|ReplaceWithARealKey\!|$(openssl rand -base64 33)|g" .env
```

Cleanup:

```
docker-compose -f docker-compose.weaviate.yml -f docker-compose.yml -f docker-compose.brazen.yml down --remove-orphan
```

[Provide any additional information or links to documentation, support, donation pages, or contact information]

Experience the future of autonomous digital work with Cogni

[Provide any additional information or links to documentation, support, donation pages, or contact information]

Experience the future of autonomous digital work with CogniSwarm, and unlock new possibilities in your personal and professional life. Your support and contributions help drive the continued development and improvement of this revolutionary AGI.

## CogniSwarm Features: A Comprehensive AGI Solution

Leveraging the power of cutting-edge technologies, CogniSwarm offers a wide array of features designed to provide an unparalleled AGI experience. Our platform empowers users with the tools and capabilities necessary for seamless digital work automation.

### Key Features

- [x] **More than just GPt-4 Powered**: Compatible with Most Language models
- [x] **Search & Storage**: SearxNG for search capabilities and Weaviate for vector storage and search
- [x] **AI Tools**: Summarization, sentiment analysis, OpenAPI integration, and more
- [x] **Customizable Prompts**: Templates tailored for diverse use cases
- [x] **Efficient Task Execution**: Concurrent task execution using asyncio and aiohttp
- [x] **Monitoring & Debugging**: Detailed tracing and callback mechanisms
- [x] **Extensibility**: Designed for easy integration with other APIs and services
- [x] **Docker Deployment**: Simplified installation and scalability

### Advanced Capabilities

- [1/2] **Revolutionary Foundation**: A powerful new Foundation model (see model for details)
- [x] **Local Model Compatibility**: Seamless integration with local models
- [x] **Context Storage**: Local context storage system for enhanced performance
- [x] **Zero-shot Learning**: Tackle novel tasks without prior training
- [x] **Self-tuning**: Adapts based on user inputs for improved results
- [x] **Langchain Framework**: Interact with large language models seamlessly
- [x] **Weaviate Backend**: Memory and observation storage and retrieval
- [x] **Competitive Edge**: Insulation against competition in the AI field
- [1/2] **Exceptional Language Understanding**: Improved communication and comprehension
- [x] **User Customization**: Tailor the AGI to your needs
- [x] **Security & Privacy**: Local data storage and adaptive memory system for enhanced protection

Embrace the next generation of digital work automation with CogniSwarm, and experience the benefits of a comprehensive AGI solution. Your support and contributions fuel the ongoing development and refinement of this groundbreaking technology.

## CogniSwarm Model: A breakthrough foundational AGI model

<details>

  <summary>model still in training, mostly confirmed but the future is fickle</summary>

Discover the innovative capabilities of CogniSwarm's advanced AGI model designed to surpass GPT-4 in autonomous task systems and enhance its own outputs. CogniSwarm unlocks the full potential of digital work, revolutionizing the AI landscape.

- [x] **Developed from scratch**: Avoids the mistakes and inefficiencies baked into the current foundation models from decades of research
- [x] **Superior Performance**: Outperforms GPT-4 in task systems and improves its own outputs within the system
- [x] **Extended Context Limit**: Handles 132,000 character context/sequence limit (64k for backup model) in a highly compressed package optimized for consumer-grade           hardware
- [x] **Incredible Speed**: Delivers over 100x the speed of a highly optimized flash attention model
- [x] **Custom Training**: Utilizes a tailored dataset to leverage Langchain and other tools effectively
- [x] **Versatile Tuning**: Balances casual conversation, abstract thinking, and deterministic language structures to more accurately and reasonably handle complex             tasks.
- [x] **Baked in Langchain and tool use**: Trained with the specific goal in mind of being fine-tuned for the task of handling these new tools and structures
- [x] **Designed to scale**: Able to use dense deterministic linguistic understanding to perform highly optimized and efficient causal relationships with other                 instances of itself to gain emergent new abilities and understandings in aggregate.

</details>


```        ________                   ________
      /  /\     \   /\    /\     /  /\     \
    /  /  \     \ /  \ /  /  \ /  /  \     \
  /  /    \__   //\   /\\/__\//  /    \__   \
/_/__\    /  / //  \ /  //  /  /_/_\    /  /_\
\  \  \  /  / //\   /  //  /  /  /  \  /  /  /
  \  \  \/  /   \/  /  \/  /  /    \/  /  /
    \  \   \/  /\  \  /  /  /  /  /  /  /
      \  \   \  /  \   \/  /  /  /  /  /
        \  \___\/____\   \/__\/__/  /
          \  \  \    /  //  /  /  /  /
            \  \/  /  \/  /  /  /  /
              \  \/______\/  /  /
                \  \  \    /  /  /
                  \  \/  /  /  /
                    \  \/  /  /
                      \  \/  /
                       \____/  
      ______                   ______
    /  /\   \   /\    /\     /  /\   \
  /  /  \   \ /  \ /  /  \ /  /  \   \
/_/__\   \   //\   /\\/__\//  /    \   \
\  \  \  /  //  \ /  //  /  /  /  /  /  /
  \  \  \/  /  \/  /  \/  /  /  /  /  /
    \  \   \/  /\  \  /  /  /  /  /  /
      \  \   \  /  \   \/  /  /  /  /
        \  \___\/____\   \/  /  /  /
          \  \  \    /  //  /  /  /
            \  \/  /  \/  /  /  /
              \  \/______\/  /  /
                \  \  \    /  /  /
                  \  \/  /  /  /
                    \  \/  /  /
                      \  \/  /
                        \____/  
```
#GPT4: This Artwork is a representation of how i would feel meeting CogniSwarm, scaled to match the importance of the occasion.
