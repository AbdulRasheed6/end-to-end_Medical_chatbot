# end-to-end_Medical_chatbot

# How to run ?
### STEPS:

Clone the Repository

```bash
Project repo: https://github.com/
```

### STEP 01- Create a conda environment after opening the repository

```bash
conda create -n medicapp python=3.10 -y
```

```bash
conda activate medicapp
```




### STEP 02- install the requirements
```bash
pip install -r requirements.txt

```

### Create a .env file in the root directory add add your Pinecone and Gemini ai credentials as follows:

```
PINECONE_API_KEY= "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
GEMINI_API_KEY= "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```


```bash
# run the following command to store embedings to pinecone
python store_index.py
```


```bash
# Finally run the following command
python app.py
```

```bash
open up localhost:
```



### Techstack Used:


- Python
- LangChain
- Flask
- Gemini
- Pinecone
