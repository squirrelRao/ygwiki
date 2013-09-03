#!/usr/bin/python
# coding=utf8

import sys;
import string;
import re;
import MySQLdb;
from HTMLParser import HTMLParser;

html_data = "hi"

shell = open("output/import.feedback.sh","w");

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
  if item_name=="课程名称": 
    item_data = item_data.replace("：","");
    item_data = item_data.replace(":","");
  if item_name=="所属课程组": 
    item_data = item_data.replace("组","");
    item_data = item_data.replace("趣味经济学","趣味经济");
    if item_data == "经济": item_data = "趣味经济";

    item_data = item_data.replace("课","");
    item_data = item_data.replace("English","英语");
    item_data = item_data.replace("english","英语");
    item_data = item_data.replace("计算机儿童","计算机");
    item_data = item_data.replace("科普","兴趣");
    item_data = item_data.replace("国学","语文");
    item_data = item_data.replace("艺术音乐","艺术");
    item_data = item_data.replace("美术","艺术");
    item_data = item_data.replace("舞蹈","艺术");
    if item_data.find("艺术")>=0: item_data = "艺术";
    item_data = item_data.replace("音乐","艺术");
    if item_data == "":  item_data = "未分类";
  return item_data 

def unify_basic_info(basic_info):
  semaster = basic_info[0];
  semaster = semaster.replace("季","");
  if semaster == "2010春": semaster="2010年春";
  if semaster == "2010秋": semaster="2010年秋";
  if semaster == "2011春": semaster="2011年春";
  if semaster == "2011秋": semaster="2011年秋";
  if semaster == "2012春": semaster="2012年春";
  if semaster == "2012秋": semaster="2012年秋";
  if semaster == "2012": semaster="2012年春";
  if semaster == "2013春": semaster="2013年春";
  if semaster == "2013春学期": semaster="2013年春";
  school = basic_info[1];
  if school == "信心": school = "信心学校";
  if school == "育才学校": school = "朝阳育才";
  if school == "光明": school = "光明学校";
  subject = basic_info[2];
  subject = subject.replace("课","");
  if subject == "兴趣科普": subject = "科普";
  if subject == "趣味经济": subject = "趣味经济学";
  if subject == "语文国学启蒙": subject = "国学";
  if subject == "经济": subject = "趣味经济学";
  if subject == "兴趣": subject = "科普";
  if subject == "计算机": subject = "计算机（儿童）";
  if subject == "计算机儿童": subject = "计算机（儿童）";
  if subject == "四年级英语": subject = "英语四年级";
  if subject == "五年级英语": subject = "英语五年级";
  if subject == "六年级英语": subject = "英语六年级";
  wikitype = "助教反馈"

  return [semaster,school,subject,wikitype];

def getcontent(str) :
  start_pos=str.find(">")+len(">");
  end_pos=str.find("</td>");
  if end_pos == -1: end_pos=str.find("</TD>");

  return str[start_pos:end_pos];

item_key_list = [];
item_value_set = {};

content_key_list = ["课堂总体情况","期望下节课主讲复习的内容","对课程内容设置的不同见解","给讲师的评语","课堂讲课和助教中存在的问题","有什么新想法","课前主讲人和助教沟通情况","课程设计的思路","课程设计的难易程度","主讲人课堂时间把握情况","课堂秩序维持情况","助教的表现及职责完成情况","学生课堂表现"];
content_value_set = {};

semaster_list = ["2010年春","2010年秋","2011年春","2011年秋","2012年春","2012年秋","2013年春"];

item_parsed = "true"
content_parsed = "end"

subject_school_dict = {};
semaster_school_dict = {};
page_dict = {};

def build_wiki_page(item_value_set,content_value_set,id,author,semaster,school,subject,wikitype,lesson_idx) :
  global semaster_school_dict;
  global subject_school_dict;
  global page_dict;
    
  page = "{{Infobox LessonFeedback";
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
  elif "所属课程组" in item_value_set: 
    name = item_value_set["所属课程组"];
  page = page+"\n"+"| name = "+name+"教案";
  
  if "所属课程组" in item_value_set: 
    group = item_value_set["所属课程组"];
    print "group="+group;
  
  #select a title picture
  page = page+"\n"+"| image = Textbook.JPG";
  
  page += "\n}}\n";

  for content in content_key_list:
    if not content in content_value_set: continue;
    page = page + "\n" + "== '''" + content + "'''==\n" + content_value_set[content];
    
  #增加参考页面
  page = page + "\n" + "== '''参考页面'''==\n"
  page = page + "\n*[[" + subject+"-"+semaster+"-"+school+"-"+lesson_idx+"-"+"课程提纲]]";
  page = page + "\n*[[" + subject+"-"+semaster+"-"+school+"-"+lesson_idx+"-"+"课程总结]]";
  page = page + "\n*[[" + subject+"-"+semaster+"-"+school+"-"+"学生课堂表现]]";
  page = page + "\n\n" + "*[http://www.ygclub.org/wiki/index.php?doc-view-"+id+".html 旧百科原始链接]\n"


  #增加分类
  if subject != "":
    page = page + "\n" + "[[Category:" + subject +"助教反馈]]";

  #增加导航
  page = page + "\n" + "{{" + subject +"助教反馈}}";

  filename = subject+"-"+semaster+"-"+school+"-"+lesson_idx+"-"+wikitype;
  filename = filename.replace("/","");
  
  print "export:"+filename;
  #print page;
  try :
    pagefile = open("output/"+filename,"w");
    print >> pagefile, page;
  
    print >> shell, "php maintenance/importTextFile.php --title \""+filename+"\" --user "+author+" \"data/"+filename+"\"";

    #update template and category map
    #by-subject
    if subject=="" : return;
    
    if subject in subject_school_dict:
      subject_school_dict[subject].add(school);
    else:
      subject_school_dict[subject]=set([school]);

    #update template and category map
    #by-semaster
    if semaster =="" : return;
    
    if semaster in semaster_school_dict:
      semaster_school_dict[semaster].add(school);
    else:
      semaster_school_dict[semaster]=set([school]);

    page_key = subject+"-"+semaster+"-"+school;
    if page_key in page_dict:
      page_dict[page_key].append("[["+filename+"|"+name+"]]");
    else:
      page_dict[page_key]=["[["+filename+"|"+name+"]]"];
    
  finally:

