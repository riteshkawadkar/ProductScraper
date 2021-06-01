import crochet
crochet.setup()

from flask import Flask , render_template, request, redirect, url_for
from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher
import time

from flask_sqlalchemy import SQLAlchemy

from woods.woods.spiders.aayersfloorsSpider import AayersfloorsspiderSpider
from woods.woods.spiders.americanheritagefloorsSpider import AmericanheritagefloorsspiderSpider
from woods.woods.spiders.arimarwoodSpider import ArimarwoodspiderSpider
from woods.woods.spiders.bhwfloorsSpider import BhwfloorsspiderSpider
from woods.woods.spiders.bpiprestigeSpider import BpiprestigespiderSpider
from woods.woods.spiders.bruceSpider import BrucespiderSpider
from woods.woods.spiders.ddcfloorsSpider import DdcfloorsspiderSpider
from woods.woods.spiders.eaglecreekfloorsSpider import EaglecreekfloorsspiderSpider
from woods.woods.spiders.earthwerksSpider import EarthwerksspiderSpider
from woods.woods.spiders.eleganzatilesSpider import EleganzatilesspiderSpider
from woods.woods.spiders.evafloorsSpider import EvafloorsspiderSpider
from woods.woods.spiders.fuzionflooringSpider import FuzionflooringspiderSpider
from woods.woods.spiders.hillcountryinnovationsSpider import HillcountryinnovationsspiderSpider
from woods.woods.spiders.indusparquetSpider import IndusparquetspiderSpider
from woods.woods.spiders.johnsonhardwoodSpider import JohnsonHardwoodspiderSpider
from woods.woods.spiders.knoasflooringSpider import KnoasflooringspiderSpider
from woods.woods.spiders.lawsonfloorsSpider import LawsonfloorsspiderSpider
from woods.woods.spiders.licousSpider import LicousspiderSpider
from woods.woods.spiders.lwflooringSpider import LwflooringspiderSpider
from woods.woods.spiders.manningtonSpider import ManningtonspiderSpider
from woods.woods.spiders.mohawkflooringSpider import MohawkflooringspiderSpider
from woods.woods.spiders.montserratfloorsSpider import MontserratfloorsspiderSpider
from woods.woods.spiders.msisurfacesSpider import MsisurfacesspiderSpider
from woods.woods.spiders.mullicanflooringSpider import MullicanflooringspiderSpider
from woods.woods.spiders.realwoodfloorsSpider import RealwoodfloorsspiderSpider
from woods.woods.spiders.republicfloorSpider import RepublicFloorSpider
from woods.woods.spiders.shawfloorSpider import ShawfloorspiderSpider
from woods.woods.spiders.slccflooringSpider import SlccflooringspiderSpider
from woods.woods.spiders.texastraditionsflooringSpider import TexastraditionsflooringspiderSpider
from woods.woods.spiders.tropicalflooringSpider import TropicalflooringspiderSpider
from woods.woods.spiders.uniflooraquaSpider import UniflooraquaspiderSpider
from woods.woods.spiders.urbanfloorSpider import UrbanfloorspiderSpider
from woods.woods.spiders.valenciahardwoodsSpider import ValenciahardwoodsspiderSpider


import sqlite3 as sql
from datetime import datetime

from twisted.internet import reactor
from scrapy.utils.log import configure_logging
import os.path



app = Flask(__name__)
output_data = []
crawl_runner = CrawlerRunner()                  # requires the Twisted reactor to run

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "products.db")

