#!/usr/bin/python
# coding=utf8

import MySQLdb

shell = open("output/import.basic.sh","w");

try:
  conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='root',db='ygwiki',port=8889)
  cur=conn.cursor()
  cur.execute('select * from markup_doc')
  row = cur.fetchone()
  while row is not None:
    print row[1]+"\t"+row[5];
   
    author = row[5];
    filename = row[1].replace(" ",'_');
    filename = filename.replace("/","");
    
#    if filename.find("-课程提纲")>0 : 
#      row = cur.fetchone()
#      continue;
#    if filename.find("-课程总结")>0 :
#      row = cur.fetchone()
#      continue;
#    if filename.find("-助教反馈")>0 :
#      row = cur.fetchone()
#      continue;

    page = row[4];
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


