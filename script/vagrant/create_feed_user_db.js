conn = new Mongo("localhost:27017");
db = conn.getDB("feedlark");
print("all dbs", db.adminCommand('listDatabases'));



db.feed.insert([{ "url": "https://news.ycombinator.com/rss",
                    "items": [
	                        {"name": "A Message to Our Loyal Customers",
                    		"pub_date": "time.struct_time(tm_year=2016, tm_mon=2, tm_mday=14, tm_hour=21, tm_min=10, tm_sec=2, tm_wday=6, tm_yday=45, tm_isdst=0)",
                            "link": "http://www.apple.com/customer-letter/",
                    		"arictle_text": "February 16, 2016 A Message to Our Customers. The United States government has demanded that Apple take an unprecedented step which threatens the security of our customers. We oppose this order, which has implications far beyond the legal case at hand. This moment calls for public discussion, and we want our customers and people around the country to understand what is at stake."
                    	    },
	                           {"name": "How to get hired at a startup when you don't know anyone",
		                        "pub_date": "time.struct_time(tm_year=2016, tm_mon=2, tm_mday=14, tm_hour=21, tm_min=12, tm_sec=2, tm_wday=6, tm_yday=45, tm_isdst=0)",
		                        "link": "http://shane.engineer/blog/how-to-get-hired-at-a-startup-when-you-don-t-know-anyone",
		                        "article_text": "If you really want to be at a company you can do so much better than a resume. A few years ago I saw an early stage startup that I knew I had to be a part of. The only problem was that it was 900 miles away and I had no connection to them. The startup was Formlabs. At they time they had 10 employees, and like most startups reduced risk by hiring people they knew. They were also situated equidistant between MIT and Harvard so there was healthy local competition. The standard approach of sending in my resume and a carefully crafted cover letter didn't work, so I decided to do something dramatic."
		                        }]},
                    {"url": "http://dave.cheney.net/feed",
                	"items": [{
                	    "name": "Unhelpful abstractions",
                	    "pub_date": "time.struct_time(tm_year=2016, tm_mon=2, tm_mday=14, tm_hour=21, tm_min=14, tm_sec=2, tm_wday=6, tm_yday=45, tm_isdst=0)",
                	    "link": "http://dave.cheney.net/2016/02/06/unhelpful-abstractions",
                	    "arictle_text": "It turned out that createOutputFile was written in an obscure way which first caused me to look at it more closely. Why the code expected the file to exist before starting wasn’t immediately clear. It may have been because some other goroutine was expecting the file to exist on disk, even if nothing had been written yet (slight race smell), or more likely the necessary information was not available for the job itself to create the file with the correct permissions. This calls for a refactoring!"
                	      },
                	      {
                	        "name": "cgo is not Go",
                	        "pub_date": "time.struct_time(tm_year=2016, tm_mon=2, tm_mday=14, tm_hour=21, tm_min=16, tm_sec=2, tm_wday=6, tm_yday=45, tm_isdst=0)",
                	        "link": "http://dave.cheney.net/2016/01/18/cgo-is-not-go",
                	        "article_text": "To steal a quote from JWZ, Some people, when confronted with a problem, think “I know, I’ll use cgo.” Now they have two problems. Recently the use of cgo came up on the Gophers’ slack channel and I voiced my concerns that using cgo, especially on a project that is intended to showcase Go inside an organisation was a bad idea. I’ve said this a number of times, and people are probably sick of hearing my spiel, so I figured that I’d write it down and be done with it."
                	    }]},
                    {"url": "http://spritesmods.com/rss.php",
            	    "items": [{ "name": "Creating the Tamagotchi Singularity",
            	                "pub_date": "time.struct_time(tm_year=2016, tm_mon=2, tm_mday=14, tm_hour=21, tm_min=18, tm_sec=2, tm_wday=6, tm_yday=45, tm_isdst=0)",
            	                "link": "http://spritesmods.com/?art=tamasingularity&amp;f=rss",
            	                "arictle_text": "Building the Tamagotchi Singularity. The Singularity has happened, but not to us. I also gave a talk about this project on the Hackaday Superconference 2015. There is a video available of that if you'd rather watch me talk. You can also directly view the end result if you so please. As some of you may know, I recently moved from the Netherlands to Shanghai. In the long term, this is great for my hobby: I got a fair amount of stuff out of China anyway, and me moving there meant I wouldn't have to wait a month for it to arrive anymore. In the short term, my ability to build things took somewhat of a hit, though: aside from my oscilloscope and some small bits and bobs I thought I would have a hard time getting in China, I left most of my electronic stuff back in the Netherlands, with the idea that I would be able to buy myself most stuff anew when I had the time."
            		            },
            			{"name": "Dekatron as Internet speed indicator",
            	          "pub_date": "time.struct_time(tm_year=2016, tm_mon=2, tm_mday=14, tm_hour=21, tm_min=20, tm_sec=2, tm_wday=6, tm_yday=45, tm_isdst=0)",
            	          "link": "http://spritesmods.com/?art=dekatron&amp;f=rss",
            	          "article_text": "ntro. As most electronic engineers and hobbyists do, I have a great respect for the earlier ways of controlling electrons, before it was found out that silicon could be used to miniaturize everything a thousandfold. It is amazing that things like a vacuum, a glow wire and a bunch of strange-looking metal bits can actually do useful stuff. The amazing-ness of it all gets even better if there are vistime.struct_time(tm_year=2016, tm_mon=2, tm_mday=14, tm_hour=21, tm_min=10, tm_sec=2, tm_wday=6, tm_yday=45, tm_isdst=0)uals involved: while vacuum tubes only have the faint glow of the heater, tubes filled with neon are more interesting because they can be used to display stuff. Nixie tubes are a prime example of those."
            		  }]}   ])