#  print "semaster="+semaster;
#    print "subject="+subject;
#    print "subject="+subject;
#  print page;
    return;

try:
  conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='root',db='ygwiki',port=8889)
  cur=conn.cursor()
  cur.execute('select * from markup_doc')
  row = cur.fetchone()
  while row is not None:
    #start a new semaster-subject

    title = row[1];
    author = row[5];
    content = row[4]
    id=str(row[0]);

    if (title.find("-助教反馈")<0) and (title.find("-助教听课反馈表")<0) : 
      row = cur.fetchone()
      continue;

    print "id\t"+id  
    print "title\t"+title  
    print "author\t"+author  
    
    semaster = "学期待补充";
    school = "学校待补充";
    subject = "学科待补充";
    wikitype = "助教反馈";
    item_value_set.clear();
    content_value_set.clear();
    
    basic_info = title.split("-");
    if len(basic_info)==1: basic_info = title.split("—");
    if len(basic_info)>=4:
      [semaster,school,subject,wikitype] = unify_basic_info(basic_info);
     
      print "semaster\t"+semaster  
      print "school\t"+school  
      print "subject\t"+subject  
      print "wikitype\t"+wikitype 
      print 
    else :
      subject = title;

    content = content.replace("","");
    content = content.replace("</td><td>","</td>\n<td>");
    content = content.replace("</TD><TD>","</TD>\n<TD>");
    content = content.replace("</div><","</div>\n<");
    content = content.replace("</DIV><","</DIV>\n<");
    content = content.replace("></DIV",">\n</DIV");
    content = content.replace("></div",">\n</div");

    new_subject = "true";
    lesson_idx_now = "";
    for line in content.split("\n"):
  
      divname = re.search("^==.*==",line);
      if divname: 
        chapter = divname.group();
        lesson_idx = chapter[2:len(chapter)-2];
   
      plan_start = re.search("^==.*==",line);
      if plan_start:
        if new_subject == "false":
          if (len(item_value_set) > 0) or (len(content_value_set) > 0): 
            build_wiki_page(item_value_set,content_value_set,id,author,semaster,school,subject,wikitype,lesson_idx_now);
        new_subject = "false";
                                 
        item_value_set.clear();
        content_value_set.clear();
        if lesson_idx == lesson_idx_now :
          lesson_idx_now = lesson_idx + "2";
        else :
          lesson_idx_now = lesson_idx;
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
        item_start = re.search("(strong|STRONG)>*"+item_key+".*<",line);
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
          #print "content_name="+content_name;
          #print ;

    if (len(item_value_set) > 0) or (len(content_value_set) > 0): build_wiki_page(item_value_set,content_value_set,id,author,semaster,school,subject,wikitype,lesson_idx_now);

    row = cur.fetchone()

  cur.close()
  conn.close()

except MySQLdb.Error,e:
  print "Mysql Error %d: %s" % (e.args[0], e.args[1])


#build template:

#subject template:
old_semaster="";

for subject in subject_school_dict:
  #new subject!
  listnum=1;
  filename = "Template:"+subject+"助教反馈";
  template="{{Navbox\n|name="+subject+"助教反馈\t|title = "+subject+"助教反馈";
  new_template = "true";
  for semaster in semaster_list:
    new_semaster = "true";
    sub_listnum=1;
    for school in subject_school_dict[subject]:
      page_key = subject+"-"+semaster+"-"+school;
      if page_key in page_dict:
        if new_semaster == "true":
          if new_template != "true":
            template = template + "\n  }}";
          new_template = "false";
          template += "\n  |group" + str(listnum) + " = " + semaster;
          template += "\n  |list" + str(listnum) + " = ";
          template += "\n  {{Navbox subgroup";
          new_semaster = "false";
          listnum = listnum + 1;

        template += "\n    |group" + str(sub_listnum) + " = " + school;
        template += "\n    |list" + str(sub_listnum) + " = ";
        sub_listnum = sub_listnum + 1;
  
        for page in page_dict[page_key]:
          template += page + " - ";

        template = template[0:len(template)-2];

  template = template + "\n  }}";
  template += "\n}}";

  if (template!=""):
    print "export:"+filename;
    
    pagefile = open("output/"+filename,"w");
    print >> pagefile, template; 
    print template;
  
    #print "php maintenance/importTextFile.php --title "+filename+" --user "+author+" data/"+filename;
    print >> shell, "php maintenance/importTextFile.php --title \""+filename+"\" --user hdwiki2mediawiki \"data/"+filename+"\"";
 

shell.close(); 
