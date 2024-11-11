from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForTokenClassification
import pandas as pd

path = 'crawl/outputs/'
# save_model = AutoModelForTokenClassification.from_pretrained('crawl/NER/b')
# tokenizer = AutoTokenizer.from_pretrained('crawl/NER/b', do_lower_case=True)
save_model = AutoModelForTokenClassification.from_pretrained("emilyalsentzer/Bio_ClinicalBERT")
tokenizer = AutoTokenizer.from_pretrained("emilyalsentzer/Bio_ClinicalBERT", do_lower_case=True)

def split_document(document):
    sentences = document.split('. ')
    lenparagraph = 0
    paragraphs = []
    paragraph = ''
    for sentence in sentences:
        if (lenparagraph + len(sentence.split(' '))) <= 256:
            lenparagraph += len(sentence.split(' '))
            paragraph = paragraph + sentence + '. '
        else:
            paragraphs.append(paragraph)
            lenparagraph = 0
            paragraph = ''
    paragraphs.append(paragraph)
    return paragraphs


def predict(input_file, timestamp):
    nlp = pipeline("ner", model=save_model, tokenizer=tokenizer, aggregation_strategy='simple',
                   ignore_labels=['X', 'O'], device=0)
    df = pd.read_csv(input_file)
    TRAIN_DATA = []
    for i in range(len(df)):
        descriptionNER = ''
        description = str(df['SkillWillLearn'][i]) + str(df['Description'][i])
        paragraph_for_ner = split_document(description)
        know = []
        tool = []
        lang = []
        plat = []
        fram = []
        soft = []
        for item in paragraph_for_ner:
            results = nlp(item)
            for ele in results:  # add character indexes
                # TEST in obj ent just created above
                if ele["entity_group"] == 'KNOW':  # (ele["entity_group"] corresponding to the label in label studio)
                    know.append(ele["word"] + ' %% ' + str(ele["score"]))
                if ele["entity_group"] == 'TOOL':
                    tool.append(ele["word"] + ' %% ' + str(ele["score"]))
                if ele["entity_group"] == 'FRAM':
                    fram.append(ele["word"] + ' %% ' + str(ele["score"]))
                if ele["entity_group"] == 'LANG':
                    lang.append(ele["word"] + ' %% ' + str(ele["score"]))
                if ele["entity_group"] == 'PLAT':
                    plat.append(ele["word"] + ' %% ' + str(ele["score"]))
                if ele["entity_group"] == 'SOFTSKILL':
                    soft.append(ele["word"] + ' %% ' + str(ele["score"]))
            for ele in reversed(results):
                item = item[:ele['end']] + '(' + ele['entity_group'] + ')' + item[ele['end']:]
            descriptionNER += item
            
        TRAIN_DATA.append({'knowledge': know, 'tool': tool, 'framework': fram, 
        'platform': plat, 'language': lang, 'soft': soft, 
        'descriptionNER': descriptionNER})

    df1 = pd.DataFrame(df)
    df2 = pd.DataFrame(TRAIN_DATA)
    fn = pd.concat([df1, df2], axis=1, join='inner')
    file_path = path + "output" + str(timestamp) + ".csv"
    fn.to_csv(file_path)  # dump to csv
    return file_path