db.user.insert([
{
	username: "iandioch",
	email: "noah@feedlark.com",
	hashed_password: "IjZAgcfl7p92ldGxad68LJZdL17lhWy",
	password_salt: "N9qo8uLOickgx2ZMRZoMye",
	subscribed_feeds: ["news.ycombinator.com/rss", "pssd.computing.dcu.ie/rss.xml"]
},
{
	username: "sully",
	email: "ross@feedlark.com",
	hashed_password: "IjZAgcfl7p92ldGxad68LJZdL17lhWy",
	password_salt: "N9qo8uLOickgx2ZMRZoMye",
	subscribed_feeds: ["news.ycombinator.com/rss", "http://spritesmods.com/rss.php","http://dave.cheney.net/feed"]
},
{
	username: "theotherguys",
	email: "nondb@feedlark.com",
	hashed_password: "IjZAgcfl7p92ldGxad68LJZdL17lhWy",
	password_salt: "N9qo8uLOickgx2ZMRZoMye",
	subscribed_feeds: ["news.ycombinator.com/rss", "http://spritesmods.com/rss.php"]
},
])
db.g2g.insert([
    {"username": "iandioch",
        "feeds": [
            {"feed" : "https://news.ycombinator.com/rss",
    			"name": "A Message to Our Loyal Customers",
    			"pub_date": "time.struct_time(tm_year=2016, tm_mon=2, tm_mday=14, tm_hour=21, tm_min=10, tm_sec=2, tm_wday=6, tm_yday=45, tm_isdst=0)",
                "link" : "http://www.apple.com/customer-letter/"},
            {"feed" : "https://news.ycombinator.com/rss",
    			"name": "How to get hired at a startup when you don't know anyone",
    			 "pub_date": "time.struct_time(tm_year=2016, tm_mon=2, tm_mday=14, tm_hour=21, tm_min=12, tm_sec=2, tm_wday=6, tm_yday=45, tm_isdst=0)",
    			 "link": "http://shane.engineer/blog/how-to-get-hired-at-a-startup-when-you-don-t-know-anyone" }
             ]
    },
    {"username": "sully",
        "feeds": [
            {"feed" : "https://news.ycombinator.com/rss",
    			"name": "A Message to Our Loyal Customers",
    			"pub_date": "time.struct_time(tm_year=2016, tm_mon=2, tm_mday=14, tm_hour=21, tm_min=10, tm_sec=2, tm_wday=6, tm_yday=45, tm_isdst=0)",
                "link" : "http://www.apple.com/customer-letter/"},
            {"feed":"https://news.ycombinator.com/rss",
    			"name": "How to get hired at a startup when you don't know anyone",
    			 "pub_date": "time.struct_time(tm_year=2016, tm_mon=2, tm_mday=14, tm_hour=21, tm_min=12, tm_sec=2, tm_wday=6, tm_yday=45, tm_isdst=0)",
    			 "link": "http://shane.engineer/blog/how-to-get-hired-at-a-startup-when-you-don-t-know-anyone"},
    		{"feed":"http://dave.cheney.net/feed",
    			"name": "Unhelpful abstractions",
    			"pub_date": "time.struct_time(tm_year=2016, tm_mon=2, tm_mday=14, tm_hour=21, tm_min=14, tm_sec=2, tm_wday=6, tm_yday=45, tm_isdst=0)",
    			"link": "http://dave.cheney.net/2016/02/06/unhelpful-abstractions"},
    		{"feed":"http://dave.cheney.net/feed",
    			"name": "cgo is not Go",
    			"pub_date": "time.struct_time(tm_year=2016, tm_mon=2, tm_mday=14, tm_hour=21, tm_min=16, tm_sec=2, tm_wday=6, tm_yday=45, tm_isdst=0)",
    			"link": "http://dave.cheney.net/2016/01/18/cgo-is-not-go"},
    		{"feed":"http://spritesmods.com/rss.php",
    			"name": "Creating the Tamagotchi Singularity",
    			"pub_date": "time.struct_time(tm_year=2016, tm_mon=2, tm_mday=14, tm_hour=21, tm_min=18, tm_sec=2, tm_wday=6, tm_yday=45, tm_isdst=0)",
    			"link": "http://spritesmods.com/?art=tamasingularity&amp;f=rss"},
    		{"feed":"http://spritesmods.com/rss.php",
    			"name": "Dekatron as Internet speed indicator",
    			  "pub_date": "time.struct_time(tm_year=2016, tm_mon=2, tm_mday=14, tm_hour=21, tm_min=20, tm_sec=2, tm_wday=6, tm_yday=45, tm_isdst=0)",
    			  "link": "http://spritesmods.com/?art=dekatron&amp;f=rss"}
        ]
    },
    {"username": "theotherguys",
        "feeds": [
            {"feed":"https://news.ycombinator.com/rss",
    			"name": "A Message to Our Loyal Customers",
    			"pub_date": "time.struct_time(tm_year=2016, tm_mon=2, tm_mday=14, tm_hour=21, tm_min=10, tm_sec=2, tm_wday=6, tm_yday=45, tm_isdst=0)",
                "link":"http://www.apple.com/customer-letter/"},
            {"feed":"https://news.ycombinator.com/rss",
    			"name": "How to get hired at a startup when you don't know anyone",
    			 "pub_date": "time.struct_time(tm_year=2016, tm_mon=2, tm_mday=14, tm_hour=21, tm_min=12, tm_sec=2, tm_wday=6, tm_yday=45, tm_isdst=0)",
    			 "link": "http://shane.engineer/blog/how-to-get-hired-at-a-startup-when-you-don-t-know-anyone"},
    		{"feed":"http://spritesmods.com/rss.php",
    			"name": "Creating the Tamagotchi Singularity",
    			"pub_date": "time.struct_time(tm_year=2016, tm_mon=2, tm_mday=14, tm_hour=21, tm_min=18, tm_sec=2, tm_wday=6, tm_yday=45, tm_isdst=0)",
    			"link": "http://spritesmods.com/?art=tamasingularity&amp;f=rss"},
    		{"feed":"http://spritesmods.com/rss.php",
    			"name": "Dekatron as Internet speed indicator",
    			  "pub_date": "time.struct_time(tm_year=2016, tm_mon=2, tm_mday=14, tm_hour=21, tm_min=20, tm_sec=2, tm_wday=6, tm_yday=45, tm_isdst=0)",
    			  "link": "http://spritesmods.com/?art=dekatron&amp;f=rss"}
        ]
    }
])

print("all collections", db.getCollectionNames());
