#!/usr/bin/python
# coding=utf8

import sys;
import re;
from HTMLParser import HTMLParser;

html_data = "hi"

shell = open("output/import.sh","w");

class MyHTMLParser(HTMLParser):
  def handle_data(self,data):
    data = data.replace("&nbsp;",'');
    data = data.replace(" ",'');
    global html_data
    if data == "" : return;
    if html_data != "":
      html_data = html_data + "," + data; 
    else:
      html_data = data; 

parser = MyHTMLParser();
def getdata(str) :
  parser.reset();
  global html_data
  html_data = ""; 
  try:
    parser.feed(str);
  finally:
    return html_data;

def unify_data(item_data,item_name) :
  if item_name=="所属课程组": 
    item_data = item_data.replace("组","");
    item_data = item_data.replace("趣味经济学","经济");
    item_data = item_data.replace("趣味经济","经济");
    item_data = item_data.replace("课","");
    item_data = item_data.replace("English","英语");
    item_data = item_data.replace("english","英语");
    item_data = item_data.replace("计算机儿童","计算机");
    item_data = item_data.replace("科普","兴趣");
    item_data = item_data.replace("国学","语文");
    item_data = item_data.replace("艺术音乐","音乐");
  return item_data 

def getcontent(str) :
  start_pos=str.find(">")+len(">");
  end_pos=str.find("</td>");
  if end_pos == -1: end_pos=str.find("</TD>");

  return str[start_pos:end_pos];

item_key_list = ["备课人","Email/MSN","所属课程组","课程名称","上课日期","上课时长","授课对象","学生信息"];
item_value_set = {};

content_key_list = ["授课目标","授课内容","授课提纲","授课步骤","教学环境、材料需求","助教需求","其他请补充"];
content_value_set = {};

item_parsed = "true"
content_parsed = "end"

def build_wiki_page(item_value_set,content_value_set,id,author,semaster,school,subject,wikitype,lesson_idx) :
  page = "{{Infobox TeachingPlan";
  name = "";
  for item in item_key_list:
    if not item in item_value_set: continue;
    
    if item=="Email/MSN": page = page+"\n"+"| Email = "+item_value_set[item];
    else: page = page+"\n"+"| "+item+" = "+item_value_set[item];
  
  #search a name
  lesson_name="";
  if "课程名称" in item_value_set:
    lesson_name=item_value_set["课程名称"];
  if lesson_name!="": name = lesson_name;
  elif subject != "": name = subject;
  elif "所属课程组" in item_value_set: name = item_value_set["所属课程组"];
  page = page+"\n"+"| name = "+name+"教案";
  
  #select a title picture
  page = page+"\n"+"| image = Textbook.JPG";
  
  page += "\n}}\n";

  for content in content_key_list:
    if not content in content_value_set: continue;
    page = page + "\n" + "== '''" + content + "'''==\n" + content_value_set[content];
    
  #增加参考页面
  #TODO: 程序自动添加课程总结链接
  page = page + "\n" + "== '''参考页面'''==\n"
  page = page + "\n" + "[http://www.ygclub.org/wiki/index.php?doc-view-"+id+".html 旧百科原始链接]\n"

  #增加分类
  if "所属课程组" in item_value_set: 
    page = page + "\n" + "[[Category:" + item_value_set["所属课程组"]+"教案]]";
  if school != "":
    page = page + "\n" + "[[Category:在" + school +"使用过的教案]]";

  #增加导航
  if "所属课程组" in item_value_set: 
    page = page + "\n" + "{{" + item_value_set["所属课程组"]+"教案}}";
  if school != "":
    page = page + "\n" + "{{" + school +"教案}}";

  
  filename = name+"-"+semaster+"-"+school+"-"+lesson_idx+"-"+wikitype;
  
  print "export:"+filename;
#  print page;
#  try :
  pagefile = open("output/"+filename,"w");
#    print >> pagefile, page;
#  finally:
  pagefile.close();
  
  #print "php maintenance/importTextFile.php --title "+filename+" --user "+author+" data/"+filename;
  #print >> shell, "php maintenance/importTextFile.php --title "+filename+" --user "+author+" data/"+filename;

