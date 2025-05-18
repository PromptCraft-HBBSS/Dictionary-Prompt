# Dictionary Prompt

An example `XML` formatted prompt. School project.

## 0. Deploying

> It is recommended to delete the `<meta>` and header comment section to save on api call expenses.
> If one were to run this in a GUI, please replace all $idStartsAt and $words with your starting id and word list.
> 
After cloning this project, create a `dotenv` configuration file:

```shell
http_proxy=http://127.0.0.1:1087        # Optional runtime configuration
https_proxy=http://127.0.0.1:1087       

# On our production setup, the BACKEND_API_VERSION is the same as our mongodb collection name. Modify this according to your backend setup.
BACKEND_API_VERSION="v0"
SERVER_PORT=4040                        # Production env setup, not necessary

MODEL_APIKEY="master"
MODEL_APISECRET="sk-....a6"                 # Your API key
MODEL_ENDPOINT="https://api.deepseek.com/"  # Your API provider endpoint (OpenAI SDK Compatible)
MODEL_NAME="deepseek-chat"                  # Your model name

# The following configurations are for our production setup.
# We are building a large database, so we hosted our db on Atlas. You can decide to alter this to your need.
# The connection string is formed using f"{protocol}://{user}:{password}@{uri}/{queries}";
MONGODB_PROTOCOL="mongodb+srv"              # Recommended
MONGODB_URI="******"
MONGODB_USER="*******"
MONGODB_PASSWORD="********"
MONGODB_QUERIES="*******"
MONGODB_DB="********"

# The system prompt. Tailor it to your need.
# In our production scenario, we are builidng a catalog of ZKE (Shanghai Junior Secondary School Academic Examination - English Section) vocabulary.
SYSTEM_PROMPT='You are an etymologist and lexicographer working on a MongoDB-based vocabulary database for a national middle-school education program. Your goal is to catalog vocabulary entries with detailed linguistic, phonetic, and semantic information.'
```

and run 

```zsh
pip install -r requirements.txt
```

to install all frozen dependencies to your environment. A `venv` or `conda` virtual env is highly recommended.

## 1. Structure
The prompt is inclosed in a `<prompt>` tag. The prompt is divided up to 4 sections: `task`, `requirements`, `instructions`, `example`, and `config`.

### 1x00 Task
This section of the prompt connects with the system prompt. It introduces the following task to the model.

```
You are a MongoDB database administrator and a vocabulary expert. 
Your task is to create a JavaScript array of MongoDB documents for vocabulary entries.
You are to generate a JavaScript array of MongoDB documents for vocabulary entries, following some strict requirements.
```

### 1x01 Requirements

In order to make sure that the model outputs the format we want(i. e. a JSON array), specific requirements are given to the model. The requirement 'without explanation' and `raw JSON` are repeated. In order to enforce a strict AST, specific fields are given.

### 1x02 Instructions

The following algorithm is proposed to the model:

```
flowchart TD
    %% Initialization
    subgraph Init [Initialization]
        A[Start]
        B[Initialize output array]
        C[Set ID counter to $idStartsAt]
        D[Split input words into senses array]
    end

    %% Processing Words
    subgraph Process [Process Each Word]
        E[For each word in senses]
        F[Increment ID]
        G[Analyze lexical properties]
        H[Identify definitions]
        I[Identify phonetics]
        J[Identify parts of speech]
    end

    %% Parallel Processing
    G --> H
    H --> I
    I --> J
    J --> K[Branching Point]

    %% Constructing Senses
    subgraph Senses [Construct Senses]
        L[For each definition]
        M[For each phonetic]
        N[For each part of speech]
        O{Valid combination?}
        P[Construct sense object]
        Q[Add sense to senses array]
    end

    %% Etymology
    subgraph Etym [Etymology]
        R[Identify prefixes, root, suffixes]
        S[For each etym element]
        T[Identify substring]
        U[Draft origin description]
        V[Construct etymology object]
        W[Add etymology to etym array]
    end

    %% Notes
    subgraph Notes [Notes]
        X[Draft usage note]
    end

    %% Finalization
    subgraph Final [Finalize Word]
        Y[Construct word object]
        Z[Add word object to output array]
        AA[Increment ID counter]
    end

    %% Flow Connections
    A --> B --> C --> D --> NN[For Each Word] --> E
    E --> F --> G
    K --> L --> M --> N --> O --> P --> Q --> Y
    K --> R --> S --> T --> U --> V --> W --> Y
    K --> X --> Y --> Z --> AA --> NN
```

### 1x03 Example
An example is given the to model:

| Config | Starting ID | Words
| - | - | - |
| Value | 1001 | a, ability, about |

An example output is also given:

```json
[
	{
		"id": 1001,
		"word": "a",
		"senses": [
			{
				"pos": "article",
				"phonic": "[ə]",
				"definition": "不定冠词（用于辅音音素开头的词前）"
			},
			{
				"pos": "article",
				"phonic": "[eɪ]",
				"definition": "不定冠词（强调时使用）"
			}
		],
		"etym": [
			{
				"fix": "a",
				"description": "源自古英语 'ān'（意为“一个”）的缩略形式"
			}
		],
		"notes": "发音取决于后续词的起始音素和语境强调。在元音音素前需使用 'an'（如：an apple [ən 'æpl]）"
	},
	{
		"id": 1002,
		"word": "ability",
		"senses": [
			{
				"pos": "n.",
				"phonic": "[ə'bɪləti]",
				"definition": "能力；才能；本领"
			}
		],
		"etym": [
			{
				"fix": "ab-",
				"description": "表示“去，离开”"
			},
			{
				"fix": "-ility",
				"description": "名词后缀，表示性质、能力"
			}
		],
		"notes": "常用于形容人的才能或完成任务的能力"
	},
	{
		"id": 1003,
		"word": "about",
		"senses": [
			{
				"pos": "prep.",
				"phonic": "[ə'baʊt]",
				"definition": "关于；大约"
			},
			{
				"pos": "adv.",
				"phonic": "[ə'baʊt]",
				"definition": "到处；大约"
			}
		],
		"etym": [
			{
				"fix": "a-",
				"description": "表示“在……之上”"
			},
			{
				"fix": "bout",
				"description": "源自古英语 'būtan'，意为“外面”"
			}
		],
		"notes": "常用于表示主题、数量或范围"
	}
]
```

This give a further intuitive template for the model

### 0x04 Config
This is actually a template string that is filled at runtime:

```xml
<config>
	<idStartsAt>$idStarts</idStartsAt>
	<words>$words</words>
</config>
```