@app.route('/updateprice', methods = ['GET', 'POST'])
def updateprice():
    if(request.method=='POST'):
        
        
        value = request.form['prices']
        
        pk = request.form['pk']
        
        table_name = 'exisiting_products'
        # Creating a connection to database
        conn = sql.connect(db_path)
        
        conn.row_factory = sql.Row
        # Creating an object of the Database to perform the operations.
        c = conn.cursor()
        
        c.execute(''' SELECT * from exisiting_products where formattedcode='%s' ''' %pk)
        
        rows = c.fetchall()
        
        print(len(rows))
        print(pk)
        print(value)
        
        
        if(len(rows)==0):
            print('Error: data not  found')
        else:
            c.execute(''' UPDATE exisiting_products SET price=? WHERE formattedcode=? ''', (value, pk))
            conn.commit()


        
        c.execute(''' SELECT * from '%s' '''%table_name)
        rows = c.fetchall()
        output_data = ([dict(i) for i in rows])

        conn.close()   

        return render_template('new.html', products = output_data )

    else:
        
        return ('sdff')

@app.route('/', methods = ['GET', 'POST'])
def show_all():
    if(request.method=='POST'):
        print("post")

        return redirect(url_for('scrape')) # Passing to the Scrape function
        #return render_template('show_all.html', products = products.query.all() )
    else:
        table_name = 'new_products'
        etable_name = 'exisiting_products'
        utable_name = 'unavailable_products'
        conn = sql.connect(db_path)
        
        conn.row_factory = sql.Row
        cur = conn.cursor()
        cur.execute(''' SELECT * from '%s' '''%etable_name)
        rows = cur.fetchall()
        output_data = ([dict(i) for i in rows])
        
        

        cur = conn.cursor()
        cur.execute(''' SELECT * from '%s' '''%table_name)
        rows_new = cur.fetchall()
        

        cur = conn.cursor()
        cur.execute(''' SELECT * from '%s' '''%utable_name)
        rows_u= cur.fetchall()

        cur.execute(''' select lastfetcheddate from exisiting_products ORDER by lastfetcheddate DESC LIMIT 1 ''')
        lastdaterow = cur.fetchall()
        output_data_lastdate = ([dict(j) for j in lastdaterow])
        try:
            lastdate = output_data_lastdate[0]['lastfetcheddate']
        except:
            lastdate = ""
        conn.close()   


        #return jsonify(output_data)
        return render_template('show_all.html',  products = output_data, ecount = len(output_data), newcount=len(rows_new), ucount=len(rows_u),totalcount = len(output_data), asOfdate = datetime.now().strftime("%d/%m/%y %H:%M:%S"), lastdate = lastdate)