#  print "semaster="+semaster;
#  print "subject="+subject;
#  print page;
  return;

div_used = "false";
for line in open(sys.argv[1]):
  line = line.rstrip();
  if re.match("&quot;[0-9]",line) :
    if len(item_value_set) > 0: build_wiki_page(item_value_set,content_value_set,id,author,semaster,school,subject,wikitype,lesson_idx_now);
    
    #start a new semaster-subject
    print line;
    lesson_idx_list = [];
      

    title = line.split("&quot;;&quot;")[4].split("&quot")[0];
    author = line.split("&quot;;&quot;")[3];
    id = line.split("&quot;")[1];
    
    print "id\t"+id  
    print "title\t"+title  
    print "author\t"+author  
    
    semaster = "";
    school = "";
    subject = "";
    wikitype = "";
    item_value_set.clear();
    content_value_set.clear();
    
    basic_info = title.split("-");
    if len(basic_info)==1: basic_info = title.split("—");
    if len(basic_info)>=4:
      semaster = basic_info[0];
      school = basic_info[1];
      if school == "信心": school = "信心学校";
      if school == "育才学校": school = "朝阳育才";
      if school == "光明": school = "光明学校";
      subject = basic_info[2];
      wikitype = basic_info[3];
      
      print "semaster\t"+semaster  
      print "school\t"+school  
      print "subject\t"+subject  
      print "wikitype\t"+wikitype 
      print 
  
    new_subject = "true";
  
  divname = re.search("<(div|DIV) class=.*hdwiki_tmml.*</(div|DIV)>",line);
  if divname: 
    lesson_idx = getdata(divname.group());
    lesson_idx_list.append(lesson_idx);
    div_used = "false";

  plan_start = re.search("center.*上课准备提纲",line);
  if plan_start:
    if new_subject == "false":
      if len(item_value_set) > 0:build_wiki_page(item_value_set,content_value_set,id,author,semaster,school,subject,wikitype,lesson_idx_now);
    new_subject = "false";

    item_value_set.clear();
    content_value_set.clear();
    lesson_idx_now = "";
    if div_used == "false": lesson_idx_now = lesson_idx;
    #div_used = "true";
    #print  
    #print lesson_idx_now

  #parse metadata
  if item_parsed == "false" :
    if (line.find("</td>")==-1) and (line.find("</TD>")==-1) : continue;
    item_data = getdata(line);
    item_data = unify_data(item_data,item_name);
    item_value_set[item_name]=item_data;
    item_parsed = "true";
    #print item_name + "=" + item_data;

  for item_key in item_key_list:
    item_start = re.search(">*"+item_key+".*<",line);
    if item_start:
      item_name = item_key;
      item_data = "";
      item_parsed = "false"
      miss_item = getdata(line).split(",");
      if len(miss_item)>1 and miss_item[0]==item_key :
        item_data = miss_item[1];
        item_data = unify_data(item_data,item_name);
        item_value_set[item_name]=item_data;
        item_parsed = "true";
#        print item_name + "=" + item_data;
      elif getdata(line)!=item_key and getdata(line).find(item_key)==0 :
        item_data = getdata(line)[len(item_key):];
        item_data = unify_data(item_data,item_name);
        item_value_set[item_name]=item_data;
        item_parsed = "true";
#        print item_name + "=" + item_data;

  #parse main contents
  if content_parsed == "start" :
    if content_data == "" : content_data = line;
    else: content_data = content_data + "\n" + line;
    
    td_pos = line.find("</td>");
    if td_pos == -1 : td_pos = line.find("</TD>");
    if td_pos >=0 :
      content_data = getcontent(content_data);
      content_value_set[content_name] = content_data;
      #print content_name+"="+content_data;
      #print ;
      content_parsed = "end";

  for content_key in content_key_list:
    content_start = re.search(">*"+content_key+".*<",line);
    if content_start:
      content_name = content_key;
      content_data = "";
      content_parsed = "start"

shell.close(); 
