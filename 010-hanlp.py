import hanlp

recognizer = hanlp.load(hanlp.pretrained.ner.MSRA_NER_BERT_BASE_ZH)


def extract_name(text: str):
  
  print('text', text)
  result = parse_name_hanlp(text)
  return result

def parse_name_hanlp(text: str):
  print('text========', text)
  entityx = recognizer.predict(list(text))
  print('entityx', entityx)
  for param in entityx:
    if param[1] == "NR":
      print("name=", param[0])
      return param[0]
    

if __name__ == '__main__':
  str = '段岭小声回答拔都的问题，从怀中取出点心。“你饿了吗？”段岭说。拔都摇摇头，段岭又说：“吃一点吧，吃了早上才有力气逃。”'
  name = extract_name('梁传凯办公电话：3822268')
  print(name)