@app.route("/scrape")
def scrape():
    global output_data
    
    # Getting the unique table name from the input URL.
    table_name = 'new_products'
    etable_name = 'exisiting_products'
    utable_name = 'unavailable_products'
    # Creating a connection to database
    conn = sql.connect(db_path)
    # Creating an object of the Database to perform the operations.
    c = conn.cursor()
    
    # This will extract the count of tables with name='<table_name>'
    # It can only be zero or one.
    #c.execute('''SELECT count(name) FROM sqlite_master WHERE name='%s' AND type='table' '''%table_name)
    
    
    #Get exisitng products count
    conn.row_factory = sql.Row
    c = conn.cursor()
    c.execute(''' SELECT * from '%s' '''%etable_name)
    eCount = len(c.fetchall())
    
    #Delete all products
    #DELETE FROM new_products
    c.execute(''' DELETE FROM '%s' '''%table_name)
    #c.execute(''' DELETE FROM '%s' '''%utable_name)
    conn.commit()
    
    
    # run crawler in twisted reactor synchronously
    scrape_with_crochet()
    time.sleep(900)
    

    #conn.execute('''CREATE TABLE '%s' (title TEXT,  code TEXT, formattedcode TEXT UNIQUE, prices TEXT, vendors TEXT, lastfetcheddate TEXT, archived TEXT, archivedon TEXT, updateinsert TEXT)''' %table_name)
     #Make all prodcuts archived first
    c.execute(''' UPDATE exisiting_products SET archived='Yes', archivedon='%s' '''%datetime.now().strftime("%d/%m/%y %H:%M:%S"))
    conn.commit()
    
    #test for delete
    #i=1
        
    for x in output_data:
        #if (i==140):
        #    break
        
        #print(str(x["formattedcode"]))
        try:
            #this is checking if formatted code already present , if absent add it in both the tables
        
            c.execute('''INSERT INTO '%s' (handle, title, formattedcode, vendor, lastfetcheddate, archived, addedon) VALUES (?,?,?,?,?,?,?)''' %etable_name ,(x["handle"], x["title"], x["formattedcode"],  x["vendor"], datetime.now().strftime("%d/%m/%y %H:%M:%S"), "No",  datetime.now().strftime("%d/%m/%y %H:%M:%S")) )
            c.execute('''INSERT INTO '%s' (handle, title, formattedcode, vendor, lastfetcheddate, archived, addedon) VALUES (?,?,?,?,?,?,?)''' %table_name , (x["handle"], x["title"], x["formattedcode"],  x["vendor"], datetime.now().strftime("%d/%m/%y %H:%M:%S"), "No",  datetime.now().strftime("%d/%m/%y %H:%M:%S")) )
        except:
            c.execute(''' UPDATE exisiting_products SET archived='No', lastfetcheddate=?, archivedon='' WHERE formattedcode=? ''',(datetime.now().strftime("%d/%m/%y %H:%M:%S"),x["formattedcode"]))
            #print('Data already exists')

        #i=i+1
    conn.commit()
 
   
    #Delete all products with archived = Yes
    try:
        c.execute('''INSERT INTO unavailable_products SELECT * FROM exisiting_products WHERE archived='Yes' ''')
    except:
        print('alreaddy there hence not updateing, we can create a loop again and insert items indivually')
    
    #c.execute(''' DELETE from exisiting_products where archived='Yes' ''')
    
    #print('Product Unavaialble')
        
    conn.commit()
 
    conn.row_factory = sql.Row
    cur = conn.cursor()
    cur.execute(''' SELECT * from '%s' '''%table_name)
    rows_new = cur.fetchall()
    

    cur.execute(''' SELECT * from '%s' '''%utable_name)
    rows_u= cur.fetchall()


    cur.execute(''' SELECT * from '%s' '''%etable_name)
    rows = cur.fetchall()
    output_data = ([dict(i) for i in rows])
    
    cur.execute(''' select lastfetcheddate from exisiting_products ORDER by lastfetcheddate DESC LIMIT 1 ''')
    lastdaterow = cur.fetchall()
    output_data_lastdate = ([dict(j) for j in lastdaterow])
    try:
        lastdate = output_data_lastdate[0]['lastfetcheddate']
    except:
        lastdate = ""
    conn.close()   



    #return jsonify(output_data)
    return render_template('show_all.html',  products = output_data, ecount = eCount, newcount=len(rows_new), ucount=len(rows_u),totalcount = len(output_data), asOfdate =  datetime.now().strftime("%d/%m/%y %H:%M:%S"), lastdate = lastdate)
    #scrape_with_crochet(baseURL=baseURL) # Passing that URL to our Scraping Function

    #time.sleep(20) # Pause the function while the scrapy spider is running
    
    #return jsonify(output_data) # Returns the scraped data after being running for 20 seconds.


