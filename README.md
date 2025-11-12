# RAG-audio

This project is using FastAPI, Mistral AI and Qdrant to provide an API for simple RAG from audio. It allows to post an audio file (that contains speech) and interact with its content via natural language. It is a project made to document learning and experimenting with the tools.

## Installation

```sh
git clone https://github.com/ngc6720/rag-audio.git
cd rag-audio
```

The project uses Mistral AI, you will need an API key to start the app. To create a key, connect to your Mistral account, got to [Mistral's settings - API Keys](https://admin.mistral.ai/organization/api-keys) and click on "Create new key". It is recommended to select an expiration date for the key.

Create a folder named "secrets" at the root of the project and, inside, create a "mistral_api_key.txt" file that contains your Mistral public API key.
This command does it all in one go (replace YOUR_API_KEY with your Mistral key):

```sh
mkdir -p secrets && echo YOUR_API_KEY > secrets/mistral_api_key.txt
```

### A) With docker

The recommended way, if you have Docker installed (requires Docker Compose v2.23.1 or above):

```sh
docker compose up -d
```

You can visit

- http://localhost:8000/docs to visualize and try the API.
- http://localhost:6333/dashboard to visualize vectors.

### B) With a virtual environment

/!\ Only for the Python/FastAPI app : Docker would still be needed for any other containerized service, i.e Qdrant for the database.

When using venv, the python app will use an in-memory version of the vector database instead, and it will not be persistant.

Skip these steps if you are already using Docker :

#### Create virtual environment

```sh
python3 -m venv .venv
source .venv/bin/activate
```

#### Install dependencies

```sh
python -m pip install --upgrade pip
pip install -r requirements.txt
```

#### Start server dev

```sh
fastapi dev app/main.py --host 0.0.0.0 --port 8000
```

#### Start server prod

```sh
fastapi run app/main.py --host 0.0.0.0 --port 80
```

## Usage

### With Swagger UI

With your browser, visit http://localhost:8000/docs for a convenient way to try endpoints.

Steps:

1. Create context from audio : provide an audio file and a name for the context.
2. Ask in context : provide a query and the name of the context to link your question to.

### With cURL

Here are examples with cURL commands instead, using the audio from ./test_media:

#### Create context from audio

```sh
curl -X POST -F "file=@test_media/stew.mp3" http://localhost:8000/rag/upload?&name=stew
```

#### Ask in context

prompt: What are some secrets for this recipe?

```sh
curl http://localhost:8000/rag/search?&q=What%20are%20some%20secrets%20for%20this%20recipe%3F&name=stew
```

## Results

With ./test_media/stew.mp3, which is the audio from a rabbit stew recipe video.

#### Q: What are some secrets for this recipe?

**Answer:**

```
"Here are some secrets for the recipe mentioned in the context:

1. **Mustard Usage**: The recipe emphasizes the use of Dijon mustard, stating that English mustard should be avoided. It is recommended to be generous with the mustard, brushing it everywhere on the rabbit. <quote>So I'll take the mustard, put mustard everywhere.</quote> <timestamp>306.8</timestamp> and <quote>And you got to be generous with the mustard.</quote> <timestamp>312.8</timestamp>.

2. **Cooking Time and Temperature**: The rabbit should be cooked in the oven at 180 degrees for about 30 to 45 minutes. <quote>cook for about 30 minutes, and it will be ready.</quote> <timestamp>531.1</timestamp> and <quote>45 minutes in the oven at 180.</quote> <timestamp>555.1</timestamp>.

3. **Liver Handling**: The liver is added last to prevent it from drying out. <quote>Last piece of meat going is the liver.</quote> <timestamp>458.3</timestamp> and <quote>So I put it on the last minute, you know.</quote> <timestamp>464.8</timestamp>.

4. **White Wine for Moisture**: A bit of white wine is added to create a light jus to keep the meat moist. <quote>Now I'm going to put a bit of white wine, just to create a little jus to keep the meat moist.</quote> <timestamp>514.9</timestamp>.

5. **Garlic and Tomato**: The recipe suggests using garlic and tomatoes, with a preference for cherry tomatoes. <quote>three cloves of garlic, or 10 cloves of garlic.</quote> <timestamp>475.6</timestamp> and <quote>But I had the cherry tomato, are quite good.</quote> <timestamp>486.1</timestamp>.

6. **Gentle Cooking**: The cooking process should be gentle to avoid burning. <quote>so you got to be gentle.</quote> <timestamp>411.3</timestamp> and <quote>It should be just gently sealed, you know.</quote> <timestamp>447.8</timestamp>.

These details highlight the key techniques and ingredients used in the recipe."
```
