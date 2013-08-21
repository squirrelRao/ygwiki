#!/usr/bin/python
# coding=utf8

import MySQLdb
def unify_basic_info(basic_info):
  semaster = basic_info[0];
  semaster = semaster.replace("季","");
  semaster = semaster.replace("学期","");
  if semaster == "2010春": semaster="2010年春";
  if semaster == "2010秋": semaster="2010年秋";
  if semaster == "2011春": semaster="2011年春";
  if semaster == "2011秋": semaster="2011年秋";
  if semaster == "2012春": semaster="2012年春";
  if semaster == "2012秋": semaster="2012年秋";
  if semaster == "2012": 
    semaster="2012年秋";
    if basic_info[2]=="趣味经济": semaster="2012年春";
    if basic_info[2]=="科普": semaster="2012年春";
    if basic_info[2]=="科普课": semaster="2012年春";
  if semaster == "2013春": semaster="2013年春";
  if semaster == "2013": semaster="2013年春";

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

  wikitype = "学生课堂表现"

  return [semaster,school,subject,wikitype];


shell = open("output/import.student.sh","w");

try:
  conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='root',db='ygwiki',port=8889)
  cur=conn.cursor()
  cur.execute('select * from markup_doc')
  row = cur.fetchone()
  while row is not None:
   
    title = row[1];
    author = row[5];
    content = row[4]
    id=str(row[0]);

    title = title.replace(" ",'_');
    title = title.replace("/","");
    
    if (title.find("学生信息和表现")>0) or (title.find("课堂表现")>0) or (title.find("学生表现")>0)  : 

      print "id\t"+id  
      print "title\t"+title  
      print "author\t"+author  

      semaster = "学期待补充";
      school = "学校待补充";
      subject = "学科待补充";
      wikitype = "学生课堂表现";
  
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
        row = cur.fetchone()
        continue;

      wiki_title = subject + "-" + semaster + "-" + school + "-" + wikitype;
      if wiki_title == title: 
        row = cur.fetchone()
        continue;

      page = "#redirect [["+ title +"]]";
      filename = wiki_title;
      print "exporting:"+filename;
      pagefile = open("output/"+filename,"w");
      print >> pagefile, page;
  
      print >> shell, "php maintenance/importTextFile.php --title \""+filename+"\" --user "+author+" \"data/"+filename+"\"";
  
    row = cur.fetchone()

  cur.close()
  conn.close()
  shell.close(); 

except MySQLdb.Error,e:
  print "Mysql Error %d: %s" % (e.args[0], e.args[1])