@crochet.run_in_reactor
def scrape_with_crochet():
    # This will connect to the dispatcher that will kind of loop the code between these two functions.
    # signal fires when single item is processed
    # and calls _crawler_result to append that ite
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)
    
    
    configure_logging()
    crawl_runner.crawl(AayersfloorsspiderSpider)
    crawl_runner.crawl(AmericanheritagefloorsspiderSpider)
    crawl_runner.crawl(ArimarwoodspiderSpider)
    crawl_runner.crawl(BhwfloorsspiderSpider)
    crawl_runner.crawl(BpiprestigespiderSpider)
    crawl_runner.crawl(BrucespiderSpider)
    crawl_runner.crawl(DdcfloorsspiderSpider)
    crawl_runner.crawl(EaglecreekfloorsspiderSpider)
    crawl_runner.crawl(EarthwerksspiderSpider)
    crawl_runner.crawl(EleganzatilesspiderSpider)
    crawl_runner.crawl(EvafloorsspiderSpider)
    crawl_runner.crawl(FuzionflooringspiderSpider)
    crawl_runner.crawl(HillcountryinnovationsspiderSpider)
    crawl_runner.crawl(IndusparquetspiderSpider)
    crawl_runner.crawl(JohnsonHardwoodspiderSpider)
    crawl_runner.crawl(LawsonfloorsspiderSpider)
    crawl_runner.crawl(LicousspiderSpider)
    crawl_runner.crawl(LwflooringspiderSpider)
    crawl_runner.crawl(ManningtonspiderSpider)
    crawl_runner.crawl(MohawkflooringspiderSpider)
    crawl_runner.crawl(MontserratfloorsspiderSpider)
    crawl_runner.crawl(MsisurfacesspiderSpider)
    crawl_runner.crawl(MullicanflooringspiderSpider)
    crawl_runner.crawl(RealwoodfloorsspiderSpider)
    crawl_runner.crawl(ShawfloorspiderSpider)
    crawl_runner.crawl(SlccflooringspiderSpider)
    crawl_runner.crawl(TexastraditionsflooringspiderSpider)
    crawl_runner.crawl(TropicalflooringspiderSpider)
    crawl_runner.crawl(UniflooraquaspiderSpider)
    crawl_runner.crawl(UrbanfloorspiderSpider)
    crawl_runner.crawl(ValenciahardwoodsspiderSpider)
    d = crawl_runner.join()
    d.addBoth(lambda _: reactor.stop())

    eventual = reactor.run() # the script will block here until all crawling jobs are finished
    
    # This will connect to the ReviewspiderSpider function in our scrapy file and after each yield will pass to the crawler_result function.
    #eventual = crawl_runner.crawl(SpiderSpider)
    return eventual




#This will append the data to the output data list.
def _crawler_result(item, response, spider):
    output_data.append(dict(item))
    
    

@app.route('/unavaialable', methods = ['GET', 'POST'])
def unavaialable():
    table_name = 'unavailable_products'
    # Creating a connection to database
    conn = sql.connect(db_path)
    
    conn.row_factory = sql.Row
    # Creating an object of the Database to perform the operations.
    c = conn.cursor()
    
    c.execute(''' SELECT * from '%s' '''%table_name)
    rows = c.fetchall()
    output_data = ([dict(i) for i in rows])

    conn.close()   
    
    if(request.method=='POST'):
        '''Fetch data and add it to the database'''
    return render_template('unavaialable.html', products = output_data)


@app.route('/new', methods = ['GET', 'POST'])
def new():
    table_name = 'new_products'
    # Creating a connection to database
    conn = sql.connect(db_path)
    
    conn.row_factory = sql.Row
    # Creating an object of the Database to perform the operations.
    c = conn.cursor()
    
    c.execute(''' SELECT * from '%s' '''%table_name)
    rows = c.fetchall()
    output_data = ([dict(i) for i in rows])

    conn.close()   
    
    if(request.method=='POST'):
        '''Fetch data and add it to the database'''
    return render_template('new.html', products = output_data )

@app.route('/websites', methods = ['GET', 'POST'])
def websites():

    # Creating a connection to database
    conn = sql.connect(db_path)
    
    conn.row_factory = sql.Row
    # Creating an object of the Database to perform the operations.
    c = conn.cursor()
    
    c.execute(''' SELECT count(vendor) as product_qty_per_vendor, vendor FROM exisiting_products GROUP by vendor ''')
    rows = c.fetchall()
    output_data = ([dict(i) for i in rows])

    conn.close()   

    
    if(request.method=='POST'):
        '''Fetch data and add it to the database'''
    return render_template('websites.html', product_qtys=output_data )


if __name__ == '__main__':
   app.run(debug = True)

