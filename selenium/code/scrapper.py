from bs4 import BeautifulSoup
from datetime import datetime
from psycopg2 import connect
from decimal import Decimal
import sys
import requests

class Scrapper:
    def __init__(self):
        url = "https://www.worldometers.info/coronavirus/"
        session = requests.Session()
        session.trust_env = False

        # headers = {
        #     'Upgrade-Insecure-Requests': '1',
        #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) '
        #                 'Chrome/72.0.3626.119 Safari/537.36',
        #     'DNT': '1'
        # }
        

        print("testing")

        # declare connection instance
        conn = connect(
            dbname = "covid19",
            user = "docker",
            host = "172.28.1.4",
            password = "docker")

        print(conn)

        command = (
            """
                CREATE TABLE IF NOT EXISTS countries (
                    country_id SERIAL PRIMARY KEY,
                    country_name varchar(50),
                    total_cases decimal,
                    new_cases decimal,
                    total_deaths decimal,
                    new_deaths decimal,
                    total_recovered decimal,
                    active_cases decimal,
                    serious_critical decimal,
                    total_case_per_mil decimal,
                    death_per_mil decimal,
                    total_tests decimal,
                    test_per_mil decimal
                )
            """
        )

        cur = conn.cursor()
        cur.execute(command)
        conn.commit()

        print("Finish Creating Tables")
        try:
            print("getting url")
            response = session.get(url, verify=False)
            print(self.decoding_ascii(response.text))
            print("continue")

            print("BeautifulSoup Constructor")
            print("===========================")
            soup = BeautifulSoup(response.text, 'html.parser')
            print("Generating result")
            print("===========================\n")
            main_country_table = soup.find('table', id="main_table_countries_today")
            news_block = soup.find('div',id="news_block")
            # today_update = news_block.find('div' , id="newsdate{}".format(datetime.today().strftime('%Y-%m-%d')))

            print("Type of main_country_table:{}".format(type(main_country_table)))

            tr_lines = False
            header_keys = False
            if main_country_table.tr != "":
                tr_lines = main_country_table.find_all('tr')
            if tr_lines:
                header_keys = tr_lines[0].find_all('th')
            # print(browser.title)
            print("\n\n\n\n")

            data = []
            header_data = []

            for header in header_keys:
                header_text= (self.decoding_ascii(header.text)).replace("\n","")
                header_data.append(header_text)

            for idx_tr, tr in enumerate(tr_lines):
                
                if not tr.attrs.get('style'):
                    rows_data = []
                    for idx_td, td in enumerate(tr.find_all('td')):
                        if idx_tr >= 2:
                            print(idx_td)
                            if idx_td == 0:
                                result_str = ""
                                if (td.a):
                                    result_str = self.decoding_ascii(td.a.text) if td.a.contents else ""
                                elif td.contents:
                                    result_str = self.decoding_ascii(td.text) if td.contents else ""
                                rows_data.append(result_str.strip())
                            elif idx_td == 12:
                                continue
                            else:
                                rows_data.append(self.retrieve_number(self.decoding_ascii(td.text) if td.contents else ""))
                    data.append(rows_data)

            print("finish getting data")
            data.pop(0)
            print(len(data))

            args_str = b",".join(cur.mogrify("(%s, %s, %s, %s, %s , %s, %s, %s, %s, %s, %s, %s)", tuple(x)) for x in data)
            print(args_str)
            cur.execute(b"INSERT INTO public.countries(country_name, total_cases, new_cases, total_deaths, new_deaths, total_recovered, active_cases, serious_critical, total_case_per_mil, death_per_mil, total_tests, test_per_mil)VALUES " + args_str) 
            conn.commit()
            postgres_insert_query = ""
            for res in data:
                if len(res) > 0:

                    
                    postgres_insert_query = """
                        INSERT INTO public.countries(
                        country_name, total_cases, new_cases, total_deaths, new_deaths, total_recovered, active_cases, serious_critical, total_case_per_mil, death_per_mil, total_tests, test_per_mil)
                        VALUES ('{country_name}', {total_cases}, {new_cases}, {total_deaths}, {new_deaths}, {total_recovered}, {active_cases}, {serious_critical}, {total_case_per_mil}, {death_per_mill}, {total_tests}, {test_per_mil});
                    """.format(
                        country_name = str(res[0]),
                        total_cases = retrieve_number(res[1]),
                        new_cases = retrieve_number(res[2]),
                        total_deaths = retrieve_number(res[3]),
                        new_deaths = retrieve_number(res[4]),
                        total_recovered = retrieve_number(res[5]),
                        active_cases = retrieve_number(res[6]),
                        serious_critical = retrieve_number(res[7]),
                        total_case_per_mil = retrieve_number(res[8]),
                        death_per_mill = retrieve_number(res[9]),
                        total_tests = retrieve_number(res[10]),
                        test_per_mil = retrieve_number(res[11]),
                    )
                    cur.execute(postgres_insert_query)
                    conn.commit()
                    flag = "hello, {0}".format("test")
        except:
            e = sys.exc_info()
            print( "<p>Error: %s</p>" % e )
        finally:
            cur.close()
            conn.close()
            # browser.quit()

        news_update = []

        # news_post = today_update.find_all("div", class_="news_post")
        # news_date = news_block.find("div", class_="news_date").text

        # for news in news_post:
        #     info = {}
        #     info.update({"news":self.decoding_ascii(news.div.ul.li.text)})
        #     source_links = news.find_all("a")
        #     links=[]
        #     for link in source_links:
        #         links.append(link.get("href"))
        #     info.update({"sources" : ",".join(links)})
        #     news_update.append(info)

        # print(len(news_update))
        # print(news_update[0])

        # display.stop()  

    def decoding_ascii(self, data):
        return data.encode('utf-8').decode('ascii', 'ignore')
    
    def retrieve_number(self, data):
        result = data.strip()
        if len(result)>0 and any(char.isdigit() for char in result):
            return Decimal(result.replace(",",""))
        else:
            return Decimal(0)
