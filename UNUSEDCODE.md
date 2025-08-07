'''
    Has issues with html.render hanging infinitely

    def get_article_links(self):
        article_links = set()

        for url in self.home_urls:
            try:

                print("Trying")
                homepage = self.session.get(url, headers=self.headers)
                print("Got homepage. Rendering")

                homepage.html.render(timeout=10)

                print("Rendered")

                soup = BeautifulSoup(homepage.html.html, "lxml")


                #Loops through <a> tags that have href attribute
                for a in soup.find_all("a", href=True):
                    href = a["href"]
                    
                    
                    #Joins together the parsed url with the main url
                    full_url = urljoin(url,href)
                    
                    print(full_url)


                    #Separates url into main part and then suburl
                    path = urlparse(full_url).path

                    if (any(re.match(pattern, path) for pattern in REGEX_PATTERNS)) and any(keyword.lower() in path.lower() for keyword in EM_KEYWORDS):
                        article_links.add(full_url)
                    elif (any (keyword in path.lower() for keyword in HOME_KEYWORDS))and  any(keyword.lower() in path.lower() for keyword in EM_KEYWORDS):
                        article_links.add(full_url)


            except Exception as e: 
                print(f"Error during homepage scraping: {e}")
        return article_links
    '''

    '''
    def get_content(self, urls):
        results = []
        now = datetime.now(timezone.utc)
        ha24 = now - timedelta(days=1)
    
        for url in urls:

            try:
                
                #Makes http request to get HTML from URL
                response = self.session.get(url, headers=HEADERS, timeout=20)
                response.raise_for_status()  # Raise an error for 4xx/5xx status codes
                soup = BeautifulSoup(response.text, 'lxml')
            except Exception as e:
                print(f" Failed to fetch HTML from {url}: {e}")
                continue

                
            try:
                '''
                #Gets Publication Date
                '''
                date = None
                #Loop through list of common date attributes
                for attrs in DATE_ATTRS:
                    #find the meta date tag
                    meta_date = soup.find("meta", attrs=attrs)
                    #Check to see if date tag was found, and if there was content inside
                    if meta_date and meta_date.get("content"):
                        date_str = meta_date["content"]
                        #Create date object. Replace "Z" with UTC offset
                        if date_str.endswith("Z"):
                            date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                        else:
                            # Parse as naive datetime, then make it UTC-aware
                                date = datetime.fromisoformat(date_str)
                                if date.tzinfo is None:
                                    date = date.replace(tzinfo=timezone.utc)
                        break
                        
            except Exception as e:
                print(f"Error during date parsing block: {e}")  

            if not date:
                try:
                    time_tag = soup.find("time", attrs={"datetime": True})
                    if time_tag:
                        date_str = time_tag["datetime"]
                        if date_str.endswith("Z"):
                            date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                        else:
                            date = datetime.fromisoformat(date_str)
                        if date.tzinfo is None:
                            date = date.replace(tzinfo=timezone.utc)
                        #print(f"Parsed from <time>: {date}")
                except Exception as e:
                    print(f"time fallback failed: {e}")
            
        
                
            #If collected date is not a datetime object, skip it to avoid bug
            if not isinstance(date, datetime):
                print("Skipping... date not found or invalid.")
                continue 


            
            #If date published of article is older than 24 hrs skip it
            if date < ha24:
                print ("Skipping... article too old.")
                continue

            try:
                '''
                #Gets Title
                '''
                # Extract the <h1> title
                title_tag = soup.find("h1")
                #If titletag is not none, strip.
                title = title_tag.text.strip() if title_tag else ""
            except Exception as e:
                print(f"Title parsing failed: {e}")
            
            try:
                '''
                #Gets Body Content
                '''
                body = None
                #Look for common content tags
                for cls in POSSIBLE_CLASSES:
                    body = soup.find("div", class_=re.compile(cls, re.IGNORECASE))
                    if body:
                        break
                
                if not body:
                    for div in soup.find_all("div"):
                        ps = div.find_all("p")
                        if len([p for p in ps if p.get_text(strip=True)]) >= 1:
                            body = div
                            break

                if body:
                    paragraphs = body.find_all("p")
                else:
                    article = soup.find("article")
                    paragraphs = article.find_all("p") if article else soup.find_all("p")

                content = '\n\n'.join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
                
                if not content.strip():
                    try:
                        og_desc = soup.find("meta", property="og:description")
                        if og_desc and og_desc.get("content"):
                            content = og_desc["content"].strip()
                            print("Used og:description as fallback content.")
                    except Exception as e:
                        print(f"Failed to extract og:description: {e}")
        
            except Exception as e:
                print(f"Content parsing failed: {e}")
                
            if not content.strip():
                print("Skipping... content is empty.")
                continue

            is_duplicate = False
            for i, existing_article in enumerate(results):
                if self.calc_sim_titles(title, existing_article["title"]):
                    is_duplicate = True
                    if len(content) > len(existing_article["content"]):
                        results[i] = {
                        "url": url,
                        "title": title,
                        "date": date,
                        "content": content
                        }
                    break

            if not is_duplicate:
                results.append({
                    "url": url,
                    "title": title,
                    "date": date,
                    "content": content
                })

        return results
        '''